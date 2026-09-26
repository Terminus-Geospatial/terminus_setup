#!/usr/bin/env bash
#
############################# INTELLECTUAL PROPERTY RIGHTS #############################
##                                                                                    ##
##                           Copyright (c) 2024 Terminus LLC                          ##
##                                All Rights Reserved.                                ##
##                                                                                    ##
##          Use of this source code is governed by LICENSE in the repo root.          ##
##                                                                                    ##
############################# INTELLECTUAL PROPERTY RIGHTS #############################
#
#    File:    build-images.sh
#    Author:  Marvin Smith
#    Date:    8/14/2026
#
#    Purpose:  Build the Terminus runtime and build container images.
#

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

readonly RUNTIME_TAG="${TERMINUS_RUNTIME_TAG:-terminus-runtime-centos10:latest}"
readonly BUILD_TAG="${TERMINUS_BUILD_TAG:-terminus-build-centos10:latest}"

function usage() {
    echo "Usage: $(basename "${BASH_SOURCE[0]}") [runtime-tag] [build-tag]"
    echo
    echo "Builds the Terminus CentOS Stream 10 runtime and build container images."
    echo "Optional environment variables:"
    echo "  TERMINUS_RUNTIME_TAG  Tag for the runtime image (default: terminus-runtime-centos10:latest)"
    echo "  TERMINUS_BUILD_TAG    Tag for the build image (default: terminus-build-centos10:latest)"
}

function build_runtime() {
    echo "Building runtime image: ${RUNTIME_TAG}"
    docker build --no-cache \
        -f "${REPO_DIR}/docker/Dockerfile.runtime" \
        -t "${RUNTIME_TAG}" \
        "${REPO_DIR}"
}

function build_build() {
    echo "Building build image: ${BUILD_TAG}"
    docker build --no-cache \
        -f "${REPO_DIR}/docker/Dockerfile.build" \
        -t "${BUILD_TAG}" \
        "${REPO_DIR}"
}

function main() {
    if [[ "$#" -gt 0 && ( "$1" == "-h" || "$1" == "--help" ) ]]; then
        usage
        exit 0
    fi

    build_runtime
    build_build

    echo "Done."
    echo "  Runtime: ${RUNTIME_TAG}"
    echo "  Build:   ${BUILD_TAG}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
