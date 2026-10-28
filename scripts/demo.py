# SPDX-License-Identifier: Apache-2.0
"""Exercise the inherited engine through both CLIs using inert local fixtures."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

from skillspector.sarif_models import validate_sarif_report

ROOT = Path(__file__).resolve().parents[1]


def scan(target: str, output_format: str = "json", *, upstream: bool = False, extra=()):
    executable = Path(sys.executable).with_name(
        "skillspector.exe" if os.name == "nt" else "skillspector"
    )
    command = [str(executable)] if upstream else [sys.executable, "-m", "skillsentry_foss"]
    command += ["scan", target, "--no-llm", "--format", output_format, *extra]
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        timeout=120,
        env={**os.environ, "LANGCHAIN_TRACING_V2": "false", "LANGSMITH_TRACING": "false"},
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(
            f"Scan failed ({result.returncode}): {result.stderr.decode('utf-8', errors='replace')}"
        )
    return result.stdout, result.returncode


def signature(report):
    """Ignore timestamps and per-run finding IDs when comparing equivalent scans."""
    return sorted(
        (issue["id"], issue["severity"], json.dumps(issue["location"], sort_keys=True))
        for issue in report["issues"]
    )


def main() -> None:
    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)
    summary = {}
    for name in ("benign", "suspicious"):
        body, exit_code = scan(f"examples/{name}")
        report = json.loads(body)
        original_body, original_exit = scan(f"examples/{name}", upstream=True)
        original = json.loads(original_body)
        assert signature(report) == signature(original), f"Finding mismatch: {name}"
        assert report["risk_assessment"] == original["risk_assessment"], name
        assert exit_code == original_exit, name
        assert report["metadata"]["llm_requested"] is False
        assert report["metadata"]["inference_usage"] == []
        (artifacts / f"{name}.json").write_bytes(body)
        summary[name] = {
            "exit_code": exit_code,
            "issues": len(report["issues"]),
            "risk_assessment": report["risk_assessment"],
            "upstream_cli_matches": True,
        }
    assert summary["benign"]["issues"] == 0
    assert summary["suspicious"]["issues"] > 0
    assert summary["suspicious"]["exit_code"] == 1
    for output_format, extension in (("terminal", "txt"), ("markdown", "md"), ("sarif", "sarif")):
        body, _ = scan("examples/suspicious", output_format)
        assert body.strip(), output_format
        (artifacts / f"suspicious.{extension}").write_bytes(body)
        if output_format == "sarif":
            validate_sarif_report(json.loads(body))
    single, _ = scan("examples/suspicious/SKILL.md")
    assert json.loads(single)["issues"]
    archive = artifacts / "example.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.write(ROOT / "examples/benign/SKILL.md", "SKILL.md")
    zipped, _ = scan("artifacts/example.zip")
    assert not json.loads(zipped)["issues"]
    recursive, _ = scan("examples", extra=("--recursive",))
    (artifacts / "recursive.json").write_bytes(recursive)
    collection = json.loads(recursive)
    assert collection["skill_count"] == 2
    assert collection["execution_successful"] is True
    assert {skill["path"] for skill in collection["skills"]} == {"benign", "suspicious"}
    summary["checks"] = [
        "Both CLIs agree on findings, risk, and exits for both fixtures",
        "Static reports request no LLM and record no inference usage",
        "Terminal, JSON, Markdown, and schema-validated SARIF output",
        "Directory, single-file, ZIP, and recursive input",
    ]
    (artifacts / "demo-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
