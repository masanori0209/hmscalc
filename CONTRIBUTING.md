# Contributing to hmscalc

Thank you for contributing to `hmscalc`!

## Branching

| Branch | Purpose |
|--------|---------|
| `main` | Stable releases (PyPI tags) |
| `release/vX.Y.Z` | Release preparation |
| `feat/*` / `fix/*` | Features and bug fixes |

Typical flow: branch from `main` → PR → CI pass → merge → tag `vX.Y.Z` on `main` → PyPI publish.

## Local development

### Poetry (recommended)

```bash
poetry install
poetry run pytest
poetry run pytest --cov=hmscalc --cov-report=term-missing --cov-fail-under=95
poetry run ruff check hmscalc tests
poetry run black --check hmscalc tests
poetry run isort --check-only hmscalc tests
poetry run mypy hmscalc tests
```

### Documentation site (MkDocs)

```bash
poetry run mkdocs serve    # local preview at http://127.0.0.1:8000
poetry run mkdocs build    # output in site/
```

**GitHub Pages:** enabled with `build_type: workflow`. Pushes to `main` and version tags deploy via `.github/workflows/docs.yml`.  
Site: https://masanori0209.github.io/hmscalc/

**Read the Docs:** import the project at [readthedocs.org](https://readthedocs.org/) and point to `.readthedocs.yaml`.

### Optional pandas extra

```bash
poetry install -E pandas
poetry run pytest tests/test_pandas_extra.py
```

### Docker (multi-Python matrix)

```bash
docker build -t hmscalc .
docker run --rm hmscalc ./runtests.sh
docker run --rm hmscalc ./lint.sh
```

## Pull requests

- Target `main` unless coordinating a release branch
- Ensure CI passes (test matrix 3.9–3.14, lint, mypy)
- Update `CHANGELOG.md` for user-visible changes
- Add tests for new behavior

## Releases

1. Bump version in `pyproject.toml` and `CHANGELOG.md`
2. Merge release PR to `main`
3. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push origin vX.Y.Z`
4. GitHub Actions publishes to PyPI on tag push

## Public API

Only symbols listed in `hmscalc.__all__` are public. Names prefixed with `_` are internal.

```python
from hmscalc import (
    HMSTime,
    HMSTimeError,
    InvalidTimeFormatError,
    NotTimeStringError,
)
```

## Code style

- Line length: 120 (black, ruff)
- Strict mypy on library and tests
- Docstrings: Google style (existing convention)
