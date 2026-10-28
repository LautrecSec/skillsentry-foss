# Security policy

Fork modification notice: this policy replaces the upstream security policy.
The original is retained in [SECURITY.upstream.md](SECURITY.upstream.md).

SkillSentry FOSS is an independent fork. NVIDIA does not operate or support
this repository.

## Report vulnerabilities privately

For a vulnerability specific to this fork, use the repository's Security tab
and private vulnerability reporting form when the owner has enabled it.
Do not assume that reporting is enabled before the repository is published.
No private reporting address has been configured or verified in this local copy.

Do not place secrets, private skill contents, or sensitive exploit details in
public issues. If private reporting is unavailable, request a private contact
from the maintainer without disclosing the vulnerability itself.

For a vulnerability in the shared NVIDIA SkillSpector engine, follow
[NVIDIA's security reporting process](https://www.nvidia.com/en-us/security/).
The retained upstream security policy describes its submission routes.
Coordinate fork-specific details with the fork maintainer as appropriate.

## Include useful evidence

Include the fork version, upstream commit, Python version, OS, affected input
type, observed behavior, impact, and a minimal sanitized reproduction.
For incomplete analysis, include relevant inspection-ledger events and limits.
Remove credentials, personal information, and unrelated proprietary content.

## Supported scope

Only the current fork snapshot is maintained here. There is no guaranteed
response time, bug bounty, vendor support, or production assurance.

The scanner does not sandbox a skill you install afterward. Static scans may
contact OSV; semantic scans send content to the configured provider. Review
[the trust boundaries](docs/fork/ARCHITECTURE.md) and use the report's coverage
and failure information before making installation decisions.
