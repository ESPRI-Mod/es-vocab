#!/bin/bash

set -u
set -e

# All relative paths are computed from this path.
readonly SCRIPT_DIR_PATH="$(dirname $0)"

source "${SCRIPT_DIR_PATH}/common.sh"

cd ${DOCUMENTATION_DIR_PATH}

echo -e "> pulling documentation:\n"
git pull origin ${GIT_DEPLOYMENT_BRANCH_NAME}

echo -e "> building documentation:\n"
pdm run mkdocs build -f "${MKDOCS_SETTINGS_FILE_PATH}"

exit 0
