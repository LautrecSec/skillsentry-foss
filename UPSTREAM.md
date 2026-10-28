# Upstream provenance and fork changes

## Pinned source

| Field | Value |
| --- | --- |
| Repository | [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) |
| Version | 2.12.0 |
| Commit | [`e7172462caf367736645f66c1aa154ca5f9c64dc`](https://github.com/NVIDIA/SkillSpector/commit/e7172462caf367736645f66c1aa154ca5f9c64dc) |
| Commit date | 2026-10-27 |
| Upstream main checked | 2026-10-28, matched local checkout |
| Upstream tracked files | 467 |
| License | Apache-2.0, preserved in `LICENSE` |
| Fork distribution version | `2.12.0+skillsentry.1` |

This folder was made from the tracked files of the clean local upstream
checkout. It excludes that checkout's `.git` directory, any credentials,
untracked files, and development environments. It is an independent source
snapshot, not a GitHub-registered fork and not a copy of upstream Git history.

## Attribution and identity

NVIDIA and upstream contributors authored the inherited scanner, analyzers,
rules, providers, integrations, and original tests. Their source headers,
license, and third-party notices are retained. New code is Apache-2.0 as well.

The fork contributes the `skillsentry_foss` entry point, provenance verifier,
fork-specific tests, inert examples, a reproducible demonstration, and fork
documentation and CI. The README links to these source credits and notices. No NVIDIA
endorsement, Verified Skills pipeline access, catalog publication, research
result, model-quality parity, or production deployment is claimed by the fork.

The package name `skillspector` and its imports are retained because upstream
metadata lookups, extensions, and API consumers use them. Reports retain their
original tool and field identities. The new distribution version identifies
the fork. Use a separate venv from any upstream installation.

## Modified inherited files

The machine-readable source of truth is [fork-changes.json](fork-changes.json).
All other inherited files must match [upstream-manifest.json](upstream-manifest.json).

| Path | Modification |
| --- | --- |
| `README.md` | Standalone Skill Sentry usage and project documentation; preserve original manual separately |
| `CONTRIBUTING.md` | Document this fork's contribution and verification process |
| `SECURITY.md` | Separate fork reporting from NVIDIA's upstream security process |
| `pyproject.toml` | Fork description/version, extra executable, license files, wheel package, labeled upstream links |
| `uv.lock` | Change only the local project version; retain external dependency pins |
| `Dockerfile` | Include license notices and use the static-first executable |
| `.env.example` | Explain CLI opt-in and that shell variables must be set explicitly |
| `.gitignore` | Exclude local caches and generated demonstration artifacts |
| `.dockerignore` | Exclude local cache and generated artifacts from the container context |
| `.github/workflows/ci.yml` | Replace upstream CI with independent fork CI |
| Other three upstream workflows | Preserve under `docs/upstream/workflows/`; remove active release, scorecard publishing, and branch mutation jobs |
| `tests/unit/test_github_release_workflow.py` | Point the inherited workflow contract checks at the preserved archive |

Original README, contribution guide, security policy, and workflows are retained
as `*.upstream.md` at the root or under `docs/upstream/workflows/`.
Each modified inherited configuration has a fork modification notice. Replaced
documents carry their own notice. `src/skillspector/` remains unchanged.

## Verify the snapshot

```bash
python scripts/verify_upstream.py
```

The script checks normalized SHA-256 hashes and archived originals. It refuses
change exceptions for inherited engine files. Text normalization permits CRLF/LF
differences across Windows and Linux. It does not normalize other content.
The fork working tree and published Git contents use LF for text. All 129 engine
files were also compared directly with the pinned upstream Git blob bytes.
Its tests check missing files, altered bytes, path traversal, invalid exemptions,
and altered archived documents.

This is a reproducibility aid, not a signed authenticity proof. Compare the
recorded commit against upstream and review changes in your own repository.
The manifest covers the pinned snapshot, not later upstream commits.

## Update procedure

1. Create a branch in this project's Git repository. Keep a clean working tree.
2. Retrieve the desired upstream commit in a separate checkout. Verify its
   license, notices, security changes, dependency lock, and release notes.
3. Compare that commit with the pinned commit using upstream Git history. Review
   engine, schema, CLI, provider, integration, and test changes together.
4. Replace inherited files from that reviewed snapshot. Reapply only documented
   fork packaging, command, and documentation changes. Preserve new upstream
   notices. Do not automatically replace your fork's active workflows.
5. Regenerate normalized hashes for every tracked file in the new upstream
   snapshot, using `scripts.verify_upstream.digest` for the documented algorithm.
   Update the pinned commit/version/date and justified change exceptions.
6. Bump the fork version in both `pyproject.toml` and the root package entry in
   `uv.lock`. Refresh the lock with `uv lock` if dependency metadata changed.
7. Run the verifier, fork tests, inherited non-live suite, extension tests, demo,
   build, distribution checks, and selected live provider checks as appropriate.
8. Update the feature matrix, validation report, and release notes with observed
   results and limitations. Review the diff before merging or publishing.

This source snapshot has no upstream merge ancestry. Adding an `upstream`
remote is useful for comparisons but does not make an ordinary `git merge`
appropriate. Maintain by reviewed snapshot updates, or explicitly migrate to a
history-preserving fork if that becomes useful.

## Authoritative references

- [Pinned upstream README](https://github.com/NVIDIA/SkillSpector/blob/e7172462caf367736645f66c1aa154ca5f9c64dc/README.md)
- [Pinned upstream license](https://github.com/NVIDIA/SkillSpector/blob/e7172462caf367736645f66c1aa154ca5f9c64dc/LICENSE)
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), especially sections 4 and 6
- [Ollama local OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
