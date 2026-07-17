"""
Check whether README.md, AGENTS.md, and STAN-QUICKSTART.md are still up-to-date
given the changes introduced by a pull request.

Uses the GitHub Models API (gpt-4o-mini) to analyse each file against the PR diff
and posts a PR comment for every file that needs an update.
"""

import json
import os
import sys

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
PR_NUMBER = os.environ["PR_NUMBER"]
REPO = os.environ["REPO"]
DIFF_PATH = os.environ.get("DIFF_PATH", "/tmp/pr.diff")

DOCS_TO_CHECK = ["README.md", "AGENTS.md", "STAN-QUICKSTART.md"]

# GitHub Models API endpoint (available in GitHub Actions with models: read)
MODELS_API_URL = "https://models.inference.ai.azure.com/chat/completions"
MODEL = "gpt-4o-mini"

# Truncation limits (characters) to stay within model context limits
DIFF_LIMIT = 10_000
DOC_LIMIT = 6_000

# Comment marker so old bot comments can be identified and replaced
COMMENT_MARKER = "<!-- docs-freshness-check -->"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_file(path: str) -> str | None:
    """Read a file from disk and return its contents, or None if not found."""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return None


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n\n[… truncated at {limit} characters …]"


def call_models_api(prompt: str) -> dict | None:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }
    try:
        resp = requests.post(MODELS_API_URL, headers=headers, json=payload, timeout=90)
    except requests.RequestException as exc:
        print(f"  Request error: {exc}", file=sys.stderr)
        return None

    if resp.status_code != 200:
        print(
            f"  API error {resp.status_code}: {resp.text[:500]}", file=sys.stderr
        )
        return None

    try:
        data = resp.json()
        raw = data["choices"][0]["message"]["content"]
        return json.loads(raw)
    except (ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        print(
            f"  Response parse error: {exc}\nRaw: {resp.text[:300]}",
            file=sys.stderr,
        )
        return None


def check_doc(doc_name: str, doc_content: str, pr_diff: str) -> dict | None:
    """Ask the AI whether *doc_name* needs updating given the PR diff.

    Returns a dict with keys:
        needs_update (bool): whether the file is outdated.
        reason (str): one-sentence explanation.
        suggested_update (str, optional): replacement content or patch description
            (only present when needs_update is True).
    Returns None if the API call fails or the response cannot be parsed.
    """
    prompt = f"""You are a documentation reviewer. A pull request has been opened in a GitHub repository.
Your job is to decide whether the file `{doc_name}` needs to be updated as a result of the changes in this PR.

## PR diff (may be truncated)
```diff
{truncate(pr_diff, DIFF_LIMIT)}
```

## Current content of `{doc_name}` (may be truncated)
```markdown
{truncate(doc_content, DOC_LIMIT)}
```

Instructions:
1. Check whether the PR introduces new features, removes features, renames things, or changes structure that is described in `{doc_name}`.
2. If the file is already updated in the diff, mark it as NOT needing an update.
3. Only flag a file if there is a clear, concrete reason it is now outdated.
4. If an update is needed, write the exact replacement content (full file) or a focused patch description.

Respond with valid JSON only — no markdown fences around it:
{{
  "needs_update": true | false,
  "reason": "<one-sentence explanation>",
  "suggested_update": "<suggested replacement or patch — omit this key when needs_update is false>"
}}"""

    return call_models_api(prompt)


def get_existing_bot_comments() -> list[dict]:
    """Return all PR comments posted by this action (identified by COMMENT_MARKER)."""
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"

    matches: list[dict] = []
    page = 1
    while True:
        try:
            resp = requests.get(
                url, headers=headers, params={"per_page": 100, "page": page}, timeout=30
            )
        except requests.RequestException:
            break
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        matches.extend([c for c in batch if COMMENT_MARKER in c.get("body", "")])
        page += 1

    return matches

def delete_comment(comment_id: int) -> None:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{REPO}/issues/comments/{comment_id}"
    try:
        requests.delete(url, headers=headers, timeout=30)
    except requests.RequestException:
        pass


def post_comment(body: str) -> None:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    try:
        resp = requests.post(url, headers=headers, json={"body": body}, timeout=30)
        if resp.status_code in (200, 201):
            print(f"  Comment posted: {resp.json().get('html_url', '—')}")
        else:
            print(
                f"  Failed to post comment: {resp.status_code} {resp.text[:300]}",
                file=sys.stderr,
            )
    except requests.RequestException as exc:
        print(f"  Request error when posting comment: {exc}", file=sys.stderr)


def build_comment(doc_name: str, result: dict) -> str:
    """Build a markdown PR comment body for a file that needs updating.

    Args:
        doc_name: filename (e.g. "README.md").
        result: dict from check_doc with keys 'reason' (str) and optionally
                'suggested_update' (str) when needs_update is True.

    Returns a markdown string that includes COMMENT_MARKER for later deduplication.
    """
    suggested = result.get("suggested_update", "")
    if suggested:
        suggested = truncate(str(suggested), 30_000)
    suggested_section = f"\n\n**Suggested update:**\n\n{suggested}" if suggested else ""
    return (
        f"{COMMENT_MARKER}\n"
        f"## 📄 Docs freshness check — `{doc_name}`\n\n"
        f"**Status:** ⚠️ Update suggested\n\n"
        f"**Reason:** {result.get('reason', '')}"
        f"{suggested_section}\n\n"
        f"---\n"
        f"*Generated automatically by the documentation freshness check action.*"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    pr_diff = read_file(DIFF_PATH)
    if not pr_diff:
        print("No diff file found or diff is empty — skipping checks.")
        return

    print("Removing previous freshness-check comments…")
    for old in get_existing_bot_comments():
        delete_comment(old["id"])

    updates_needed = []

    for doc in DOCS_TO_CHECK:
        print(f"\nChecking {doc}…")
        content = read_file(doc)
        if content is None:
            print(f"  File not found — skipping.")
            continue

        result = check_doc(doc, content, pr_diff)
        if result is None:
            print(f"  Could not get AI response — skipping.")
            continue

        if result.get("needs_update"):
            print(f"  ⚠️  Update suggested: {result.get('reason', '')}")
            updates_needed.append(doc)
            post_comment(build_comment(doc, result))
        else:
            print(f"  ✅ Up-to-date.")

    print(
        f"\nDone. Files needing updates: {updates_needed if updates_needed else 'none'}"
    )


if __name__ == "__main__":
    main()
