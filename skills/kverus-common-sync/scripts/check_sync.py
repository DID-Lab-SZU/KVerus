#!/usr/bin/env python3
"""Check that kverus-common references are synchronized with the local Verus guide."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


GUIDE_REL = Path("database/verified/code/tools/verus/source/docs/guide/src")


def agent_dir() -> Path:
    if "AGENT_DIR" in os.environ:
        return Path(os.environ["AGENT_DIR"])
    return Path(__file__).resolve().parents[3]


def common_rel() -> Path:
    return agent_dir() / "skills" / "kverus-common"


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    common = common_rel()
    for path in [cur, *cur.parents]:
        if (path / common).exists() and (path / GUIDE_REL).exists():
            return path
    raise SystemExit(
        "error: could not find repo root containing both "
        f"{common} and {GUIDE_REL}; pass --repo-root or set AGENT_DIR"
    )


def parse_source_paths(text: str) -> list[str]:
    lines = text.splitlines()
    sources: list[str] = []
    in_sources = False
    for line in lines:
        if line.strip() == "Sources:":
            in_sources = True
            continue
        if in_sources:
            if line.startswith("- "):
                match = re.search(r"`([^`]+)`", line)
                if match:
                    sources.append(match.group(1))
                continue
            if line.strip() == "":
                continue
            break
    return sources


def markdown_code_refs(text: str) -> list[str]:
    return re.findall(r"`([^`]+\.md)`", text)


def is_guide_source_line(line: str) -> bool:
    return line.startswith(
        "- `database/verified/code/tools/verus/source/docs/guide/src/"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument(
        "--strict-mtime",
        action="store_true",
        help="treat guide files newer than their kverus-common reference as errors",
    )
    args = parser.parse_args()

    repo = args.repo_root.resolve() if args.repo_root else find_repo_root(Path.cwd())
    common = repo / common_rel()
    guide = repo / GUIDE_REL
    refs_dir = common / "references"

    errors: list[str] = []
    warnings: list[str] = []

    if not common.is_dir():
        errors.append(f"missing kverus-common directory: {common}")
    if not guide.is_dir():
        errors.append(f"missing Verus guide directory: {guide}")
    if not refs_dir.is_dir():
        errors.append(f"missing references directory: {refs_dir}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    files = sorted([common / "SKILL.md", *refs_dir.glob("*.md")])
    if len(files) <= 1:
        errors.append(f"no reference markdown files found under {refs_dir}")

    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(repo)

        if path.parent == refs_dir:
            sources = parse_source_paths(text)
            if not sources:
                errors.append(f"{rel}: missing Sources block")
            for source in sources:
                if not source.startswith(str(GUIDE_REL) + "/"):
                    errors.append(f"{rel}: source is not under Verus guide: {source}")
                    continue
                source_path = repo / source
                if not source_path.is_file():
                    errors.append(f"{rel}: missing guide source: {source}")
                    continue
                if source_path.stat().st_mtime > path.stat().st_mtime:
                    msg = f"{rel}: guide source newer than reference: {source}"
                    if args.strict_mtime:
                        errors.append(msg)
                    else:
                        warnings.append(msg)

        for lineno, line in enumerate(text.splitlines(), start=1):
            if is_guide_source_line(line):
                continue
            for ref in markdown_code_refs(line):
                if ref.startswith("references/"):
                    continue
                if ref.startswith(str(GUIDE_REL) + "/"):
                    continue
                errors.append(
                    f"{rel}:{lineno}: bare markdown reference should use references/...: {ref}"
                )

    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    if warnings:
        print(f"\nOK with warnings: {len(warnings)} warning(s)")
        return 2
    print("OK: kverus-common is structurally synchronized with the Verus guide sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
