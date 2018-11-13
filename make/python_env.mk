# -*- coding: utf-8 -*-
# Auto generated from pygitrepo 0.0.25
#
# This Makefile is a dev-ops tool set.
# Compatible with:
#
# - Windows
# - MacOS
# - MacOS + pyenv + pyenv-virtualenv tool set
# - Linux
#
# Frequently used make command:
#
# - make up
# - make clean
# - make install
# - make test
# - make build_doc
# - make view_doc
# - make deploy_doc
# - make reformat


#--- User Defined Variable ---
PACKAGE_NAME="login_analytics"

# Python version Used for Development
PY_VER_MAJOR="3"
PY_VER_MINOR="6"
PY_VER_MICRO="2"

# If you use pyenv-virtualenv, set to "Y"
USE_PYENV="N"

# S3 Bucket Name
DOC_HOST_BUCKET_NAME="login-gov-doc"


#--- Derive Other Variable ---

# Virtualenv Name
VENV_NAME="${PACKAGE_NAME}_venv"

# Project Root Directory
GIT_ROOT_DIR=${shell git rev-parse --show-toplevel}
PROJECT_ROOT_DIR=${shell pwd}

ifeq (${OS}, Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif

# Windows
ifeq (${DETECTED_OS}, Windows)
    USE_PYENV="N"

    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/Scripts"
    SITE_PACKAGES="${VENV_DIR_REAL}/Lib/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/Lib64/site-packages"

    GLOBAL_PYTHON="/c/Python${PY_VER_MAJOR}${PY_VER_MINOR}/python.exe"
    OPEN_COMMAND="start"
endif


# MacOS
ifeq (${DETECTED_OS}, Darwin)

ifeq ($(USE_PYENV), "Y")
    VENV_DIR_REAL="${HOME}/.pyenv/versions/${PY_VERSION}/envs/${VENV_NAME}"
    VENV_DIR_LINK="${HOME}/.pyenv/versions/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
else
    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    VENV_DIR_LINK="./${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
endif

    GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
    OPEN_COMMAND="open"
endif


# Linux
ifeq (${DETECTED_OS}, Linux)
    USE_PYENV="N"

    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    VENV_DIR_LINK="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"

    GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
    OPEN_COMMAND="open"
endif


BASH_PROFILE_FILE="${HOME}/.bash_profile"

BIN_ACTIVATE="${BIN_DIR}/activate"
BIN_PYTHON="${BIN_DIR}/python"
BIN_PIP="${BIN_DIR}/pip"
BIN_PYTEST="${BIN_DIR}/pytest"
BIN_SPHINX_START="${BIN_DIR}/sphinx-quickstart"
BIN_TWINE="${BIN_DIR}/twine"
BIN_TOX="${BIN_DIR}/tox"
BIN_JUPYTER="${BIN_DIR}/jupyter"


S3_PREFIX="s3://${DOC_HOST_BUCKET_NAME}/${PACKAGE_NAME}"
AWS_DOC_URL="http://${DOC_HOST_BUCKET_NAME}.s3.amazonaws.com/${PACKAGE_NAME}/index.html"

PY_VERSION="${PY_VER_MAJOR}.${PY_VER_MINOR}.${PY_VER_MICRO}"


.PHONY: help
help: ## ** Show this help message
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


#--- Make Commands ---
.PHONY: info
info: ## ** Show information about python, pip in this environment
	@echo - venv: ${VENV_DIR_REAL} "\n"
	@echo - python executable: ${BIN_PYTHON} "\n"
	@echo - pip executable: ${BIN_PIP} "\n"
	@echo - document on s3: ${AWS_DOC_URL} "\n"
	@echo - site-packages: ${SITE_PACKAGES} "\n"


#--- Virtualenv ---
.PHONY: brew_install_pyenv
brew_install_pyenv: ## Install pyenv and pyenv-virtualenv
	-brew install pyenv
	-brew install pyenv-virtualenv


.PHONY: enable_pyenv
enable_pyenv: ## Config $HOME/.bash_profile file
	if ! grep -q 'export PYENV_ROOT="$$HOME/.pyenv"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'export PYENV_ROOT="$$HOME/.pyenv"' >> "${BASH_PROFILE_FILE}" ;\
	fi
	if ! grep -q 'export PATH="$$PYENV_ROOT/bin:$$PATH"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'export PATH="$$PYENV_ROOT/bin:$$PATH"' >> "${BASH_PROFILE_FILE}" ;\
	fi
	if ! grep -q 'eval "$$(pyenv init -)"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'eval "$$(pyenv init -)"' >> "${BASH_PROFILE_FILE}" ;\
	fi
	if ! grep -q 'eval "$$(pyenv virtualenv-init -)"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'eval "$$(pyenv virtualenv-init -)"' >> "${BASH_PROFILE_FILE}" ;\
	fi


.PHONY: setup_pyenv
setup_pyenv: brew_install_pyenv enable_pyenv ## Do some pre-setup for pyenv and pyenv-virtualenv
	pyenv install ${PY_VERSION} -s
	pyenv rehash


.PHONY: init_venv
init_venv: ## Initiate Virtual Environment
ifeq (${USE_PYENV}, "Y")
	# Install pyenv
	-brew install pyenv
	-brew install pyenv-virtualenv

	# Edit Config File
	if ! grep -q 'export PYENV_ROOT="$$HOME/.pyenv"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'export PYENV_ROOT="$$HOME/.pyenv"' >> "${BASH_PROFILE_FILE}" ;\
	fi
	if ! grep -q 'export PATH="$$PYENV_ROOT/bin:$$PATH"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'export PATH="$$PYENV_ROOT/bin:$$PATH"' >> "${BASH_PROFILE_FILE}" ;\
	fi
	if ! grep -q 'eval "$$(pyenv init -)"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'eval "$$(pyenv init -)"' >> "${BASH_PROFILE_FILE}" ;\
	fi
	if ! grep -q 'eval "$$(pyenv virtualenv-init -)"' "${BASH_PROFILE_FILE}" ; then\
	    echo 'eval "$$(pyenv virtualenv-init -)"' >> "${BASH_PROFILE_FILE}" ;\
	fi

	pyenv install ${PY_VERSION} -s
	pyenv rehash

	-pyenv virtualenv ${PY_VERSION} ${VENV_NAME}
else
	virtualenv -p ${GLOBAL_PYTHON} ${VENV_NAME}
endif


.PHONY: up
up: init_venv ## ** Set Up the Virtual Environment


.PHONY: clean
clean: ## ** Clean Up Virtual Environment
ifeq (${USE_PYENV}, "Y")
	-pyenv uninstall -f ${VENV_NAME}
else
	-rm -r ${VENV_DIR_REAL}
endif


#--- Install ---

.PHONY: uninstall
uninstall: ## ** Uninstall This Package
	-${BIN_PIP} uninstall -y ${PACKAGE_NAME}


.PHONY: install
install: uninstall ## ** Install This Package via setup.py
	${BIN_PIP} install .


.PHONY: dev_install
dev_install: uninstall ## ** Install This Package in Editable Mode
	${BIN_PIP} install --editable .


.PHONY: dev_dep
dev_dep: ## Install Development Dependencies
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PIP} install -r requirements-dev.txt; \
	)


