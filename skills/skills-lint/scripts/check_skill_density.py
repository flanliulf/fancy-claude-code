#!/usr/bin/env python3
"""
Check SKILL.md and SKILL.en.md body and Workflow density.

Usage:
    python3 scripts/check_skill_density.py <skill-dir>

Exit codes:
    0: completed, even when warnings are triggered
    1: invalid arguments
    2: target directory does not exist
"""

import argparse
import json
import re
import sys
from pathlib import Path


WORKFLOW_CHARS_LIMIT = 1500
WORKFLOW_RATIO_LIMIT = 0.5
BODY_NEAR_LIMIT = 4500


def split_body(text: str) -> str:
    parts = text.split("---", 2)
    if len(parts) >= 3:
        return parts[2].lstrip("\n")
    return text


def extract_workflow(body: str, filename: str) -> str:
    if filename == "SKILL.en.md":
        pattern = r"^\[Workflow\]\s*$"
    else:
        pattern = r"^\[Workflow（执行流程）\]\s*$"

    match = re.search(pattern, body, re.MULTILINE)
    if not match:
        return ""

    next_section = re.search(r"^\[[^\n]+\]\s*$", body[match.end() :], re.MULTILINE)
    end = match.end() + next_section.start() if next_section else len(body)
    return body[match.start() : end]


def has_workflow_reference(body: str) -> bool:
    reference_patterns = [
        r"`references/[^`]*workflow[^`]*\.md`",
        r"`references/[^`]*流程[^`]*\.md`",
        r"\breferences/[^\s)]*workflow[^\s)]*\.md\b",
    ]
    return any(re.search(pattern, body, re.IGNORECASE) for pattern in reference_patterns)


def inspect_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    body = split_body(text)
    workflow = extract_workflow(body, path.name)
    body_chars = len(body)
    workflow_chars = len(workflow)
    workflow_ratio = workflow_chars / body_chars if body_chars else 0.0
    workflow_reference = has_workflow_reference(body)
    density_warning = workflow_chars > WORKFLOW_CHARS_LIMIT and workflow_ratio > WORKFLOW_RATIO_LIMIT

    return {
        "file": path.name,
        "body_chars": body_chars,
        "workflow_chars": workflow_chars,
        "workflow_ratio": round(workflow_ratio, 4),
        "near_body_limit": body_chars >= BODY_NEAR_LIMIT,
        "has_workflow_reference": workflow_reference,
        "triggered_density_warning": density_warning,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Skill Workflow density.")
    parser.add_argument("skill_dir", help="Path to a Skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    if not skill_dir.exists() or not skill_dir.is_dir():
        print(f"error: target directory does not exist: {skill_dir}", file=sys.stderr)
        return 2

    files = []
    for filename in ("SKILL.md", "SKILL.en.md"):
        path = skill_dir / filename
        if path.exists():
            files.append(inspect_file(path))

    result = {
        "skill_dir": str(skill_dir),
        "thresholds": {
            "workflow_chars": WORKFLOW_CHARS_LIMIT,
            "workflow_ratio": WORKFLOW_RATIO_LIMIT,
            "near_body_limit": BODY_NEAR_LIMIT,
        },
        "files": files,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
