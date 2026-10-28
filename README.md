# Skill Sentry

Security scanning for AI agent skills. Inspect a skill before installation,
review its findings, and apply the same checks in an agent workflow or CI.

Maintained by [LautrecSec](https://github.com/LautrecSec).

Skill Sentry uses static analysis by default. No GPU, API key, or paid service
is required for static scans. Local or hosted semantic analysis is available
through an explicit `--llm` option.

## Capabilities

| Area | Included capabilities |
| --- | --- |
| Inputs | Skill directories, Markdown files, ZIP bundles, Git repository URLs, and supported file URLs |
| Static analysis | Pattern matching, Python AST analysis, taint tracking, and YARA rules |
| Threat checks | Prompt injection, data exfiltration, privilege escalation, unsafe code, supply-chain risks, memory poisoning, tool misuse, and MCP-related risks |
| Semantic analysis | Optional model-based analysis through local or hosted providers |
| Reports | Terminal, JSON, Markdown, and SARIF; findings, locations, risk scores, severity, and recommendations |
| Policy | Reviewed baselines, suppression visibility, finding gates, coverage requirements, and incomplete-analysis gates |
| Collections | Recursive skill discovery, optional transitive reference scanning, and a contributed batch scanner |
| Integrations | MCP server, MCP Registry payload scanning and comparison, Python API, Pi, and OpenCode |

See the [feature matrix](docs/fork/FEATURE_PARITY.md) and
[analyzer catalog](docs/fork/ANALYZER_CATALOG.md) for implementation details.
Included functionality and independently tested functionality are recorded
separately in [VALIDATION.md](VALIDATION.md).

## Install

Use Python 3.12 through 3.14 and a dedicated virtual environment. Python 3.12
is the validated version. Dependencies require a network connection during setup.

Clone the source, then install with [uv](https://docs.astral.sh/uv/):

```powershell
git clone https://github.com/LautrecSec/skillsentry-foss.git
cd skillsentry-foss
uv sync --locked --all-extras
uv run --no-sync skillsentry --version
uv run --no-sync skillsentry scan ./examples/benign
```

This installs the development tools and optional MCP dependencies using the
committed lockfile. For a smaller installation, pip instructions, and
platform-specific setup, use the [start-to-finish guide](docs/fork/START_TO_FINISH.md).

## Scan a skill

```powershell
# Scan a skill directory.
uv run --no-sync skillsentry scan ./examples/benign

# Scan one Markdown file.
uv run --no-sync skillsentry scan ./examples/suspicious/SKILL.md

# Scan the immediate child skill directories in a collection.
uv run --no-sync skillsentry scan ./examples --recursive

# Inspect all scan options.
uv run --no-sync skillsentry scan --help
```

ZIP archives and remote repository/file URLs are also accepted. Remote inputs
require network access. Transitive reference retrieval is a separate opt-in;
review the [input and traversal guide](docs/fork/START_TO_FINISH.md#3-scan-each-supported-input)
before enabling it.

The suspicious example contains inert attack instructions for testing. It is
expected to produce findings and exit with code 1. Do not install it as a skill.

## Run the demonstration

```powershell
uv run --no-sync python scripts/demo.py
```

The demonstration scans both examples, compares command behavior, checks report
formats and SARIF structure, and exercises single-file, ZIP, and recursive inputs.
Generated reports are written under the ignored `artifacts/` directory.

Recorded static-scan results:

| Example | Findings | Risk score | Severity | Recommendation | Exit code |
| --- | --- | --- | --- | --- | --- |
| Benign | 0 | 0 | LOW | SAFE | 0 |
| Suspicious | 3 | 62 | HIGH | DO_NOT_INSTALL | 1 |

These are fixture results, not an accuracy benchmark. A `SAFE` recommendation is
a report label, not proof that an input is safe to install.

## Reports and CI policy

```powershell
uv run --no-sync skillsentry scan ./examples/suspicious --format json
uv run --no-sync skillsentry scan ./examples/suspicious --format markdown
uv run --no-sync skillsentry scan ./examples/suspicious --format sarif

# Fail on active findings, incomplete analysis, or coverage below 100 percent.
uv run --no-sync skillsentry scan ./examples/benign --fail-on-findings --fail-on-incomplete --min-coverage 100
```

Review findings, locations, inspection coverage, and completion status together.
A low risk score does not establish that every relevant file was inspected.

| Exit code | Meaning |
| --- | --- |
| 0 | Score is at most 50 and no requested strict gate fired |
| 1 | Score is above 50, or a requested finding, completeness, or coverage gate fired |
| 2 | Input, configuration, platform, or execution error |

On Windows, save reports by redirecting stdout to a new file in a trusted
directory outside the scan target. Use modern PowerShell for UTF-8 handling:

```powershell
uv run --no-sync skillsentry scan ./examples/benign --format json > ./new-scan.json
$scanExit = $LASTEXITCODE
if ($scanExit -ne 0) { throw "Scan did not pass; exit code: $scanExit" }
Get-Content -Raw ./new-scan.json | ConvertFrom-Json
```

The secure `--output FILE` writer supports POSIX guarantees and deliberately
rejects Windows. Shell redirection uses the shell's own file-creation behavior.
See the [report guide](docs/fork/START_TO_FINISH.md#4-read-reports-and-enforce-policy)
for details.

## Review accepted findings

Generate a baseline only after reviewing the findings you intend to accept:

```powershell
uv run --no-sync skillsentry baseline ./examples/suspicious --output - > ./reviewed-baseline.json
uv run --no-sync skillsentry scan ./examples/suspicious --baseline ./reviewed-baseline.json --show-suppressed
```

A generated baseline accepts every finding from that scan. Review its entries
before using it as policy. Never automatically trust a baseline supplied by an
untrusted skill. See the [suppression guide](docs/SUPPRESSION.md).

## Optional semantic analysis

Configure a supported local or hosted provider, then explicitly enable analysis:

```powershell
uv run --no-sync skillsentry scan ./examples/suspicious --llm --format json
```

Follow the [local inference setup](docs/fork/START_TO_FINISH.md#6-enable-local-semantic-analysis-when-desired)
for Ollama configuration, including the exact environment variable names.
Hosted provider configuration is covered in the [reference manual](README.upstream.md#llm-analysis).
Local models require their own compute and model downloads. Hosted services may
charge for requests. Live model inference has not been independently validated
for this distribution.

## MCP and agent integrations

Start the local stdio server:

```powershell
uv run --no-sync skillsentry mcp
```

The server exposes `scan_skill(target, use_llm, output_format)`. Set
`use_llm=false` in tool calls for static analysis. The MCP tool has its own
semantic-analysis default; the CLI's static default does not override it.

For installation and configuration, see the
[agent integration guide](docs/fork/START_TO_FINISH.md#7-use-agent-integrations),
[Pi extension](docs/PI_EXTENSION.md), [OpenCode extension](docs/OPENCODE_EXTENSION.md),
and [batch scanner](contrib/batch_scan/docs/README.md).

## Container use

```bash
docker build -t skillsentry-foss .
docker run --rm -v "$PWD:/scan" skillsentry-foss scan ./examples/benign
```

The container defaults to the `skillsentry` command. The Docker image has not
been built or run in the recorded validation environment.

## Security boundaries

- Scans inspect content without executing the target skill. They do not isolate
  or contain a skill that you later install.
- Static analysis can query OSV with dependency names and versions. Static mode
  is not an offline switch. Remote inputs and optional tracing can also use
  the network.
- Semantic analysis sends eligible content to the configured provider. Select
  a provider and deployment appropriate for the data being scanned.
- Findings can include false positives and false negatives. Static checks do
  not establish runtime safety or complete attack coverage.
- Keep HTTP MCP transport on a trusted loopback interface. It does not provide
  authentication for use as a public scanning service.

Read the [architecture and data-egress documentation](docs/fork/ARCHITECTURE.md)
and [security policy](SECURITY.md) before integrating scans into a trust decision.

## Development and verification

```powershell
uv run --no-sync python scripts/verify_upstream.py
uv run --no-sync pytest tests/fork -q -p no:cacheprovider
uv run --no-sync python scripts/demo.py
uv run --no-sync python -m build --no-isolation
uv run --no-sync python -m twine check dist/*
```

The full non-live Python suite and extension tests run on Linux. Focused project
checks also run on Windows. The exact observed results, corrected failures, and
untested paths are documented in [VALIDATION.md](VALIDATION.md). See
[CONTRIBUTING.md](CONTRIBUTING.md) for development requirements.

## Documentation

| Document | Contents |
| --- | --- |
| [Start to finish](docs/fork/START_TO_FINISH.md) | Installation, inputs, reports, providers, integrations, testing, and publication |
| [Architecture](docs/fork/ARCHITECTURE.md) | Components, trust boundaries, and network behavior |
| [Analyzer catalog](docs/fork/ANALYZER_CATALOG.md) | Analyzer inventory and rule mappings |
| [Feature matrix](docs/fork/FEATURE_PARITY.md) | Included functionality and verification evidence |
| [Validation](VALIDATION.md) | Recorded checks and limits |
| [Portfolio notes](docs/fork/PORTFOLIO.md) | Contribution scope and demonstration guidance |
| [Source provenance](UPSTREAM.md) | Source credits, pinned revision, and documented modifications |
| [Reference manual](README.upstream.md) | Preserved command, provider, and API reference |
| [Publication guide](docs/fork/PUBLISH.md) | Repository and release procedure |

## License and credits

[Apache License 2.0](LICENSE). This distribution includes third-party
open-source code. Source authorship and project modifications are documented in
[NOTICE](NOTICE) and [UPSTREAM.md](UPSTREAM.md). Retain those notices, existing
source headers, and [third-party notices](THIRD_PARTY_NOTICES.md) when redistributing.

Documentation modification notice: this README was rewritten for Skill Sentry
on 2026-10-28. The original manual is preserved in [README.upstream.md](README.upstream.md).
