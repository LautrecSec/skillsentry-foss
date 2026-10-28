# Validation evidence

Validation date: **2026-10-28**. Fork version: `2.12.0+skillsentry.1`.
Pinned upstream: `e7172462caf367736645f66c1aa154ca5f9c64dc`.

The results below are observations from this workspace. A preserved source file,
registered provider, or inherited test is not presented as a runtime result.

## Confirmed checks

| Check | Observed result |
| --- | --- |
| Upstream revision | GitHub's current main commit matched the clean local checkout |
| Source snapshot | 467 inherited files, 453 unchanged, 14 documented project-level changes; no verifier failures |
| Engine preservation | All 129 files under `src/skillspector/` matched pinned upstream Git blob bytes exactly after LF normalization; engine exceptions are rejected by the verifier |
| Analyzer import | All 27 discovered analyzer nodes registered without import errors |
| Rule catalog | 89 entries enumerated from the central rule/category mapping |
| Focused fork and workflow tests, Windows Python 3.12.14 | 26 passed (21 fork checks and 5 inherited workflow checks) |
| Fork lint and formatting | Ruff check and format check passed for the new source, tests, and scripts |
| Benign directory fixture | 0 findings, score 0, LOW, SAFE, exit 0 |
| Suspicious directory fixture | 3 findings, score 62, HIGH, DO_NOT_INSTALL, exit 1 |
| Compatibility comparison | Both CLIs matched findings, locations, risk assessment, and exit status on both fixtures |
| Inference opt-in | Static demo reports had `llm_requested=false` and empty inference usage |
| Output formats | Terminal, JSON, Markdown, and SARIF generated; SARIF passed the inherited structural validator |
| Other local inputs | Single-file, ZIP, and recursive scans completed; recursive scan contained both examples |
| MCP stdio | Actual initialization, tool listing, and `scan_skill` call succeeded; benign input scored 0 in static-only mode |
| OpenCode tests, Ubuntu and Node 22.20.0 | 56 passed, 0 failed |
| Pi tests, Ubuntu and Node 22.20.0 | 37 passed, 0 failed |
| Package build | Wheel and source archive built with `python -m build --no-isolation` |
| Distribution metadata | Both distributions passed `twine check` |
| Distribution contents | Wheel contained both Python packages and LICENSE, NOTICE, THIRD_PARTY_NOTICES.md; source archive excluded local caches and generated artifacts |
| Built-wheel import and scan | Wheel installed into a separate target directory, imported from that directory, and scanned the benign fixture successfully |

The wheel check reused dependencies from the development environment. It checks
the built package contents and entry point; it is not an installation test on
a clean operating system. The SARIF validator checks the inherited structural
schema, not every semantic requirement of the complete SARIF specification.

## Ubuntu non-live Python suite

The full credential-free selection ran on Ubuntu's native filesystem with
Python 3.12.16. It completed in 18 minutes 44 seconds with:

- **15,623 passed**.
- **6 failed**, subsequently corrected and retested as described below.
- **35 skipped** and **4 expected failures**.
- **250 deselected** by the integration/provider marker policy.
- **7 warnings**, including an inherited unregistered timeout marker and a
  deliberately duplicated ZIP member.

Five failures came from inherited release-workflow contract tests still reading
the old active workflow path. Their fixture path now points to the preserved
upstream workflow archive. The test logic is retained, and its modified file
and archived original are documented in the provenance records.

The sixth failure compared LF-normalized scanner text with raw CRLF bytes in
an OMS fixture copied from the Windows checkout. The new repository's text
files were normalized to its committed LF policy. No engine logic changed;
all 129 inherited engine files now match upstream Git blobs byte for byte.

The final targeted Ubuntu run passed **62 tests, with zero failures or errors**:
all 21 fork checks, all 5 archived-workflow checks, and all 36 OMS cases.
Every failure from the full run was covered by this successful follow-up.
The entire 15,668-case selection was not rerun after these corrections, so this
document does not claim a single final full-suite green run.

The local evidence files are `artifacts/linux-pytest.xml`,
`artifacts/linux-pytest.log`, `artifacts/linux-retest.xml`, and
`artifacts/linux-retest.log`. These are ignored validation artifacts.

## Windows suite observations

An initial broad diagnostic invocation of the inherited non-live suite stopped
after ten issues: **6,283 passed, 4 failed, 6 errors, 250 deselected**. It ran
during setup, before the provenance manifest was finalized. The final focused
fork and archived-workflow checks subsequently passed all 26 tests. The broad Windows invocation is
not a complete Windows compatibility result, and its failures are not all
attributed to upstream defects.

The inherited extension tests also did not pass on Windows with Node 24.22.1:
OpenCode reported 51 passed and 5 failed; Pi reported 26 passed, 10 failed, and
1 skipped. The failure logs include expectations about directory enumeration
order. The same suites passed on Ubuntu with the upstream Node version.
The active fork CI runs these extension suites on Linux.

The engine's secure `--output` writer intentionally rejects Windows because
the required POSIX descriptor and no-follow operations are unavailable. This
protection is preserved. The Windows guide uses stdout redirection into a
trusted directory. Full Windows engine compatibility is not claimed.

## Reproduce the checks

From the repository root:

```bash
uv sync --locked --all-extras
uv run --no-sync python scripts/verify_upstream.py
uv run --no-sync pytest tests/fork -q -p no:cacheprovider
uv run --no-sync python scripts/demo.py
uv run --no-sync ruff check src/skillsentry_foss tests/fork scripts/verify_upstream.py scripts/demo.py
uv run --no-sync ruff format --check src/skillsentry_foss tests/fork scripts/verify_upstream.py scripts/demo.py
uv run --no-sync python -m build --no-isolation
uv run --no-sync python -m twine check dist/*
```

On Linux with Python 3.12 and Node 22.20.0:

```bash
uv run --no-sync pytest -m 'not integration and not provider' tests --tb=short
node --test tests/opencode/skillspector_scan_lib.test.ts
node --test tests/unit/test_pi_extension.mjs
```

The demo writes ignored artifacts under `artifacts/`. This workspace also has
ignored validation logs. They are local evidence and are excluded from source
archives, container contexts, and Git publication.

## Scope limits

- No hosted-provider or local-model inference endpoint was exercised.
- Provider and integration markers were excluded from credential-free tests.
- No detection-accuracy, false-positive-rate, or model-equivalence benchmark was performed.
- Live Git/file-URL retrieval, transitive networking, OSV advisories, MCP Registry
  endpoints, and LangGraph Studio were not independently exercised against their
  live services. Their implementations and tests are retained.
- MCP stdio was exercised; HTTP transport was not started for an end-to-end test.
- The Docker engine was unavailable, so the image was not built or run here.
- Python 3.13, Python 3.14, and macOS were not exercised.
- GitHub repository destination: [LautrecSec/skillsentry-foss](https://github.com/LautrecSec/skillsentry-foss).
  GitHub Actions results are separate from the local validation evidence above.
- No GitHub release, private reporting channel, or PyPI package was published or configured.
- No trademark availability assessment was performed for the working project name.

Source and interface parity apply to the pinned upstream commit. They do not
establish a guarantee of safe installation, runtime containment, complete
coverage, or future compatibility.
