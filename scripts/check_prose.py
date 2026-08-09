"""Check every Markdown file for the prose punctuation rules.

The rules from SKILL.md: no em or en dashes as punctuation, no semicolons in
prose, and no spaced hyphens standing in for other punctuation. Fenced code
blocks, inline code, URLs, and HTML entities are exempt because the characters
there are content rather than punctuation. Exits 1 with one line per violation.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^(\s*)(`{3,})")


def check(path: Path) -> list[str]:
    violations = []
    fence_len = 0
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        fence = FENCE.match(raw)
        if fence:
            ticks = len(fence.group(2))
            if fence_len == 0:
                fence_len = ticks
            elif ticks >= fence_len:
                fence_len = 0
            continue
        if fence_len:
            continue
        body = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", raw)
        body = re.sub(r"`[^`]*`", "", body)
        body = re.sub(r"\(http[^)]*\)", "", body)
        body = re.sub(r"&[a-z]+;", "", body)
        if "—" in raw or "–" in raw:
            violations.append(f"{path.relative_to(REPO)}:{lineno}: em or en dash: {raw.strip()}")
        if " - " in body:
            violations.append(f"{path.relative_to(REPO)}:{lineno}: spaced hyphen: {raw.strip()}")
        if ";" in body:
            violations.append(f"{path.relative_to(REPO)}:{lineno}: semicolon in prose: {raw.strip()}")
    return violations


def main() -> int:
    problems = []
    for path in sorted(REPO.glob("**/*.md")):
        if ".git" in path.parts:
            continue
        problems.extend(check(path))
    if problems:
        print("\n".join(problems))
        return 1
    print(f"prose punctuation clean across {len(list(REPO.glob('**/*.md')))} Markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
