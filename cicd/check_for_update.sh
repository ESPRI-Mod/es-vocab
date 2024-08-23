#!/bin/bash
set -u

# All relative paths are computed from this path.
readonly SCRIPT_DIR_PATH="$(dirname $0)"

source "${SCRIPT_DIR_PATH}/common.sh"
source "${UPDATE_FILE_PATH}"

function reset_update_file
{
    sed -i "s/$1=.*/$1=0/g" "${UPDATE_FILE_PATH}"
    return $?
}

exit_code=0

if [ ${documentation} -eq 1 ]; then
    echo -e "\n*** updating documentation ***\n"
    { "${SCRIPT_DIR_PATH}/update_documentation.sh" && reset_update_file 'documentation' ; } || exit_code=1
fi

if [ ${deployment} -eq 1 ]; then
    echo -e "*** updating deployment scripts ***\n"
    { "${SCRIPT_DIR_PATH}/update_deployment_scripts.sh" && reset_update_file 'deployment' ; } || exit_code=1
fi

if [ ${service} -eq 1 ]; then
    echo -e "\n*** updating service ***\n"
    { "${SCRIPT_DIR_PATH}/update_service.sh" && reset_update_file 'service' ; } || exit_code=1
fi

exit ${exit_code}
