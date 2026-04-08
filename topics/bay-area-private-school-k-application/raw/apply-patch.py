#!/usr/bin/env python3
"""Assemble updated research-plan.yaml from part files."""
import os

base = "/Users/weizheng/projects/claude/llm_knowledge/topics/bay-area-private-school-k-application"
raw = os.path.join(base, "raw")

part1 = open(os.path.join(raw, "plan-part1.txt")).read()
part2 = open(os.path.join(raw, "plan-part2.txt")).read()
qg    = open(os.path.join(raw, "qG-patch.yaml")).read()

combined = part1.rstrip("\n") + "\n\n" + part2.rstrip("\n") + "\n\n" + qg.rstrip("\n") + "\n"

out_path = os.path.join(base, "research-plan.yaml")
with open(out_path, "w") as f:
    f.write(combined)

lines = combined.splitlines()
print(f"Written: {len(lines)} lines to {out_path}")

# Spot checks
checks = [
    "status: gap_fill_complete",
    "searches_used: 83",
    "fetches_used: 96",
    "guidebook_pass_completed_at: '2026-04-07'",
    "- id: qG001",
    "- id: qG020",
    "answered_at: '2026-04-07'",
]
for check in checks:
    found = any(check in line for line in lines)
    print(f"{'OK' if found else 'MISSING'}: {check}")
