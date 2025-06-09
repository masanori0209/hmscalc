#!/bin/bash
set -e

PYTHON_VERSIONS=("3.9.19" "3.10.14" "3.11.9" "3.12.3")

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
eval "$(pyenv init --path)"

for VERSION in "${PYTHON_VERSIONS[@]}"; do
  echo "==> Testing with Python $VERSION for hmscalc."
  pyenv install -s $VERSION
  pyenv local $VERSION
  poetry env use $VERSION
  poetry install
  poetry run pytest
done
