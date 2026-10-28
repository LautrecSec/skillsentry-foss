# Publish to GitHub

Project repository: [LautrecSec/skillsentry-foss](https://github.com/LautrecSec/skillsentry-foss).
This guide covers source verification, publication, and release creation.
Run publication commands from this project's root, not from its parent checkout.

## 1. Verify what will be published

```bash
uv run --no-sync python scripts/verify_upstream.py
uv run --no-sync pytest tests/fork -q
uv run --no-sync python scripts/demo.py
uv run --no-sync python -m build --no-isolation
uv run --no-sync python -m twine check dist/*
```

Review `VALIDATION.md`. Keep attribution and license files. Check that generated
reports contain only intended public fixtures. The `.gitignore` excludes venvs,
environment files, caches, build outputs, and `artifacts/`. The existing upstream
fixtures contain deliberately malicious strings for testing; these are expected
test data, not scripts to run manually.

## 2. Initialize local history

If `.git` already exists in this folder, use it. Otherwise:

```bash
git init -b main
git remote add upstream https://github.com/NVIDIA/SkillSpector.git
```

Check `git rev-parse --show-toplevel` and confirm it resolves to this folder.
Then review and commit:

```bash
git status --short
git add .
git diff --cached --stat
git diff --cached --check
git commit -m "Create attributed SkillSentry FOSS distribution"
```

Git requires your own configured name and email. Use your verified GitHub
identity or GitHub no-reply email. Do not fabricate an author identity. The
initial commit contains a snapshot; it must not claim to have authored every
inherited file. Attribution in the repository remains necessary.

## 3. Create your public repository

For a new copy under your own account, use an authenticated
[GitHub CLI](https://cli.github.com/):

```bash
gh auth status
gh repo create skillsentry-foss --public --source . --remote origin --push --description "Security scanning for AI agent skills with static analysis by default, optional semantic analysis, and reproducible verification."
```

This command publishes to the authenticated account. It is intended to be run
by the owner after reviewing the staged contents. It does not register the
project as a GitHub fork. If that repository name is taken in your account,
choose another name and update your project links after creation.

Alternatively, create an empty public repository through GitHub's New repository
page without generating README, license, or gitignore files. Add its displayed
remote URL as `origin` and use GitHub's displayed command to push `main`.
If the repository already exists, verify `git remote -v` before pushing.

GitHub OAuth credentials need the `workflow` scope to push this project's
`.github/workflows/ci.yml`. If GitHub rejects the push for that missing scope:

```bash
gh auth refresh --hostname github.com --scopes workflow
git push --set-upstream origin main
```

Review and authorize the additional permission in your browser before retrying.

## 4. Set repository presentation and security

1. Keep the README's license and source-credit links, attribution files, and source headers.
2. Use topics such as `ai-security`, `agent-skills`, `security-scanner`,
   `static-analysis`, `mcp`, and `red-teaming` when they fit your presentation.
3. Enable GitHub Actions. Wait for the fork CI results before claiming CI passes.
4. Enable private vulnerability reporting and confirm the Security tab offers
   its reporting form. Update `SECURITY.md` when a private contact is available.
5. Enable dependency/security features available for the repository and configure
   branch protection or repository rules if needed. No organization policies
   or administrative settings are assumed to have been configured.
6. Pin the project on your profile after you have reviewed it and can explain
   its implementation and limitations.

The active workflow uses read-only repository permissions, pinned action commits,
and no provider credentials. It does not publish packages, create releases,
modify contributor branches, or automatically publish scorecard results.

## 5. Create a release

After CI passes and `VALIDATION.md` reflects the released state:

```bash
git tag -a v2.12.0-skillsentry.1 -m "SkillSentry FOSS, based on NVIDIA SkillSpector 2.12.0"
git push origin v2.12.0-skillsentry.1
gh release create v2.12.0-skillsentry.1 --verify-tag --title "SkillSentry FOSS 2.12.0 + fork 1" --notes-file RELEASE_NOTES.md dist/*
```

The package uses the PEP 440 version `2.12.0+skillsentry.1`; the Git tag uses a
portable spelling. Attach the built wheel and source archive. Retain notices in
both. Do not upload this compatibility distribution to the upstream `skillspector`
PyPI project. A separately published PyPI package would require a distinct
distribution identity and corresponding metadata changes.

## References

- [GitHub CLI repository creation](https://cli.github.com/manual/gh_repo_create)
- [GitHub private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
- [GitHub CLI release creation](https://cli.github.com/manual/gh_release_create)
