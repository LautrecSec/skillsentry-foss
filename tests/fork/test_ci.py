# SPDX-License-Identifier: Apache-2.0
"""Guard the fork's CI permissions and prevent accidental upstream publishing."""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_active_ci_has_read_only_permissions_and_no_credentials():
    source = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    workflow = yaml.load(source, Loader=yaml.BaseLoader)
    assert workflow["permissions"] == {"contents": "read"}
    assert "pull_request_target" not in workflow["on"]
    assert "secrets." not in source
    for job in workflow["jobs"].values():
        assert not any(value == "write" for value in job.get("permissions", {}).values())


def test_ci_actions_are_pinned():
    source = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    refs = re.findall(r"\buses:\s*([^\s#]+)", source)
    assert refs and all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", ref) for ref in refs)


def test_upstream_automation_is_preserved_but_inactive():
    assert {p.name for p in (ROOT / ".github/workflows").glob("*.yml")} == {"ci.yml"}
    for name in ("release.yml", "scorecard.yml", "update-pr-branches.yml"):
        assert (ROOT / "docs/upstream/workflows" / name).is_file()
