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
#   File:    conan-build.sh
#   Author:  Marvin Smith
#   Date:    7/5/2023
#
#   Purpose:  Build terminus repos using standard conan commands.
#

set -e

function usage() {
    echo "usage: $(basename $0) [-h,--help] [-r,--release] [-c,--clean] [-m,--minimal]"
    echo "                      [-s,--source-root <dir>] [-b,--build-root <dir>] [-v,--verbose]"
    echo "                      [-x,--no-deploy] [-C,--channel [<channel>]] [-B,--build-missing]"
    echo "                      [-o,--option <conan_pkg_option>]..."
}

function details() {
    echo "Builds executable applications and libraries for any C++ application utilizing the Terminus"
    echo "Integrated Build Process.  Some applications and libraries have dependencies managed by the"
    echo "Conan package manager."
    echo

}

function show_help() {
    echo "Terminus Integrated Build Process - Build Script"
    echo
    usage
    echo
    details
    echo
}

# Bring the required utilities into scope
dir_scripts="$(cd "$(dirname "$0")" && pwd)"
source "$dir_scripts/log.bash"

#  Configurable Options
build_type='Debug'
clean_build='false'
use_minimal_setup='false'
source_root=''
build_root=''
force_clean='false'
options=()
no_deploy='false'
no_package=false
channel=''
build_missing=''

while [ $# -gt 0 ]; do
    case $1 in
        -h | --help)
            show_help
            exit 0
            ;;
        -r | --release)
            build_type='Release'
            ;;
        -c | --clean)
            clean_build='true'
            ;;
        -f | --force)
            force_clean='true'
            ;;
        -n | --no-package)
            no_package=true
            no_deploy='true'
            ;;
        -s | --source-root)
            shift
            source_root="$(cd "$1" && pwd)"
            ;;
        -b | --build-root)
            shift
            mkdir -p "$1"
            build_root="$(cd "$1" && pwd)"
            ;;
        -v | --verbose)
            export VERBOSE=1
            ;;
        -o | --option)
            shift
            options+=("-o $1")
            ;;
        -x | --no-deploy)
            no_deploy='true'
            ;;
        -C | --channel)
            shift
            if [ -z "$1" ] || [ "${1::1}" == '-' ]; then
                channel='branches/development'
                set -- "$1" "$@"
            else
                channel="$1"
            fi
            ;;
        -B | --build-missing)
            build_missing='--build=missing'
            ;;
        *)
            log_error "Unrecognized option '$1'"
            exit 1
            ;;
    esac
    shift
done

#------------------------------------#
#-          Setup the build         -#
#------------------------------------#
if [ -z "${source_root}" ]; then
    source_root="$(pwd)"
fi

if [ ! -f "${source_root}/conanfile.py" ]; then
    log_info "No conanfile.py found in ${source_root}. Skipping Conan build."
    exit 0
fi

if [ -z "${build_root}" ]; then
    if [ "$source_root" == "$(pwd)" ]; then
        build_root="$(pwd)/build"
        mkdir -p "${build_root}"
    else
        build_root="$(pwd)"
    fi
fi

log_info "Source Root: ${source_root}"
log_info "Build Root : ${build_root}"

if [ "${clean_build}" == 'true' ]; then
    log_info "Cleaning build root"
    if [ "$build_root" == "$HOME" ]; then
        log_error "Will not clean build root as it is your home directory."
        exit 1
    fi
    if [ "${build_root}" != "$(pwd)" ]; then
        rm -rf "${build_root}"/*
    else
        choice='y'
        if [ "$force_clean" == 'false' ]; then
            read -p "wrn: The current directory is the build root.  Are you sure you want to clean it? [y/N] " choice
            choice="${choice:-n}"
        fi
        if [ "$choice" == 'y' ] || [ "$choice" == 'Y' ]; then
            rm -rf *
        else
            log_info "Stopping build"
            exit 1
        fi
    fi
fi

#  Define the CMake Command to Use
export cmd_cmake="${CONAN_CMAKE_PROGRAM:-cmake}"
if [ -z "$(command -v ${cmd_cmake})" ]; then
    log_error "CMake command '$cmd_cmake' not found."
    log_error ''
    log_error 'CMake is required for the Integrated Build Process, but may not be installed.'
    log_error 'If CMake is installed, set the CONAN_CMAKE_PROGRAM environment variable to'
    log_error 'either (1) the full path of the CMake executable or (2) the name of the CMake'
    log_error 'program discoverable on the ${PATH}.'
    exit 1
fi
log_info "Using CMake $("${cmd_cmake}" --version | head -1 | awk '{print $3}' )"


#----------------------------------------#
#-          Perform the Build           -#
#----------------------------------------#
source "${dir_scripts}/conan-setup.bash" -m

app_name=$(getAppNameFromConanfileFunc "$source_root")
app_version=$( getAppVersionFromConanfileFunc "${source_root}" )
pkg_ref="${app_name}/${app_version}@${channel}"

log_info '-------------------------------------'
log_info "Building ${pkg_ref} (Build-Type: ${build_type})"
log_info '-------------------------------------'

conanfile='conanfile.py'

log_info '-------------------------------------'
log_info "Running Conan Install (Build-Type: ${build_type})"
log_info '-------------------------------------'
CMD="conan install ${conanfile} ${build_missing} --output-folder build -s build_type=${build_type} ${options[@]}"
echo "${CMD}"
$CMD

CMD="conan build ${build_missing} --output-folder build -s build_type=${build_type} ${options[@]} conanfile.py"
echo ${CMD}
${CMD}


log_info '-------------------------------------'
log_info 'Calling export package'
log_info '-------------------------------------'

CMD="conan export-pkg --output-folder build -s build_type=${build_type} ${conanfile}"
echo ${CMD}
${CMD}

log_info '-------------------------------------'
log_info 'Build Complete'
log_info '-------------------------------------'
exit 0

#  After a successful compilation, automatically deploy the application if the
#  Conan recipe defines a 'deploy()' function (unless the user explicitly says
#  not to deploy).  We only deploy if there is a deploy function so that only
#  our applications (which conventially provide a deploy method) get deployed.
#  This prevents unnecessary copies of library package contents into the deployment area.
#
deploy_func="$(grep 'def deploy' ${conanfile} || true)"
if [ ! -z "${deploy_func}" ]; then
    if [ "${no_deploy}" == 'true' ]; then
        log_info "Skipping deployment"
    else
        if [ "${build_type}" == 'Release' ]; then
            options+=("-r")
        fi

        #  When running the deployment script, we explicitly pass in the reference of the
        #  package we just build.  We do this as opposed to using the Conan recipt for 2
        #  reasons:  (1) It makes building the arguments to the deployment script simpler,
        #  and (2) it prevents us from deploying libraries--or more specificatlly, packages
        #  without an explicit `deploy` method---which would result in unecessary copies of
        #  everything the package needs, which would include all packages in it's dependency
        #  graph.  You could imagine this might take up a lot of disk space unnecessarily,
        #  which is why we avoid it.
        log_info "Running deployment script"
        CMD="${dir_scripts}/conan-deploy.sh ${pkg_ref} ${options[@]}"
        echo ${CMD}
        ${CMD}
    fi
else
    log_info "Skipping deployment (no deploy function in recipe)"
fi

exit 0