# SkillSentry FOSS 2.12.0+skillsentry.1

Initial independent distribution based on NVIDIA SkillSpector 2.12.0,
commit `e7172462caf367736645f66c1aa154ca5f9c64dc`.

## Included upstream functionality

The complete upstream scanner, rule definitions, providers, reporting, MCP
server, Pi/OpenCode integrations, batch tooling, tests, and documentation are
retained. See the feature matrix for source locations and runtime verification
status. No new detection accuracy or model-equivalence claim is made.

## Fork changes

- `skillsentry` defaults scans and baseline generation to static analysis.
- `--llm` explicitly enables the configured semantic provider on those commands.
- The original `skillspector` executable and Python API retain upstream behavior.
- A pinned source manifest and verifier detect inherited-source drift.
- Fork tests verify the opt-in policy and command compatibility.
- Inert examples and a reproducible demo exercise input and report formats.
- Setup, architecture, egress, feature parity, portfolio, and publication guides
  document the fork and its limitations.
- Independent CI replaces active upstream release and repository mutation jobs.
- Apache license and third-party attribution are retained in distribution files.

## Operational notes

Static scans can query OSV. LLM analysis can send content to the selected
provider and may cost money. The default policy applies to the new CLI's scan
and baseline commands; MCP, batch, extensions, and Python callers retain their
own upstream controls. Use a dedicated venv because the distribution name
remains `skillspector`.

Read `VALIDATION.md` for executed checks and unverified paths before deploying.
