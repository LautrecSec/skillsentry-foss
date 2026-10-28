# Start to finish

SkillSentry FOSS is an independent Apache-2.0 fork of NVIDIA SkillSpector 2.12.0 at
commit `e7172462caf367736645f66c1aa154ca5f9c64dc`. The scanner, rule definitions,
report contracts, providers, MCP implementation, and extensions are inherited.
The fork adds its own command and operational documentation. Read
[UPSTREAM.md](../../UPSTREAM.md) before presenting this as portfolio work.

## 1. Install the project

Use Python 3.12, 3.13, or 3.14. Python 3.12 is the initial validation target.
No NVIDIA account, GPU, API key, or paid service is required for static scans.
Dependencies must be downloaded during initial installation. Free software does
not make hosted inference or compute free.

Run the commands from the repository root. `uv` is optional but recommended for
the committed dependency lock. Install it using the
[official installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

### Windows PowerShell

```powershell
uv sync --locked --all-extras
uv run --no-sync skillsentry --version
uv run --no-sync skillsentry scan ./examples/benign
```

Without uv, use an existing supported Python installation:

```powershell
py -3.12 -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -e '.[dev]'
& ./.venv/Scripts/skillsentry.exe --version
& ./.venv/Scripts/skillsentry.exe scan ./examples/benign
```

The pip path resolves compatible dependencies at installation time. Use uv for
the exact versions in `uv.lock`. Invoking the venv executable avoids changing
PowerShell execution policy or activating a script.

### Linux or macOS

```bash
uv sync --locked --all-extras
uv run --no-sync skillsentry scan ./examples/benign
```

Or use pip:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/skillsentry scan ./examples/benign
```

The Python distribution keeps the name `skillspector` for upstream metadata and
integration compatibility. Install this fork in its own venv. Installing it
alongside another SkillSpector distribution in one environment replaces that
distribution; it is not a second independent Python package.

## 2. Run the reproducible demonstration

```bash
uv run --no-sync python scripts/demo.py
```

The script invokes both CLIs against both examples with static analysis,
compares finding signatures and risk scores, checks SARIF, exercises recursive
scanning, single-file input and ZIP input, and writes reports under `artifacts/`.
It fails if the deliberately suspicious fixture produces no findings. The
fixtures contain inert text. They are never installed or executed as skills.
This is a smoke demonstration, not a detection benchmark or proof of safety.

## 3. Scan each supported input

```bash
uv run --no-sync skillsentry scan ./examples/benign
uv run --no-sync skillsentry scan ./examples/suspicious/SKILL.md
uv run --no-sync skillsentry scan ./artifacts/example.zip
uv run --no-sync skillsentry scan ./examples --recursive
```

Remote scans also accept Git repository URLs and supported file URLs:

```bash
uv run --no-sync skillsentry scan https://github.com/NVIDIA/skills
```

That repository is an example remote input, not a statement about its findings.
Remote inputs require network access. Transitive retrieval is separately opt-in:

```bash
uv run --no-sync skillsentry scan ./examples/benign --transitive --transitive-depth 1
```

Use repeatable `--transitive-allow-prefix` and `--transitive-deny-prefix` to
constrain destinations. Review [resource bounds](../ANALYSIS_RESOURCE_BOUNDS.md)
and [nested artifacts](../NESTED_ARTIFACT_INSPECTION.md) before large scans.

## 4. Read reports and enforce policy

```bash
uv run --no-sync skillsentry scan ./examples/suspicious --format json
uv run --no-sync skillsentry scan ./examples/suspicious --format markdown
uv run --no-sync skillsentry scan ./examples/suspicious --format sarif
uv run --no-sync skillsentry scan ./examples/benign --fail-on-findings --fail-on-incomplete --min-coverage 100
```

Read findings, locations, severity, risk assessment, coverage, and the inspection
ledger together. `SAFE` is the engine's report label; it is not a guarantee that
the skill is safe. Review incomplete analysis before making installation decisions.

| Exit | Meaning |
| --- | --- |
| 0 | Scan completed with score at most 50 and no requested strict gate fired |
| 1 | Score above 50, or a requested finding/completeness/coverage gate fired |
| 2 | Input, configuration, platform, or execution error |

On POSIX platforms, reports can use `--output FILE` with the inherited secure
writer. On Windows that writer deliberately refuses unsupported guarantees.
Redirect stdout to a new trusted destination outside the scan target:

```powershell
uv run --no-sync skillsentry scan ./examples/suspicious --format json > ./new-scan.json
$scanExit = $LASTEXITCODE
if ($scanExit -eq 2) { throw 'Scan failed; do not accept the report.' }
Get-Content -Raw ./new-scan.json | ConvertFrom-Json
```

For consistent UTF-8 redirection use modern PowerShell, preferably 7.4 or newer.
The demo uses Python subprocess byte capture and therefore avoids shell encoding
differences. Shell redirection has the shell's file creation semantics, not the
engine's symlink-resistant writer. Use a trusted directory and a new filename.

## 5. Handle accepted findings

Generate a baseline on stdout, which also works on Windows:

```powershell
uv run --no-sync skillsentry baseline ./examples/benign --output - > ./reviewed-baseline.json
uv run --no-sync skillsentry scan ./examples/benign --baseline ./reviewed-baseline.json --show-suppressed
```

Review each entry and its reason before adopting it. A generated baseline
suppresses every finding from that scan. Never automatically trust a baseline
shipped by an untrusted skill. `--use-shipped-baseline` remains opt-in.
See the complete [suppression specification](../SUPPRESSION.md).

## 6. Enable local semantic analysis when desired

The inherited Ollama provider uses a local OpenAI-compatible endpoint without a
paid API key. Install Ollama separately from [ollama.com](https://ollama.com/).
Download a locally runnable model and review that model's license and hardware
requirements. This example uses an upstream bundled model identifier:

```bash
ollama pull llama3.1:8b
```

Start the Ollama service if your installation does not already run it.
PowerShell configuration:

```powershell
$env:SKILLSPECTOR_PROVIDER = 'ollama'
$env:OLLAMA_BASE_URL = 'http://localhost:11434/v1'
$env:SKILLSPECTOR_MODEL = 'llama3.1:8b'
uv run --no-sync skillsentry scan ./examples/suspicious --llm --format json
```

Bash configuration:

```bash
export SKILLSPECTOR_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434/v1
export SKILLSPECTOR_MODEL=llama3.1:8b
uv run --no-sync skillsentry scan ./examples/suspicious --llm --format json
```

The endpoint's actual context size and structured-output behavior matter. Model
support is inherited, not a claim of local model equivalence to hosted models.
Inspect semantic runtime status and errors in the report. Local inference was
not exercised unless the validation report explicitly records it.

The fork's `skillsentry` command requires `--llm`. The compatibility command
`skillspector scan` retains upstream's default attempt to use LLM analysis.
Python callers must explicitly set `use_llm=False` when they want static analysis.
Hosted providers remain available with their existing configuration and costs.
A `.env` template is not automatically loaded by either CLI.

## 7. Use agent integrations

The optional MCP extra is included by `--all-extras`. For a smaller install use
`uv sync --locked --extra mcp`.

```bash
uv run --no-sync skillsentry mcp
uv run --no-sync skillsentry mcp --transport http --host 127.0.0.1 --port 8000
```

The inherited `scan_skill` tool has its own `use_llm` parameter. Set it to
`false` for static scans. The fork CLI's scan defaults do not alter MCP tool
defaults. HTTP rejects local target paths and binds to loopback. Do not expose
it as an unauthenticated public scanning service.

An MCP client configuration can invoke the compatibility command:

```json
{
  "mcpServers": {
    "skillsentry-foss": {
      "command": "skillspector",
      "args": ["mcp"]
    }
  }
}
```

Use the absolute executable path from your project's venv if the client cannot
resolve it on PATH. Keep existing integration identifiers intact. Follow the
retained [Pi guide](../PI_EXTENSION.md), [OpenCode guide](../OPENCODE_EXTENSION.md),
and [upstream manual](../../README.upstream.md#python-api-integration) for their
complete installation and API contracts. They use `skillspector` intentionally.

The contributed batch scanner remains under `contrib/batch_scan/`. Use its
[guide](../../contrib/batch_scan/docs/README.md) and pass `--no-llm` explicitly
when required; the new alias does not change its independent defaults.

## 8. Develop, verify, and package

```bash
uv run --no-sync python scripts/verify_upstream.py
uv run --no-sync pytest tests/fork -q
uv run --no-sync pytest -m 'not integration and not provider' tests --tb=short
uv run --no-sync ruff check src/skillsentry_foss tests/fork scripts/verify_upstream.py scripts/demo.py
uv run --no-sync python -m build --no-isolation
uv run --no-sync python -m twine check dist/*
```

The inherited suite includes POSIX file, permission, and shell assumptions.
Run the full suite on Linux or WSL. The fork CI runs the focused fork checks
on Windows and Linux and the full inherited suite on Linux. Live provider and
integration tests are deliberately excluded from credential-free CI.
See [VALIDATION.md](../../VALIDATION.md) for checks actually run in this workspace.

Git checkouts retain the executable bit on `tests/docker/smoke.sh`. If you use a
Python source archive built on Windows, run `chmod +x tests/docker/smoke.sh` on
Linux before invoking `make docker-smoke`, or invoke the script with Bash.

## 9. Publish and present the work

Follow [PUBLISH.md](PUBLISH.md) to create your own public repository and first
release. Use [PORTFOLIO.md](PORTFOLIO.md) for an accurate project description,
demonstration sequence, and interview discussion. Do not claim the inherited
scanner, detection rules, research results, or test corpus as original work.
