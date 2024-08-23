#!/bin/bash

set -u
set -e

# All relative paths are computed from this path.
readonly SCRIPT_DIR_PATH="$(dirname $0)"

source "${SCRIPT_DIR_PATH}/common.sh"

cd "${SCRIPT_DIR_PATH}"

echo -e "> pulling deployment scripts:\n"
git pull origin ${GIT_DEPLOYMENT_BRANCH_NAME}

exit 0
