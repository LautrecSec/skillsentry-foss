# Feature parity and verification

Baseline: NVIDIA SkillSpector 2.12.0, commit
`e7172462caf367736645f66c1aa154ca5f9c64dc`, checked on 2026-10-28.
The fork includes all 467 tracked upstream files, with documented project-level
changes and archived originals. The complete engine under `src/skillspector/`
is retained unchanged. The verifier checks that claim against the source manifest.

This is source and interface parity with a pinned version, not a promise to
track future commits automatically. Runtime evidence is recorded separately in
[VALIDATION.md](../../VALIDATION.md). Inheritance alone does not prove equivalent
model output, detection accuracy, or behavior on every operating system.

## Input and workflow capabilities

| Capability | Included implementation or guide | Verification |
| --- | --- | --- |
| Local skill directories | `input_handler.py`, `cli.py` | Demo and inherited tests |
| Single-file inputs | `input_handler.py` | Demo and inherited tests |
| ZIP bundles and nested artifacts | `input_handler.py`, `nested_artifacts.py` | ZIP demo; nested parser tests inherited |
| Git repository and file URLs | `input_handler.py` | Source preserved; remote networking not required by demo |
| Recursive skill collections | `multi_skill.py`, CLI recursive path | Demo and inherited tests |
| Transitive reference traversal | `references.py`, `transitive.py`, CLI | Source preserved; inherited tests |
| Explicit exclusions and scope | CLI and inspection ledger | Source preserved; inherited tests |
| Download, archive, parser, time, and finding limits | `state.py`, artifact modules | Source preserved; resource-bound tests inherited |
| Fail-closed incomplete-analysis records | `inspection_ledger.py`, `nodes/finalize_inspection_ledger.py` | Source preserved; inherited tests |
| OpenSSF/DSSE content projection | `oms.py` | Source preserved; no signature verification claimed |

Paths without a prefix are relative to `src/skillspector/`.

## Analysis coverage

| Capability | Source under `nodes/analyzers/` | Notes |
| --- | --- | --- |
| Prompt injection | `static_patterns_prompt_injection.py` | Original rules and normalization |
| Anti-refusal instructions | `static_patterns_anti_refusal.py` | Original rules |
| Data exfiltration | `static_patterns_data_exfiltration.py` | Original rules |
| Privilege escalation | `static_patterns_privilege_escalation.py` | Original rules |
| Supply chain and trigger abuse | `static_patterns_supply_chain.py`, `osv_client.py` | Live OSV lookup and offline fallback retained |
| Excessive agency | `static_patterns_excessive_agency.py` | Original rules |
| Output handling | `static_patterns_output_handling.py`, `sql_parameter_binding.py` | Includes latest pinned SQL binding precision proof |
| System prompt leakage | `static_patterns_system_prompt_leakage.py` | Original rules |
| Memory poisoning | `static_patterns_memory_poisoning.py` | Original rules |
| Tool misuse | `static_patterns_tool_misuse.py` | Original rules |
| Rogue agent behavior | `static_patterns_rogue_agent.py` | Original rules |
| Agent snooping | `static_patterns_agent_snooping.py` | Present in source beyond the README's older headline count |
| SSRF | `static_patterns_ssrf.py` | Original rules |
| Unsafe deserialization | `static_patterns_deserialization.py` | Original rules |
| Harmful content | `static_patterns_harmful_content.py` | Original rules |
| Dangerous Python behavior | `behavioral_ast.py` | AST analysis retained |
| Taint tracking | `behavioral_taint_tracking.py` | Original source/sink logic |
| YARA signatures and custom rule directories | `static_yara.py`, `../../yara_rules/` | Compiled YARA dependency retained |
| Bundled hooks and project execution settings | `bundled_execution_surface.py` | Original activation and capability logic |
| MCP least privilege | `mcp_least_privilege.py` | Original permission analysis |
| MCP tool poisoning and drift | `mcp_tool_poisoning.py`, `mcp_rug_pull.py` | Static and optional semantic paths retained |
| Artifact integrity | `artifact_integrity.py` | Original verification and incompleteness behavior |
| Semantic security discovery | `semantic_security_discovery.py` | Requires configured model and semantic opt-in |
| Semantic developer intent and quality policy | `semantic_developer_intent.py`, `semantic_quality_policy.py` | Requires configured model and semantic opt-in |
| Meta review and deterministic finding retention | `../meta_analyzer.py` | Retained even when model review disputes or fails |

The original README says 71 patterns across 17 categories. That headline is not
used as a verified total for this snapshot. The source has evolved beyond those
categories. [ANALYZER_CATALOG.md](ANALYZER_CATALOG.md) records the actual discovered
analyzers and central rule-name mapping at this commit. That mapping is not a
claim that every rule applies to every input or that it includes every dynamic
diagnostic ID.

## Reports and policy

| Capability | Included implementation | Verification |
| --- | --- | --- |
| Terminal, JSON, Markdown, SARIF 2.1.0 | `nodes/report.py`, `sarif_models.py` | Demo produces all four and validates SARIF |
| Risk score, severity, recommendation | Report module | Both CLIs compared on fixtures |
| Baselines, glob rules, fingerprints, suppressed findings | `suppression.py`, CLI baseline command | Original behavior plus fork default tests |
| Strict finding/completeness/coverage gates | CLI | Original flags retained and command surface tested |
| Structured locations and nested provenance | Artifact modules and reports | Original schemas preserved |
| Inference usage and provider/model provenance | `inference_usage.py`, `llm_provenance.py` | Static demo checks no requested inference |
| Secure file output and cleanup | `file_output.py`, `cleanup.py` | POSIX guarantees retained; Windows stdout path documented |

## Providers and integrations

The complete `providers/` tree is included: NVIDIA Build, OpenAI, Anthropic,
Anthropic proxy, Amazon Bedrock, Azure OpenAI, Gemini, Ollama, OpenAI-compatible,
and the inherited agent CLI adapters. Availability, authentication, model
features, and costs depend on the provider. Registered or present does not mean
all adapters are enabled; the upstream Codex CLI restriction remains intact.

| Capability | Included interface | Scope |
| --- | --- | --- |
| Python graph API | `from skillspector import graph, create_graph` | Unchanged |
| MCP server, stdio and loopback HTTP | `mcp_server.py`, `mcp` command | Unchanged server and tool arguments |
| MCP Registry scan and snapshot comparison | `mcp_registry.py`, CLI registry flags | Unchanged |
| Pi extension | `extensions/skillspector.ts`, `package.json` | Unchanged tool/package identity |
| OpenCode tool and command | `.opencode/` | Unchanged |
| Agent skill integrations | `skills/` | Unchanged |
| Contributed multilingual batch scanning | `contrib/batch_scan/` | Unchanged independent defaults |
| LangGraph development workflow | `langgraph.json`, development extra | Unchanged |
| Container | `Dockerfile` | Same engine; fork entry point and notice inclusion differ |

## Intentional differences

1. The new `skillsentry scan` and `baseline` default to static analysis and
   accept `--llm`. The compatibility command is unchanged.
2. Fork version, README, notices, security policy, contribution guide, and
   packaging identify the independent project.
3. The container defaults to `skillsentry`.
4. Active CI is independent; upstream release publishing, scorecard publication,
   and automatic PR branch updates are archived rather than activated.
5. The fork adds verification, tests, examples, and documentation. It does not
   recreate NVIDIA's hosted Verified Skills pipeline, catalog, or signing service.
