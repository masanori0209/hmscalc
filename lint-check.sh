#!/bin/bash
set -e

PYTHON_VERSIONS=( $(cat .python-version | xargs) )

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
eval "$(pyenv init --path)"

for VERSION in "${PYTHON_VERSIONS[@]}"; do
  echo "==> Linting with Python $VERSION for hmscalc."
  pyenv install -s $VERSION
  pyenv local $VERSION
  poetry env use $VERSION
  poetry install
  poetry run ruff check hmscalc tests --fix
  poetry run black check hmscalc tests
  poetry run isort check hmscalc tests
  poetry run mypy check hmscalc tests
  echo "==> Lint passed for Python $VERSION."
done
