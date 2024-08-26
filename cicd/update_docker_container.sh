#!/bin/bash

####################### SETTINGS #######################

set -u
set -e

# All relative paths are computed from this path.
readonly SCRIPT_DIR_PATH="$(dirname $0)"

source "${SCRIPT_DIR_PATH}/common.sh"

readonly export DOCKER_TEST_IMAGE_PORT=8080
readonly DOCKER_COMPOSE_TEST_TARGET_NAME='test'
readonly DOCKER_COMPOSE_PROD_TARGET_NAME='prod'
readonly DOCKER_IMAGE_NAME_PREFIX='es-vocab'

####################### FUNCTIONS #######################

function delete_image
{
    local image_tag="${1}"
    image_ids=$(docker image ls --quiet --all --filter "reference=${DOCKER_IMAGE_NAME_PREFIX}:${image_tag}")
    if [[ -n ${image_ids} ]]; then
        echo "  > delete ${image_tag} image:"
        docker image rm --force ${image_ids}
    fi
}

function delete_container
{
    local container_tag="${1}"
    containers_ids=$(docker container ls --quiet --all --filter name=${container_tag})
    if [[ -n ${containers_ids} ]]; then
        echo "  > delete ${container_tag} container(s):"
        docker container rm --volumes --force ${containers_ids}
    fi
}

function delete_dangling_image
{
    image_ids=$(docker image ls --quiet --all --filter 'dangling=true')
    if [[ -n ${image_ids} ]]; then
        echo "  > delete dangling image(s):"
        docker image rm --force ${image_ids}
    fi
}

####################### MAIN #######################

cd "${SCRIPT_DIR_PATH}"

echo -e "> clean the test environment:\n" # On failed previous execution of this script.
delete_image ${DOCKER_COMPOSE_TEST_TARGET_NAME}
delete_container ${DOCKER_COMPOSE_TEST_TARGET_NAME}

echo -e "> building tmp docker image:\n"
docker compose build ${DOCKER_COMPOSE_TEST_TARGET_NAME}

echo -e "> starting the ${${DOCKER_COMPOSE_TEST_TARGET_NAME}} container:\n"
docker compose up --detach ${DOCKER_COMPOSE_TEST_TARGET_NAME}

# TODO: implement tests
test_result_code=0

# Whatever the container passes the tests, it must be shutdown.
docker compose down --volumes ${DOCKER_COMPOSE_TEST_TARGET_NAME} # Stop & delete test container.

if [ ${test_result_code} -eq 0 ]; then
    echo -e "> retag docker test into prod:\n"
    # Retag the test image into prod image.
    docker tag ${DOCKER_IMAGE_NAME_PREFIX}:${DOCKER_COMPOSE_TEST_TARGET_NAME} ${DOCKER_IMAGE_NAME_PREFIX}:${DOCKER_COMPOSE_PROD_TARGET_NAME}
    echo -e "> stop and delete the current prod container:\n"
    docker compose down --volumes prod
    echo -e "> start the new prod image:\n"
    docker compose up --detach ${DOCKER_COMPOSE_PROD_TARGET_NAME}
    echo -e "> clean the test environment"
    # Delete test image: it doesn't impact the newly deployed prod image!
    delete_image ${DOCKER_COMPOSE_TEST_TARGET_NAME}
    # Retagging makes the previous prod image to be untagged, so delete it:
    delete_dangling_image
# TODO: else (handle unpassed tests).
fi

# TODO: send email or Slack message.

exit 0
