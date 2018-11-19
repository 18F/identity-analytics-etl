#!/bin/bash
# This script installs:
#
# - HomeBrew: package manager for mac, https://brew.sh/
# - pyenv: python version manager
# - pyenv-virtualenv: python virtual environment manager
# - Python3.6.2: our main analytics development version

PY_VER="3.6.2"

# test if specific formula is already installed
brew_is_installed() {
  brew list -1 | grep -Fqx "$1"
}

pyver_is_installed() {
  pyenv versions | grep -Fq "$1"
}

if ! command -v brew >/dev/null; then
  echo "Installing Homebrew ..."
    curl -fsS \
      'https://raw.githubusercontent.com/Homebrew/install/master/install' | ruby
else
  echo "Homebrew already installed. Skipping ..."
fi

if ! brew_is_installed 'pyenv'; then
  brew install pyenv
fi

if ! brew_is_installed 'pyenv-virtualenv'; then
  brew install pyenv-virtualenv
fi

if ! pyver_is_installed ${PY_VER}; then
  echo "Installing Python ${PY_VER} from pyenv"
  pyenv install ${PY_VER}
else
  echo "Python ${PY_VER} already installed. Skipping ..."
fi
