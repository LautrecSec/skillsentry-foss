# SPDX-License-Identifier: Apache-2.0
"""Check inherited files against the recorded upstream snapshot, without network access."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath


def digest(data: bytes) -> str:
    """Normalize UTF-8 text line endings so Git checkouts remain comparable."""
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        pass
    else:
        if b"\0" not in data:
            data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def verify(root: Path) -> dict[str, object]:
    root = root.resolve()
    manifest = json.loads((root / "upstream-manifest.json").read_text(encoding="utf-8"))
    changes = json.loads((root / "fork-changes.json").read_text(encoding="utf-8"))
    files = manifest["files"]
    failures = []
    unchanged = 0
    for name in changes:
        if name not in files or name.startswith("src/skillspector/"):
            failures.append(f"Invalid change exception: {name}")
    for name, expected in files.items():
        relative = PurePosixPath(name)
        path = root.joinpath(*relative.parts)
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or "\\" in name
            or ":" in name
            or not path.resolve().is_relative_to(root)
        ):
            failures.append(f"Unsafe manifest path: {name}")
            continue
        change = changes.get(name)
        if change:
            if not isinstance(change, dict) or not change.get("reason"):
                failures.append(f"Missing change reason: {name}")
                continue
            replacement = change.get("preserved_as")
            if replacement:
                archived = root / replacement
                if not archived.resolve().is_relative_to(root):
                    failures.append(f"Unsafe archive path: {name}")
                elif not archived.is_file() or digest(archived.read_bytes()) != expected:
                    failures.append(f"Archived upstream file differs: {name}")
            continue
        if not path.is_file() or digest(path.read_bytes()) != expected:
            failures.append(f"Inherited file missing or changed: {name}")
        else:
            unchanged += 1
    return {
        "upstream_commit": manifest["commit"],
        "inherited_files": len(files),
        "unchanged_files": unchanged,
        "documented_changes": len(changes),
        "failures": failures,
    }


def main() -> None:
    result = verify(Path(__file__).resolve().parents[1])
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result["failures"] else 0)


if __name__ == "__main__":
    main()
