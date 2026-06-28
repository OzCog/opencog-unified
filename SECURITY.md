# Security Policy

## Supported Versions

OpenCog Unified is an actively-developed monorepo. Security fixes are applied
to the `main` branch and back-ported on a best-effort basis to the most recent
tagged release.

| Version  | Supported          |
| -------- | ------------------ |
| `main`   | :white_check_mark: |
| Released | :white_check_mark: (latest tag) |
| Older    | :x:                |

## Reporting a Vulnerability

**Please do not open a public issue for security vulnerabilities.**

The preferred reporting channel is **GitHub Security Advisories**:

> https://github.com/OzCog/opencog-unified/security/advisories/new

This delivers your report privately to the maintainers and lets us
collaborate on a fix and a coordinated disclosure timeline.

If you cannot use GitHub Security Advisories, email the maintainers at
`security@opencog.org` with the following information:

- **Affected component / cognitive layer** (foundation, core, logic, …)
- **Affected versions** (commit SHA or tag)
- **Reproduction steps** — minimal, copy-pasteable
- **Impact assessment** — what an attacker can achieve
- **Suggested mitigation**, if you have one

We will acknowledge your report within **72 hours** and aim to provide a
preliminary triage and remediation plan within **7 days**.

## Coordinated Disclosure

We follow a 90-day coordinated disclosure timeline by default. We will
publicly credit reporters in the release notes unless you request anonymity.

## Hardening Practices

The repository's CI applies these defensive controls automatically:

- **`gitleaks`** scans every push and PR for accidentally-committed secrets.
- **`actionlint` + `shellcheck`** enforce safe shell quoting in workflows.
- **`yamllint --strict`** rejects malformed workflow definitions.
- **Pinned action versions** are managed by Dependabot with grouped weekly PRs.
- **Branch protection** requires the `Quality Gate Status` check to pass.
- **`workflow-quoting` guard** ensures `GITHUB_*` variables are always quoted.

If you discover a CI hardening gap, please open an advisory or PR.