.PHONY: test_dep
test_dep: ## Install Test Dependencies
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PIP} install -r requirements-test.txt; \
	)


.PHONY: doc_dep
doc_dep: ## Install Doc Dependencies
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PIP} install -r requirements-doc.txt; \
	)


#--- Test ---

.PHONY: test
test: dev_install test_dep ## ** Run test
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PYTEST} tests -s; \
	)


.PHONY: test_only
test_only: ## Run test without checking dependencies
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PYTEST} tests -s; \
	)


.PHONY: cov
cov: dev_install test_dep ## ** Run Code Coverage test
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PYTEST} tests -s --cov=${PACKAGE_NAME} --cov-report term --cov-report annotate:.coverage.annotate; \
	)


.PHONY: cov_only
cov_only: ## Run Code Coverage test without checking dependencies
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PYTEST} tests -s --cov=${PACKAGE_NAME} --cov-report term --cov-report annotate:.coverage.annotate; \
	)


#--- Sphinx Doc ---

.PHONY: init_doc
init_doc: doc_dep ## Initialize Sphinx Documentation Library
	{ \
		cd ${PROJECT_ROOT_DIR}/docs; \
		${BIN_SPHINX_START}; \
	}


.PHONY: build_doc
build_doc: doc_dep dev_install ## ** Build Documents, start over
	-rm -r ${PROJECT_ROOT_DIR}/docs/build
	-rm -r ${PROJECT_ROOT_DIR}/docs/source/${PACKAGE_NAME}
	( \
		source ${BIN_ACTIVATE}; \
		cd ${PROJECT_ROOT_DIR}/docs; \
		make html; \
	)


.PHONY: build_doc_again
build_doc_again: ## Build Documents, skip re-install, skip cleanup-old-doc
	-rm -r ${PROJECT_ROOT_DIR}/docs/source/${PACKAGE_NAME}
	( \
		source ${BIN_ACTIVATE}; \
		cd ${PROJECT_ROOT_DIR}/docs; \
		make html; \
	)


.PHONY: view_doc
view_doc: ## ** Open Sphinx Documents
	${OPEN_COMMAND} ${PROJECT_ROOT_DIR}/docs/build/html/index.html


.PHONY: deploy_doc
deploy_doc: ## ** Deploy Document to AWS S3
	aws s3 rm ${S3_PREFIX} --recursive --profile 18f-dev
	aws s3 sync ${PROJECT_ROOT_DIR}/docs/build/html ${S3_PREFIX} --quiet --profile 18f-dev


.PHONY: clean_doc
clean_doc: ## Clean Existing Documents
	-rm -r ${PROJECT_ROOT_DIR}/docs/build


.PHONY: reformat
reformat: dev_dep ## ** Pep8 Format Source Code
	${BIN_PYTHON} ${PROJECT_ROOT_DIR}/fixcode.py


.PHONY: notebook
notebook: ## ** Run jupyter notebook
	${BIN_PIP} install jupyter
	${BIN_JUPYTER} notebook