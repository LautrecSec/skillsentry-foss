# SPDX-License-Identifier: Apache-2.0
"""The snapshot check must detect missing and modified inherited code."""

import json
from pathlib import Path

import pytest

from scripts.verify_upstream import digest, verify


def snapshot(tmp_path, name="engine.py", data=b"original\n", changes=None):
    (tmp_path / "upstream-manifest.json").write_text(
        json.dumps({"commit": "test", "files": {name: digest(data)}}), encoding="utf-8"
    )
    (tmp_path / "fork-changes.json").write_text(json.dumps(changes or {}), encoding="utf-8")
    return tmp_path


def test_real_snapshot():
    assert verify(Path(__file__).resolve().parents[2])["failures"] == []


def test_line_endings():
    assert digest(b"source\r\n") == digest(b"source\n")
    assert digest(b"\x00\r\n") != digest(b"\x00\n")


@pytest.mark.parametrize("content", [None, "changed\n"])
def test_missing_and_changed_files_fail(tmp_path, content):
    snapshot(tmp_path)
    if content is not None:
        (tmp_path / "engine.py").write_text(content, encoding="utf-8")
    assert verify(tmp_path)["failures"]


def test_documented_change_requires_reason(tmp_path):
    snapshot(tmp_path, changes={"engine.py": {"reason": "Fork packaging"}})
    assert verify(tmp_path)["failures"] == []
    (tmp_path / "fork-changes.json").write_text('{"engine.py": {"reason": ""}}')
    assert verify(tmp_path)["failures"]


def test_engine_cannot_be_exempted(tmp_path):
    snapshot(
        tmp_path,
        "src/skillspector/core.py",
        changes={"src/skillspector/core.py": {"reason": "Bypass"}},
    )
    assert verify(tmp_path)["failures"]


def test_path_escape_is_rejected(tmp_path):
    snapshot(tmp_path, "../outside.py")
    assert verify(tmp_path)["failures"] == ["Unsafe manifest path: ../outside.py"]


def test_archived_original_is_checked(tmp_path):
    snapshot(tmp_path, changes={"engine.py": {"reason": "Replaced", "preserved_as": "original.py"}})
    assert verify(tmp_path)["failures"]
    (tmp_path / "original.py").write_text("original\n", encoding="utf-8")
    assert verify(tmp_path)["failures"] == []
