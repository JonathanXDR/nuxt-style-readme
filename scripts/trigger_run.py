"""Run one trigger-eval query against a fresh project root and report the verdict.

Usage: python3 trigger_run.py "<query>"

Prints TRIGGERED or NOT_TRIGGERED on the last line. Implements the corrected
harness from evals/README.md: a real small repository as the project root, the
skill installed project-level, any-point detection of a skill consult, a 120
second budget, and process-group termination so MCP servers cannot be orphaned.
"""

import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

SKILL_SRC = str(Path(__file__).resolve().parent.parent / "nuxt-style-readme")
FIXTURE_SRC = os.path.join(SKILL_SRC, "evals/files/quickmath")
TIMEOUT = 120


def repo_status() -> str:
    proc = subprocess.run(
        ["git", "-C", os.path.dirname(SKILL_SRC), "status", "--porcelain"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        print("WARNING: git status failed, the source repository cannot be verified", file=sys.stderr)
    return proc.stdout


def main() -> int:
    query = sys.argv[1]
    root = tempfile.mkdtemp(prefix="trigger-")
    before = repo_status()
    try:
        for entry in os.listdir(FIXTURE_SRC):
            src = os.path.join(FIXTURE_SRC, entry)
            dst = os.path.join(root, entry)
            shutil.copytree(src, dst) if os.path.isdir(src) else shutil.copy2(src, dst)
        skill_dst = os.path.join(root, ".claude", "skills", "nuxt-style-readme")
        os.makedirs(os.path.dirname(skill_dst), exist_ok=True)
        shutil.copytree(SKILL_SRC, skill_dst)

        proc = subprocess.Popen(
            [
                "claude", "-p", query,
                "--output-format", "stream-json", "--verbose",
                "--max-turns", "8",
                "--dangerously-skip-permissions",
            ],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            start_new_session=True,
        )
        try:
            out, _ = proc.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            out, _ = proc.communicate()

        # A skip-permissions nested session can wander outside its project root.
        # One run did, and wrote a README into the real har2pdf fixture, so every
        # run compares the source repository against its pre-run state.
        added = sorted(set(repo_status().splitlines()) - set(before.splitlines()))
        if added:
            print("WARNING: source repository modified during the run:\n" + "\n".join(added), file=sys.stderr)

        triggered = False
        for line in out.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            for block in (event.get("message") or {}).get("content") or []:
                if block.get("type") != "tool_use":
                    continue
                name = block.get("name", "")
                text = json.dumps(block.get("input", {}))
                if name == "Skill" and "nuxt-style-readme" in text:
                    triggered = True
                if name == "Read" and "skills/nuxt-style-readme/SKILL.md" in text:
                    triggered = True
        print("TRIGGERED" if triggered else "NOT_TRIGGERED")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
