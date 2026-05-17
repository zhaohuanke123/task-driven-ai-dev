#!/usr/bin/env python3
"""
Deploy coding-workflow architecture files to a project directory.

Usage:
    python install.py --target <path> [options]

If options are omitted, prompts interactively.

Examples:
    python install.py --target ../my-app --name "Blog System" \\
        --tech-frontend "React+TypeScript+Tailwind" \\
        --tech-backend "Node.js+Express" \\
        --tech-database "PostgreSQL"
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

TEMPLATE_DIR = Path(__file__).resolve().parent / "assets" / "templates"
AGENTS_DIR = Path(__file__).resolve().parent / "assets" / "agents"
HOOKS_DIR = Path(__file__).resolve().parent / "assets" / "hooks"
SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"

TEMPLATES = [
    "CLAUDE.md",
    "architecture.md",
    "task.json",
    "progress.txt",
]

AGENTS = [
    "planner.md",
    "executor.md",
    "verifier.md",
]

HOOKS = [
    "doc-gate.sh",
]


def collect_info(args: argparse.Namespace) -> dict[str, str]:
    """Collect project info from args or interactive prompts."""
    info: dict[str, str] = {}

    def ask(key: str, prompt: str, default: str = "") -> str:
        val = getattr(args, key.replace("-", "_"), None)
        if val:
            print(f"{prompt}: {val}")
            return val
        if default:
            return input(f"{prompt} [{default}]: ") or default
        return input(f"{prompt}: ")

    print("\n=== Project Information ===\n")
    info["name"] = ask("name", "Project name")
    info["description"] = ask("description", "Description (1-2 sentences)")
    info["tech_frontend"] = ask("tech-frontend", "Frontend stack", "React+TypeScript")
    info["tech_backend"] = ask("tech-backend", "Backend stack", "Node.js")
    info["tech_database"] = ask("tech-database", "Database", "PostgreSQL")
    info["tech_auth"] = ask("tech-auth", "Auth solution", "Supabase Auth")

    print()
    return info


def check_existing(target: Path) -> list[str]:
    """Return list of template files that already exist in target."""
    existing = []
    for name in TEMPLATES:
        if (target / name).exists():
            existing.append(name)
    for name in AGENTS:
        if (target / ".agents" / name).exists():
            existing.append(f".agents/{name}")
    return existing


def substitute(content: str, info: dict[str, str]) -> str:
    """Replace placeholders in template content."""
    replacements = [
        # CLAUDE.md + architecture.md
        (r"\[项目名\]", info.get("name", "Project")),
        (r"\[1-2 句话描述项目.*?\]", info.get("description", "A web application")),
        (r"\[项目描述和核心功能\]", info.get("description", "A web application")),
        # architecture.md Tech Stack
        (r"\[例如: React \+ TypeScript \+ Tailwind\]",
         info.get("tech_frontend", "React+TypeScript")),
        (r"\[例如: Node\.js \+ Express\]",
         info.get("tech_backend", "Node.js")),
        (r"\[例如: PostgreSQL\]",
         info.get("tech_database", "PostgreSQL")),
        (r"\[例如: JWT / Supabase Auth\]",
         info.get("tech_auth", "Supabase Auth")),
        (r"\[选择理由\]", "Fill in your reason"),
    ]
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    return content


def deploy(target: Path, info: dict[str, str], overwrite: bool) -> list[str]:
    """Copy templates and agent definitions to target."""
    deployed = []
    target.mkdir(parents=True, exist_ok=True)

    for name in TEMPLATES:
        dest = target / name
        if dest.exists() and not overwrite:
            print(f"  Skipping {name} (already exists)")
            continue

        src = TEMPLATE_DIR / name
        if not src.exists():
            print(f"  WARNING: template not found: {src}")
            continue

        content = src.read_text(encoding="utf-8")
        content = substitute(content, info)
        dest.write_text(content, encoding="utf-8")
        deployed.append(name)
        print(f"  Created {name}")

    agents_target = target / ".agents"
    agents_target.mkdir(parents=True, exist_ok=True)

    for name in AGENTS:
        dest = agents_target / name
        if dest.exists() and not overwrite:
            print(f"  Skipping .agents/{name} (already exists)")
            continue

        src = AGENTS_DIR / name
        if not src.exists():
            print(f"  WARNING: agent definition not found: {src}")
            continue

        content = src.read_text(encoding="utf-8")
        dest.write_text(content, encoding="utf-8")
        deployed.append(f".agents/{name}")
        print(f"  Created .agents/{name}")

    return deployed


def deploy_hooks(target: Path, overwrite: bool) -> list[str]:
    """Deploy hook scripts and settings.json."""
    deployed = []

    hooks_target = target / ".claude" / "hooks"
    hooks_target.mkdir(parents=True, exist_ok=True)

    for name in HOOKS:
        dest = hooks_target / name
        if dest.exists() and not overwrite:
            print(f"  Skipping .claude/hooks/{name} (already exists)")
            continue

        src = HOOKS_DIR / name
        if not src.exists():
            print(f"  WARNING: hook script not found: {src}")
            continue

        content = src.read_text(encoding="utf-8")
        dest.write_text(content, encoding="utf-8")
        deployed.append(f".claude/hooks/{name}")
        print(f"  Created .claude/hooks/{name}")

    settings_src = TEMPLATE_DIR / ".claude" / "settings.json"
    settings_dest = target / ".claude" / "settings.json"

    if not settings_src.exists():
        print(f"  WARNING: settings.json template not found: {settings_src}")
        return deployed

    if settings_dest.exists():
        import json
        try:
            existing = json.loads(settings_dest.read_text(encoding="utf-8"))
            new_hooks = json.loads(settings_src.read_text(encoding="utf-8"))

            if "hooks" not in existing:
                existing["hooks"] = new_hooks.get("hooks", {})
            else:
                existing_hooks = existing["hooks"]
                for event_type, hook_list in new_hooks.get("hooks", {}).items():
                    if event_type in existing_hooks:
                        for new_hook in hook_list:
                            matcher = new_hook.get("matcher", "")
                            existing_matchers = {
                                h.get("matcher", "") for h in existing_hooks[event_type]
                            }
                            if matcher not in existing_matchers:
                                existing_hooks[event_type].append(new_hook)
                    else:
                        existing_hooks[event_type] = hook_list

            settings_dest.write_text(
                json.dumps(existing, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            deployed.append(".claude/settings.json")
            print("  Updated .claude/settings.json (merged hooks)")
        except (json.JSONDecodeError, KeyError):
            print("  WARNING: could not merge settings.json, skipping")
    else:
        settings_dest.parent.mkdir(parents=True, exist_ok=True)
        content = settings_src.read_text(encoding="utf-8")
        settings_dest.write_text(content, encoding="utf-8")
        deployed.append(".claude/settings.json")
        print("  Created .claude/settings.json")

    return deployed


def run_validation(target: Path) -> bool:
    """Run validate_architecture.py on the deployed architecture.md."""
    script = SCRIPTS_DIR / "validate_architecture.py"
    arch = target / "architecture.md"

    if not script.exists():
        print(f"  WARNING: validation script not found: {script}")
        return True
    if not arch.exists():
        print(f"  WARNING: architecture.md not found: {arch}")
        return False

    print(f"\nRunning architecture validation...")
    result = subprocess.run(
        [sys.executable, str(script), "--architecture-file", str(arch)],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deploy coding-workflow architecture files to a project."
    )
    parser.add_argument("--target", required=True, help="Target project directory")
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--description", help="Project description")
    parser.add_argument("--tech-frontend", help="Frontend stack")
    parser.add_argument("--tech-backend", help="Backend stack")
    parser.add_argument("--tech-database", help="Database")
    parser.add_argument("--tech-auth", help="Auth solution")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--skip-validation", action="store_true", help="Skip architecture validation")
    args = parser.parse_args()

    target = Path(args.target).resolve()

    print(f"Target: {target}")

    # Check existing files
    existing = check_existing(target)
    if existing and not args.overwrite:
        print(f"\nFiles already exist: {', '.join(existing)}")
        response = input("Overwrite existing files? [y/N/skip]: ").strip().lower()
        if response == "skip":
            print("Skipping existing files, creating only new ones.")
        elif response == "y" or response == "yes":
            pass  # overwrite
        else:
            print("Cancelled.")
            return 1

    # Collect info and deploy
    info = collect_info(args)

    print("Deploying files...")
    deployed = deploy(target, info, overwrite=args.overwrite)
    hook_deployed = deploy_hooks(target, overwrite=args.overwrite)
    deployed.extend(hook_deployed)

    if not deployed:
        print("\nNo files deployed.")
        return 0

    print(f"\nDeployed {len(deployed)} file(s) to {target}")
    print("  - Project files: CLAUDE.md, architecture.md, task.json, progress.txt")
    print("  - PEV agents: .agents/planner.md, .agents/executor.md, .agents/verifier.md")
    if hook_deployed:
        print("  - Hooks: .claude/hooks/doc-gate.sh, .claude/settings.json")

    # Validate
    if not args.skip_validation:
        ok = run_validation(target)
        if not ok:
            print("\nValidation failed. Fix architecture.md and re-run validation:")
            print(f"  python scripts/validate_architecture.py --architecture-file {target / 'architecture.md'}")
            return 1

    print("\nDone.")
    print(f"\nSubsequent development: AI reads CLAUDE.md on new conversations.")
    print(f"PEV workflow: Planner → Executor → Verifier (see SKILL.md for details).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
