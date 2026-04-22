"""
create_linear_artifacts.py
==========================
Phase 2 of the spreadsheet-to-linear skill.

Reads the resolved task data (resolved_tasks.json) and skill config
(skill_config.json) from Phase 0/1, then creates all Linear artifacts
in the correct order:

  1. Initiative (one per run, idempotent — skips if already exists)
  2. Projects (one per unique Sub-project, idempotent)
  3. Issues (one per task row, idempotent by title match within project)
  4. Dependency relations (blocks/blockedBy wired after all issues exist)

Idempotency strategy
--------------------
- Before creating any object, the script queries Linear for an existing
  object with the same name (Initiative/Project) or title (Issue).
- If found, it updates rather than duplicates.
- A run log (run_log.json) records every created/updated object ID so
  subsequent runs can skip already-completed work.

Dry-run mode
------------
Pass --dry-run to print every planned API call without executing it.
This is the recommended first step after Phase 1 review.

Usage
-----
    # Dry run first — review what will happen
    python3 create_linear_artifacts.py --dry-run \
        --tasks ./output/resolved_tasks.json \
        --config ./output/skill_config.json \
        --initiative "My Project" \
        --output-dir ./output

    # Execute for real
    python3 create_linear_artifacts.py \
        --tasks ./output/resolved_tasks.json \
        --config ./output/skill_config.json \
        --initiative "My Project" \
        --output-dir ./output
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from config_schema import SkillConfig


# ---------------------------------------------------------------------------
# MCP helper
# ---------------------------------------------------------------------------

def mcp_call(tool: str, args: dict, dry_run: bool = False) -> dict | list | None:
    """
    Call a Linear MCP tool via manus-mcp-cli.
    In dry_run mode, prints the call and returns None without executing.
    """
    if dry_run:
        print(f"  [DRY-RUN] {tool}({json.dumps(args, ensure_ascii=False)[:200]})")
        return None

    cmd = [
        "manus-mcp-cli", "tool", "call", tool,
        "--server", "linear",
        "--input", json.dumps(args),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    marker = "Tool execution result:\n"
    if marker in output:
        json_str = output.split(marker, 1)[1].strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse MCP response for {tool}: {e}\nRaw: {json_str[:500]}")
    if result.returncode != 0:
        raise RuntimeError(f"MCP call failed for {tool}: {result.stderr.strip()}")
    raise RuntimeError(f"Unexpected MCP output for {tool}: {output[:500]}")


# ---------------------------------------------------------------------------
# Run log — tracks created/updated IDs for idempotency
# ---------------------------------------------------------------------------

class RunLog:
    """
    Persists a mapping of logical keys → Linear IDs across runs.
    Keys:
      initiative:<name>      → initiative ID
      project:<name>         → project ID
      issue:<task_id>        → issue ID (Linear identifier, e.g. MCS-42)
    """

    def __init__(self, path: str):
        self.path = path
        self.data: dict = {}
        if Path(path).exists():
            with open(path) as f:
                self.data = json.load(f)

    def get(self, key: str) -> Optional[str]:
        return self.data.get(key)

    def set(self, key: str, value: str) -> None:
        self.data[key] = value
        self._save()

    def _save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def summary(self) -> str:
        return json.dumps(self.data, indent=2)


# ---------------------------------------------------------------------------
# Lookup helpers — find existing Linear objects by name
# ---------------------------------------------------------------------------

def find_existing_initiative(name: str, dry_run: bool) -> Optional[str]:
    """Return the ID of an existing initiative with this name, or None."""
    if dry_run:
        return None
    data = mcp_call("list_initiatives", {})
    for init in data.get("initiatives", []):
        if init["name"].strip().lower() == name.strip().lower():
            return init["id"]
    return None


def find_existing_project(name: str, team_name: str, dry_run: bool) -> Optional[str]:
    """Return the ID of an existing project with this name in the team, or None."""
    if dry_run:
        return None
    data = mcp_call("list_projects", {})
    for proj in data.get("projects", []):
        if proj["name"].strip().lower() == name.strip().lower():
            # Check it belongs to the right team
            teams = [t.get("name", "") for t in proj.get("teams", [])]
            if team_name in teams or not teams:
                return proj["id"]
    return None


def find_existing_issue(title: str, project_id: str, dry_run: bool) -> Optional[str]:
    """Return the Linear identifier (e.g. MCS-42) of an existing issue with this title."""
    if dry_run:
        return None
    data = mcp_call("list_issues", {"project": project_id, "limit": 250})
    for issue in data.get("issues", []):
        if issue.get("title", "").strip().lower() == title.strip().lower():
            return issue.get("identifier") or issue.get("id")
    return None


# ---------------------------------------------------------------------------
# Creation helpers
# ---------------------------------------------------------------------------

def ensure_initiative(
    name: str,
    description: str,
    target_date: Optional[str],
    owner_id: Optional[str],
    run_log: RunLog,
    dry_run: bool,
) -> Optional[str]:
    """Create or update the Initiative. Returns its ID."""
    log_key = f"initiative:{name}"
    existing_id = run_log.get(log_key) or find_existing_initiative(name, dry_run)

    args: dict = {
        "name": name,
        "description": description,
        "status": "Active",
    }
    if target_date:
        args["targetDate"] = target_date
    if owner_id:
        args["owner"] = owner_id
    if existing_id:
        args["id"] = existing_id
        action = "Updated"
    else:
        action = "Created"

    result = mcp_call("save_initiative", args, dry_run=dry_run)
    if dry_run:
        print(f"    → Would {action.lower()} Initiative: '{name}'")
        return None

    initiative_id = (result or {}).get("id") or existing_id
    if initiative_id:
        run_log.set(log_key, initiative_id)
        print(f"  ✓ {action} Initiative: '{name}' ({initiative_id})")
    return initiative_id


def ensure_project(
    name: str,
    team_name: str,
    initiative_name: str,
    target_date: Optional[str],
    lead_id: Optional[str],
    run_log: RunLog,
    dry_run: bool,
) -> Optional[str]:
    """Create or update a Project. Returns its ID."""
    log_key = f"project:{name}"
    existing_id = run_log.get(log_key) or find_existing_project(name, team_name, dry_run)

    args: dict = {
        "name": name,
        "addTeams": [team_name],
    }
    if initiative_name:
        args["addInitiatives"] = [initiative_name]
    if target_date:
        args["targetDate"] = target_date
    if lead_id:
        args["lead"] = lead_id
    if existing_id:
        args["id"] = existing_id
        action = "Updated"
    else:
        action = "Created"

    result = mcp_call("save_project", args, dry_run=dry_run)
    if dry_run:
        print(f"    → Would {action.lower()} Project: '{name}' (target: {target_date or 'none'})")
        return None

    project_id = (result or {}).get("id") or existing_id
    if project_id:
        run_log.set(log_key, project_id)
        print(f"  ✓ {action} Project: '{name}' ({project_id})")
    return project_id


def ensure_issue(
    task: dict,
    project_id: str,
    project_name: str,
    team_name: str,
    run_log: RunLog,
    dry_run: bool,
) -> Optional[str]:
    """Create or update an Issue. Returns its Linear identifier (e.g. MCS-42)."""
    log_key = f"issue:{task['task_id']}"
    existing_id = run_log.get(log_key) or find_existing_issue(task["issue_title"], project_id, dry_run)

    args: dict = {
        "title": task["issue_title"],
        "team": team_name,
        "project": project_name,
        "description": task["issue_body"],
    }

    # Assignee
    if task.get("owner_id"):
        args["assignee"] = task["owner_id"]
    elif task.get("owner_raw"):
        args["assignee"] = task["owner_raw"]  # fallback to raw name/email

    # Estimate
    if task.get("estimate_points") is not None:
        args["estimate"] = task["estimate_points"]

    # Due date
    if task.get("end_date_raw"):
        args["dueDate"] = task["end_date_raw"]

    # Status
    if task.get("status_id"):
        args["state"] = task["status_id"]
    elif task.get("status_name"):
        args["state"] = task["status_name"]

    # MoSCoW label
    if task.get("moscow"):
        args["labelNames"] = [task["moscow"]]

    # Cycle
    if task.get("cycle_id"):
        args["cycle"] = task["cycle_id"]

    if existing_id:
        args["id"] = existing_id
        action = "Updated"
    else:
        action = "Created"

    result = mcp_call("save_issue", args, dry_run=dry_run)
    if dry_run:
        print(f"    → Would {action.lower()} Issue: '{task['issue_title']}' "
              f"(assignee: {task.get('owner_raw', 'none')}, "
              f"estimate: {task.get('estimate_label', 'none')})")
        return None

    issue_id = (result or {}).get("identifier") or (result or {}).get("id") or existing_id
    if issue_id:
        run_log.set(log_key, issue_id)
        print(f"  ✓ {action} Issue: '{task['issue_title']}' ({issue_id})")
    return issue_id


def wire_dependencies(
    tasks: list[dict],
    run_log: RunLog,
    dry_run: bool,
) -> None:
    """
    Wire blockedBy relations for all tasks that have dependency_ids.
    Must be called after all issues have been created (so IDs are known).
    """
    wired = 0
    skipped = 0

    for task in tasks:
        if not task.get("dependency_ids"):
            continue

        blocker_issue_ids = []
        for dep_task_id in task["dependency_ids"]:
            blocker_linear_id = run_log.get(f"issue:{dep_task_id}")
            if blocker_linear_id:
                blocker_issue_ids.append(blocker_linear_id)
            else:
                print(f"  ⚠ Dependency {dep_task_id} for {task['task_id']} not found in run log — skipping")
                skipped += 1

        if not blocker_issue_ids:
            continue

        this_issue_id = run_log.get(f"issue:{task['task_id']}")
        if not this_issue_id:
            print(f"  ⚠ Issue {task['task_id']} not found in run log — cannot wire dependencies")
            skipped += 1
            continue

        args = {
            "id": this_issue_id,
            "blockedBy": blocker_issue_ids,
        }

        if dry_run:
            print(f"    → Would wire: {task['task_id']} ({this_issue_id}) "
                  f"blockedBy {task['dependency_ids']} ({blocker_issue_ids})")
        else:
            mcp_call("save_issue", args, dry_run=False)
            print(f"  ✓ Wired: {task['task_id']} blockedBy {', '.join(task['dependency_ids'])}")
        wired += 1

    if not dry_run:
        print(f"  Dependencies: {wired} wired, {skipped} skipped.")


# ---------------------------------------------------------------------------
# Execution report
# ---------------------------------------------------------------------------

def build_execution_report(
    tasks: list[dict],
    run_log: RunLog,
    initiative_name: str,
    dry_run: bool,
    start_time: datetime,
) -> str:
    elapsed = (datetime.now() - start_time).total_seconds()
    mode = "DRY RUN" if dry_run else "EXECUTED"
    lines = [
        "# Spreadsheet-to-Linear: Phase 2 Execution Report",
        "",
        f"**Mode:** {mode}  ",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Duration:** {elapsed:.1f}s  ",
        f"**Initiative:** {initiative_name}",
        "",
        "---",
        "",
        "## Created / Updated Objects",
        "",
        "| Type | Name | Linear ID |",
        "| :--- | :--- | :--- |",
    ]

    for key, value in run_log.data.items():
        obj_type, name = key.split(":", 1)
        lines.append(f"| {obj_type.capitalize()} | {name} | `{value}` |")

    lines += [
        "",
        "---",
        "",
        "## Task Summary",
        "",
        "| Task ID | Title | Assignee | MoSCoW | Estimate | Dependencies |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for t in tasks:
        deps = ", ".join(t.get("dependency_ids", [])) or "—"
        lines.append(
            f"| {t['task_id']} | {t['task_name'][:40]} | "
            f"{t.get('owner_raw', '—')} | {t.get('moscow', '—')} | "
            f"{t.get('estimate_label', '—')} | {deps} |"
        )

    if dry_run:
        lines += [
            "",
            "> **This was a dry run.** No changes were made to Linear.",
            "> Re-run without `--dry-run` to execute.",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Phase 2: Create Linear artifacts from resolved task data."
    )
    parser.add_argument("--tasks", default="./output/resolved_tasks.json",
                        help="Path to resolved_tasks.json from Phase 1")
    parser.add_argument("--config", default="./output/skill_config.json",
                        help="Path to skill_config.json from Phase 0")
    parser.add_argument("--initiative", default="",
                        help="Initiative name (overrides config value)")
    parser.add_argument("--output-dir", default="./output",
                        help="Directory for output files and run log")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print planned API calls without executing them")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Seconds to wait between API calls (default: 0.5)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = datetime.now()
    mode_label = "DRY RUN" if args.dry_run else "EXECUTION"
    print(f"\nPhase 2: {mode_label} — Creating Linear artifacts...")

    # Load config and tasks
    if not Path(args.config).exists():
        print(f"ERROR: Config not found: {args.config}", file=sys.stderr)
        sys.exit(1)
    if not Path(args.tasks).exists():
        print(f"ERROR: Tasks file not found: {args.tasks}", file=sys.stderr)
        sys.exit(1)

    config = SkillConfig.load(args.config)
    with open(args.tasks) as f:
        tasks: list[dict] = json.load(f)

    initiative_name = args.initiative or config.initiative_name
    if not initiative_name:
        print("ERROR: No initiative name provided. Use --initiative or set it in preflight.", file=sys.stderr)
        sys.exit(1)

    print(f"  Team:       {config.team.name}")
    print(f"  Initiative: {initiative_name}")
    print(f"  Tasks:      {len(tasks)}")
    print(f"  Dry run:    {args.dry_run}")
    print()

    # Load or create run log
    run_log_path = str(output_dir / "run_log.json")
    run_log = RunLog(run_log_path)

    # -----------------------------------------------------------------------
    # Step 1: Create Initiative
    # -----------------------------------------------------------------------
    print("Step 1: Initiative")

    # Derive target date from latest task due date
    all_dates = [t["end_date_raw"] for t in tasks if t.get("end_date_raw")]
    initiative_target = max(all_dates) if all_dates else None

    # Use first task owner as initiative owner if not set
    first_owner_id = next((t["owner_id"] for t in tasks if t.get("owner_id")), None)

    initiative_id = ensure_initiative(
        name=initiative_name,
        description=f"Auto-created by spreadsheet-to-linear skill on {start_time.strftime('%Y-%m-%d')}.",
        target_date=initiative_target,
        owner_id=first_owner_id,
        run_log=run_log,
        dry_run=args.dry_run,
    )
    if not args.dry_run:
        time.sleep(args.delay)

    # -----------------------------------------------------------------------
    # Step 2: Create Projects (one per unique sub-project)
    # -----------------------------------------------------------------------
    print("\nStep 2: Projects")

    subprojects: dict[str, list[dict]] = {}
    for task in tasks:
        subprojects.setdefault(task["subproject"], []).append(task)

    project_ids: dict[str, str] = {}  # subproject_name → project_id

    for sp_name, sp_tasks in subprojects.items():
        sp_dates = [t["end_date_raw"] for t in sp_tasks if t.get("end_date_raw")]
        sp_target = max(sp_dates) if sp_dates else None
        sp_lead_id = next((t["owner_id"] for t in sp_tasks if t.get("owner_id")), None)

        project_id = ensure_project(
            name=sp_name,
            team_name=config.team.name,
            initiative_name=initiative_name,
            target_date=sp_target,
            lead_id=sp_lead_id,
            run_log=run_log,
            dry_run=args.dry_run,
        )
        if project_id:
            project_ids[sp_name] = project_id
        if not args.dry_run:
            time.sleep(args.delay)

    # -----------------------------------------------------------------------
    # Step 3: Create Issues
    # -----------------------------------------------------------------------
    print("\nStep 3: Issues")

    for task in tasks:
        sp_name = task["subproject"]
        project_id = project_ids.get(sp_name, sp_name)  # fallback to name if dry-run

        ensure_issue(
            task=task,
            project_id=project_id,
            project_name=sp_name,
            team_name=config.team.name,
            run_log=run_log,
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            time.sleep(args.delay)

    # -----------------------------------------------------------------------
    # Step 4: Wire dependencies
    # -----------------------------------------------------------------------
    print("\nStep 4: Dependencies")

    tasks_with_deps = [t for t in tasks if t.get("dependency_ids")]
    if tasks_with_deps:
        wire_dependencies(tasks, run_log, dry_run=args.dry_run)
        if not args.dry_run:
            time.sleep(args.delay)
    else:
        print("  No dependencies to wire.")

    # -----------------------------------------------------------------------
    # Execution report
    # -----------------------------------------------------------------------
    report = build_execution_report(tasks, run_log, initiative_name, args.dry_run, start_time)
    report_path = output_dir / ("dry_run_report.md" if args.dry_run else "execution_report.md")
    report_path.write_text(report, encoding="utf-8")

    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\nPhase 2 {mode_label} complete in {elapsed:.1f}s.")
    print(f"→ Report saved: {report_path}")
    if args.dry_run:
        print("→ Re-run without --dry-run to execute for real.")
    else:
        print(f"→ Run log saved: {run_log_path}")
        print("→ All artifacts created. Open Linear to verify.")


if __name__ == "__main__":
    main()
