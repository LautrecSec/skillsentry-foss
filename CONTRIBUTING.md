# Contributing to SkillSentry FOSS

Fork modification notice: this policy replaces the upstream contribution guide.
The original is retained in [CONTRIBUTING.upstream.md](CONTRIBUTING.upstream.md).

This repository is an attributed fork of NVIDIA SkillSpector. Keep inherited
source attribution and distinguish fork changes from upstream functionality.

## Local setup and checks

Use Python 3.12 or another version supported by pyproject.toml.

```bash
uv sync --locked --all-extras
uv run --no-sync python scripts/verify_upstream.py
uv run --no-sync pytest tests/fork -q
uv run --no-sync python scripts/demo.py
uv run --no-sync ruff check src/skillsentry_foss tests/fork scripts/verify_upstream.py scripts/demo.py
uv run --no-sync ruff format --check src/skillsentry_foss tests/fork scripts/verify_upstream.py scripts/demo.py
```

On Linux, also run the inherited non-live suite:

```bash
uv run --no-sync pytest -m 'not integration and not provider' tests --tb=short
```

The TypeScript and JavaScript extension tests use Node 22.20.0 or a compatible
newer runtime:

```bash
node --test tests/opencode/skillspector_scan_lib.test.ts
node --test tests/unit/test_pi_extension.mjs
```

Build and check distributions with `python -m build --no-isolation` and
`python -m twine check dist/*` inside the development environment. Do not run
live provider tests with other people's credentials or publish test data.

## Change scope

Keep the upstream engine unchanged unless the contribution explicitly requires
an engine change. A deliberate engine change requires a reviewed update to the
provenance policy, focused security regression tests, the feature matrix, and
validation notes. The current verifier deliberately refuses engine exemptions.
Do not silently disable that check to get CI passing.

Prefer a small change at the shared implementation point. Preserve input
validation, resource limits, secure output, incomplete-analysis diagnostics,
and existing finding retention. Add a regression test for non-trivial behavior.

A pull request should state the concrete problem, resulting behavior, checks
run, remaining limitations, and any new data egress. Never include API keys,
private skill content, employer material, or identifiable scan results without
authorization. Intentional test attack strings belong in labeled fixtures.

## Attribution and reports

Do not reassign NVIDIA copyright headers to yourself. Keep LICENSE, NOTICE,
and THIRD_PARTY_NOTICES.md. Record changes to inherited files in
`fork-changes.json` and update UPSTREAM.md. New files should use an
`SPDX-License-Identifier: Apache-2.0` comment where the format permits it.

Use [SECURITY.md](SECURITY.md) for sensitive vulnerabilities. Use the fork's
issue tracker for fork bugs after publication. The upstream NVIDIA tracker is
not this fork's support channel.
