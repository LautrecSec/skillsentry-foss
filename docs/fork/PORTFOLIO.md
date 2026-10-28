# Portfolio and interview guide

## Project description

SkillSentry FOSS is an independent fork of NVIDIA SkillSpector for inspecting AI
agent skills before installation. It preserves the upstream scanner and adds a
static-first command, explicit LLM opt-in, source-provenance verification,
compatibility tests, reproducible examples, and operational documentation.

The original scanner, analyzers, detection rules, LangGraph workflow, providers,
MCP implementation, and integration test corpus come from NVIDIA SkillSpector
and its contributors. The repository records that relationship in the README,
NOTICE, manifest, and feature matrix.

## What this project can demonstrate

| Engineering decision | Evidence to show |
| --- | --- |
| Preserve compatibility instead of rewriting working security code | Retained engine plus command-surface tests |
| Make inference an explicit choice | `skillsentry scan --help` and default-policy tests |
| Separate source availability from verified runtime behavior | Feature matrix and validation report |
| Make the fork auditable | Pinned commit, manifest, documented exceptions, verifier tests |
| Avoid claiming that static analysis is offline | Documented OSV and tracing boundaries |
| Preserve security controls on an unsupported platform | Windows output behavior and secure writer documentation |
| Treat scan completeness as installation policy | Inspection ledger and strict-gate examples |
| Attribute third-party work accurately | LICENSE, NOTICE, original headers and upstream documents |

## Five-minute demonstration

1. Show the upstream commit in `UPSTREAM.md`, then run the provenance verifier.
   Explain that the manifest detects drift but is not a signed attestation.
2. Run `skillsentry scan ./examples/benign`. Inspect the zero findings, risk
   assessment, and coverage rather than claiming a safety guarantee.
3. Run `skillsentry scan ./examples/suspicious --format json`. Show specific
   rule IDs, locations, evidence, and the failure exit code.
4. Run `python scripts/demo.py`. Show the comparison with the compatibility CLI,
   the validated SARIF file, and static-mode metadata.
5. Show the fork tests and the validation limitations. Explain which components
   you changed and which came directly from upstream.

## Claims supported by the repository

After reviewing and understanding the code, an accurate description is:

> Developed and validated an attributed fork of NVIDIA SkillSpector with
> static-first scanning, explicit LLM opt-in, source snapshot verification,
> CLI compatibility tests, and reproducible security-scanning examples.

Use only the test outcomes recorded in `VALIDATION.md` or a successful CI run.
Do not claim a precision rate, production deployment, novel detection algorithm,
or complete platform coverage without corresponding evidence.

For a resume, connect the work to what you can explain and defend personally.
AI-assisted implementation is still work you must review, test, and understand.
Retaining thousands of upstream tests does not mean you authored those tests.

## Interview questions to prepare

1. Why preserve the scanner instead of reimplementing its rules?
2. What exact behavior differs between the two CLI entry points?
3. What data can leave the host during a static scan?
4. Why are source hashes insufficient to prove detection quality or source trust?
5. How can a baseline hide a malicious finding?
6. What happens when an analyzer times out or encounters an unsupported artifact?
7. Why does Windows report output use a different workflow?
8. How would you evaluate a local LLM without assuming hosted-model equivalence?
9. Which changes would make future upstream updates harder to review?
10. Which results are observations, and which capabilities are merely inherited?

Use the implementation and validation report to answer. If you have not tested a
path, state that directly. This repository establishes an operational fork and
verification work; additional research claims require separate experiments.
