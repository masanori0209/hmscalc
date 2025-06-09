# Contributing to hmscalc

Thank you for your interest in contributing to `hmscalc`!
This document outlines the branching strategy and rules used in this repository.

---

## 🚀 Branching Strategy

| Branch        | Purpose                            |
|---------------|-------------------------------------|
| `main`        | Stable branch for releases (PyPI)   |
| `develop`     | Active development integration      |
| `feature/*`   | New features (e.g. `feature/to-hours`) |
| `fix/*`       | Bug fixes (e.g. `fix/negative-format`) |
| `release/*`   | Release preparation (e.g. `release/v0.2.0`) |
| `hotfix/*`    | Emergency fixes for production      |

---

## 🔁 Typical Workflow

1. Start a feature branch from `develop`
2. Merge features into `develop` via pull requests
3. Create a `release/*` branch from `develop` when preparing for a new release
4. Merge `release/*` into both `main` and `develop`
5. Tag the release on `main` (e.g., `v0.2.0`) to trigger PyPI deployment

---

## ✅ Protected Branch: `main`

The `main` branch is protected with the following rules:

- ✅ **Pull requests required** — No direct push to `main`
- ✅ **Passing status checks required** — CI must pass (`pytest`, `mypy`, etc.)
- ✅ **Linear history only** — Merge commits are disallowed
- ✅ **Admins included** — Rules apply even to repository admins

To contribute:
- Always branch off `develop`
- Never commit directly to `main`
- Use descriptive branch names and PR titles

---

## 🧪 CI & PyPI Release

- All pull requests must pass tests via GitHub Actions
- Pushing a tag like `v0.2.0` to `main` will automatically publish to PyPI

---

Thank you for contributing!
