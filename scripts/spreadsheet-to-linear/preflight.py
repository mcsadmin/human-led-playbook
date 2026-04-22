"""
preflight.py
============
Phase 0 of the spreadsheet-to-linear skill.

Queries the live Linear workspace to produce:
  1. A human-readable Markdown readiness report (preflight_report.md)
  2. A machine-readable config JSON (skill_config.json) consumed by Phase 1

Usage
-----
    python3 preflight.py [--team "MCS Shared"] [--initiative "My Project"] \
                         [--scale tshirt] [--output-dir ./output]

The script uses the Linear MCP via manus-mcp-cli. It does not require a
Linear API key directly — authentication is handled by the MCP server.
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Ensure sibling scripts are importable when run directly
sys.path.insert(0, str(Path(__file__).parent))
from config_schema import (
    SkillConfig, LinearMember, LinearLabel, LinearCycle, LinearTeam, LinearStatus,
    MOSCOW_LABEL_GROUP, DEFAULT_ESTIMATE_SCALE,
)
from estimate_conversion import describe_scale, SCALES


# ---------------------------------------------------------------------------
# MCP helper
# ---------------------------------------------------------------------------

def mcp_call(tool: str, args: dict) -> dict | list:
    """
    Call a Linear MCP tool via manus-mcp-cli and return the parsed JSON result.
    Raises RuntimeError on failure.
    """
    cmd = [
        "manus-mcp-cli", "tool", "call", tool,
        "--server", "linear",
        "--input", json.dumps(args),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # manus-mcp-cli writes "Tool execution result:\n<json>" to stdout
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
# Data fetchers
# ---------------------------------------------------------------------------

def fetch_teams() -> list[LinearTeam]:
    data = mcp_call("list_teams", {})
    return [
        LinearTeam(id=t["id"], name=t["name"], key=t.get("key") or t.get("identifier") or "")
        for t in data.get("teams", [])
    ]


def fetch_members(limit: int = 250) -> list[LinearMember]:
    members = []
    cursor = None
    while True:
        args: dict = {"limit": limit}
        if cursor:
            args["cursor"] = cursor
        data = mcp_call("list_users", args)
        batch = data.get("users", [])
        for u in batch:
            if u.get("isActive") and not u.get("isGuest"):
                members.append(LinearMember(
                    id=u["id"],
                    name=u.get("name", ""),
                    email=u.get("email", ""),
                    display_name=u.get("displayName", ""),
                ))
        if not data.get("hasNextPage"):
            break
        cursor = data.get("cursor")
    return members


def fetch_labels() -> list[LinearLabel]:
    data = mcp_call("list_issue_labels", {})
    labels = []
    for l in data.get("labels", []):
        labels.append(LinearLabel(
            id=l["id"],
            name=l["name"],
            group=l.get("parent") or "",
        ))
    return labels


def fetch_cycles(team_id: str) -> list[LinearCycle]:
    try:
        data = mcp_call("list_cycles", {"teamId": team_id})
        cycles = []
        for c in (data if isinstance(data, list) else data.get("cycles", [])):
            cycles.append(LinearCycle(
                id=c["id"],
                name=c.get("name", f"Cycle {c.get('number', '')}").strip(),
                starts_at=c.get("startsAt", ""),
                ends_at=c.get("endsAt", ""),
            ))
        return cycles
    except Exception:
        return []


def fetch_statuses(team_name: str) -> list[LinearStatus]:
    data = mcp_call("list_issue_statuses", {"team": team_name})
    statuses = []
    for s in (data if isinstance(data, list) else data.get("statuses", [])):
        statuses.append(LinearStatus(
            id=s["id"],
            name=s["name"],
            type=s.get("type", ""),
        ))
    return statuses


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(config: SkillConfig, scale_name: str) -> str:
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines += [
        "# Spreadsheet-to-Linear: Phase 0 Preflight Report",
        "",
        f"**Generated:** {now}  ",
        f"**Team:** {config.team.name} (`{config.team.key}`)  ",
        f"**Initiative:** {config.initiative_name or '*(not set — will be created)*'}  ",
        f"**Estimate Scale:** {scale_name}",
        "",
        "---",
        "",
        "## 1. Team Members",
        "",
        "Use the **exact Name or Email** values below in the `Owner (R)` and `Accountable (A)` columns of your spreadsheet.",
        "",
        "| Name | Email | Display Name |",
        "| :--- | :--- | :--- |",
    ]
    for m in sorted(config.members, key=lambda x: x.name.lower()):
        lines.append(f"| {m.name} | {m.email} | {m.display_name} |")

    lines += [
        "",
        "---",
        "",
        "## 2. Available Labels",
        "",
        "Use the **exact Label Name** values below in the `MoSCoW` and other label columns.",
        "",
        "| Group | Label Name |",
        "| :--- | :--- |",
    ]
    groups: dict[str, list[str]] = {}
    for l in config.labels:
        groups.setdefault(l.group or "Ungrouped", []).append(l.name)
    for group in sorted(groups.keys()):
        for name in sorted(groups[group]):
            lines.append(f"| {group} | {name} |")

    # MoSCoW group check
    moscow_labels = [l for l in config.labels if l.group == MOSCOW_LABEL_GROUP]
    if not moscow_labels:
        lines += [
            "",
            "> ⚠️ **No 'MoSCoW' label group found.** To enable MoSCoW classification,",
            "> create a label group named `MoSCoW` in Linear with labels: Must, Should, Could, Won't.",
        ]

    lines += [
        "",
        "---",
        "",
        "## 3. Cycles (Sprints)",
        "",
    ]
    if config.cycles:
        lines += [
            "Use the **exact Cycle Name** values below in the `Sprint` column of your spreadsheet.",
            "",
            "| Cycle Name | Starts | Ends |",
            "| :--- | :--- | :--- |",
        ]
        for c in config.cycles:
            lines.append(f"| {c.name} | {c.starts_at[:10] if c.starts_at else '—'} | {c.ends_at[:10] if c.ends_at else '—'} |")
    else:
        lines += [
            "> ⚠️ **No Cycles are configured for this team.**",
            ">",
            "> Cycles are required to assign Issues to Sprints. To set them up:",
            "> 1. Go to **Linear → Settings → Teams → MCS Shared → Cycles**.",
            "> 2. Set a cycle duration (e.g., 2 weeks) and a start day.",
            "> 3. Linear will auto-generate upcoming cycles.",
            "> 4. Re-run this preflight check to see the cycle names.",
            ">",
            "> Until Cycles are configured, leave the `Sprint` column blank in your spreadsheet.",
        ]

    lines += [
        "",
        "---",
        "",
        "## 4. Estimate Conversion Matrix",
        "",
        "Estimated hours from your spreadsheet will be automatically converted to",
        f"Linear estimate points using the **{scale_name}** scale:",
        "",
        "```",
        describe_scale(scale_name),
        "```",
        "",
        "---",
        "",
        "## 5. Workflow States",
        "",
        "| State Name | Type |",
        "| :--- | :--- |",
    ]
    for s in config.statuses:
        lines.append(f"| {s.name} | {s.type} |")

    lines += [
        "",
        "---",
        "",
        "## Next Steps",
        "",
        "1. Build your task register spreadsheet using the names and values above.",
        "2. Ensure the spreadsheet includes the three coaching columns: **Context / Why**, **Task Breakdown**, and **Acceptance Criteria**.",
        "3. Run **Phase 1** (`parse_spreadsheet.py`) to generate the review document.",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Phase 0: Preflight readiness check for spreadsheet-to-linear skill.")
    parser.add_argument("--team", default="", help="Linear team name (default: first team found)")
    parser.add_argument("--initiative", default="", help="Initiative name for this project")
    parser.add_argument("--scale", default=DEFAULT_ESTIMATE_SCALE,
                        choices=list(SCALES.keys()), help="Estimate scale to use")
    parser.add_argument("--output-dir", default="./output", help="Directory for output files")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Phase 0: Preflight — querying Linear workspace...")

    # 1. Resolve team
    print("  → Fetching teams...")
    teams = fetch_teams()
    if not teams:
        print("ERROR: No teams found in Linear workspace.", file=sys.stderr)
        sys.exit(1)
    team = next((t for t in teams if t.name.lower() == args.team.lower()), teams[0])
    if args.team and team.name.lower() != args.team.lower():
        print(f"  ⚠ Team '{args.team}' not found. Using '{team.name}'.")
    print(f"  ✓ Team: {team.name} ({team.key})")

    # 2. Fetch workspace data
    print("  → Fetching members...")
    members = fetch_members()
    print(f"  ✓ {len(members)} active members found.")

    print("  → Fetching labels...")
    labels = fetch_labels()
    print(f"  ✓ {len(labels)} labels found.")

    print("  → Fetching cycles...")
    cycles = fetch_cycles(team.id)
    if cycles:
        print(f"  ✓ {len(cycles)} cycles found.")
    else:
        print("  ⚠ No cycles configured — see report for setup instructions.")

    print("  → Fetching workflow statuses...")
    statuses = fetch_statuses(team.name)
    print(f"  ✓ {len(statuses)} workflow states found.")

    # 3. Build config
    config = SkillConfig(
        team=team,
        members=members,
        labels=labels,
        cycles=cycles,
        statuses=statuses,
        estimate_scale=args.scale,
        initiative_name=args.initiative,
    )

    # 4. Save config JSON
    config_path = output_dir / "skill_config.json"
    config.save(str(config_path))
    print(f"\n  ✓ Config saved: {config_path}")

    # 5. Generate and save report
    report = build_report(config, args.scale)
    report_path = output_dir / "preflight_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"  ✓ Preflight report saved: {report_path}")

    print("\nPhase 0 complete. Review the preflight report before building your spreadsheet.")


if __name__ == "__main__":
    main()
