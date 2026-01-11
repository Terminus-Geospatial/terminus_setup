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
#    File:    conan-deploy.bash
#    Author:  Marvin Smith
#    Date:    10/5/2023
#

#  Deploy an application with conan

set -e

function usage() {
    echo "usage: $(basename $0) [<reference>] [-d,--dest <dir>] [-r,--release] [-t,--toolset <num>]"
    echo "                      [-C,--channel [<chan>]] [-o,--option <conanopt>] [-h,--help]"
}

function details() {
    echo "Installs and deploys a previously build Conan package to a location suitable for running in"
    echo "isolation.  If a package matching the provided reference is found in the local Conan cache, then"
    echo "the contents from the cached package will be deployed without reaching out to the Package Manager."
    echo "Otherwise, Conan will check for a package in the package-manager to download, then deploy"
    echo
    echo "The script deploys applications to '\$HOME/installs/terminus' by default.  You can control this by"
    echo "providing the '-d' option."
    echo
    echo "IMPORTANT:  When a 'reference' is not provided, the script will deploy the package recipe in one"
    echo "of two ways: (1) if a 'deploy' method is present in the recipe, it will be used to create the "
    echo "deployment, or (2) if a 'deploy' method is not present in the recipe, then the default 'deploy'"
    echo "generator will be used, which copies the contents of the package **and all packages in it's dependency graph**"
    echo "to the deployment destination.  Note that (2) can result in very large deployoments for libraries"
    echo "that have a lot of dependencies, so in general we only run this script on packages that provide"
    echo " a 'deploy' method in their recipe."
    echo
    echo "Examples:"
    echo
    echo "  (1) $(basename $0)"
    echo
    echo "      Installs and deploys the app described by './configfile.py' to"
    echo "      '~/installs/apps/<name>' where '<name> is read from conanfile.py.  If there is no 'deploy'"
    echo "      method in the Conan recipe, then a copy of the package contents and the contents of all packages"
    echo "      in its dependency graph are included in the deployment."
    echo
    echo "  (2) $(basename $0) foo/1.0.0@"
    echo
    echo "      Installs and deploys the 'foo/1.0.0@' package to '~/installs/apps/foo'. If the package is"
    echo "      not in the local Conan cache, Conan will download it from whatever repo it is configured to use."
    echo
    echo "  (3) $(basename $0) foo/1.0.0@branches/develop -d ./deployment"
    echo
    echo "      Installs and deploys the 'foo/1.0.0@branches/develop' package to './deployment'. If the"
    echo "      package is not in the local Conan cache, Conan will download it from whatever repo it is"
    echo "      configured to use."
    echo
    echo "Arguments:"
    echo "  reference"
    echo "      (optional) The Conan package reference of the package to download.  If not provided, then"
    echo "      it is assumed there is a 'conanfile.py' file in the current working directory that can be"
    echo "      used determine the package to download.  If there is no 'deploy()' method in the 'conanfile.py',"
    echo "      then the contents of the package described by the recipe will be copied to the deployment"
    echo "      folder alongside the contents of all dependencies in it's dependency graph."
    echo
    echo "Options:"
    echo "  -h,--help"
    echo "      Display this help information"
    echo
    echo "  -d,--dest <dir>"
    echo "      The location to deploy the application to.  The value of '<dir>' may be relative or absolute."
    echo "      The default deployment area is '\$HOME/installs/terminus/<name>', where '<name>' is the name of"
    echo "      the package."
    echo
    echo "  -r,--release"
    echo "      Install the 'Release' version of the package."
    echo
    echo "  -C,--channel [<channel>]"
    echo "      Specifies the user/channel suffix to use when the 'reference' argument is not provided.  This"
    echo "      option is ignored if the 'reference' argument is provided.  If a value for this option is not"
    echo "      provided, then the value defaults to 'branches/develop'.  See the help for the '-C' option of"
    echo "      'conan-build.bash' for more information."
    echo
    echo "  -o,--option <conanopt>"
    echo "      Set a Conan package option that will be forwarded to the 'conan install' command used to"
    echo "      install and deploy the application.  The options must match those used by an existing"
    echo "      package (e.g. build with 'conan-build.bash' and the same set of options)."
}

function show_help() {
    echo "Terminus Build Process: Deploy an App with Conan"
    echo
    usage
    echo
    details
    echo
}

#--------------------------------------------#
#-          Start of primary script         -#
#--------------------------------------------#

#  Bring the required utilities into scope
dir_scripts="$(cd "$(dirname "$0")" && pwd)"
source "${dir_scripts}/log.bash"

#  Set the current conanfile.py in this directory
conanfile_path="$(realpath conanfile.py)"
if [ ! -f "${conanfile_path}" ]; then
    log_error "no conanfile found in this directory ($PWD)"
    exit 1
fi

#  Setup options
reference=''
app_name=''
app_version=''
app_channel=''
out_dir=''
options=()
build_type='Debug'

while [ $# -gt 0 ]; do
    case $1 in
        -h | --help)
            show_help
            exit 0
            ;;
        -d | --dest)
            shift
            out_dir="$1"
            ;;
        -r | --release)
            build_type='Release'
            ;;
        -C | --channel)
            shift
            if [ -z "$1" ] || [ "${1::1}" == '-' ]; then
                app_channel='branches/develop'
                set -- "$1" "$@"
            else
                app_channel="$1"
            fi
            ;;
        -o | --option)
            shift
            options+=("-o $1")
            ;;
        *)
            if [ -z "${reference}" ]; then
                reference="$1"
            else
                log_error "Unrecognized option '$1'"
                exit 1
            fi
            ;;
    esac
    shift
done

source "${dir_scripts}/conan-setup.bash" -m

#  Make sure we have everything we need for an install/deployment
#
if [ -z "${reference}" ]; then
    #  The user didn't provide an explicit reference.  We will attempt to form it
    #  ourselves from a local 'conanfile.py' or using the legacy options.
    if [ -z ${app_name} ]; then
        app_name=$(getAppNameFromConanfileFunc)
    fi
    if [ -z ${app_version} ]; then
        app_version=$(getAppVersionFromConanfileFunc)
    fi
    reference="${app_name}/${app_version}@${app_channel}"

    #  Determine if there is a 'deploy' method in the Conan recipe.  If there is not,
    #  then use the default deployment mechanism, which is just a copy of the package
    #  contents from the cache.
    deploy_func="$(grep 'def deploy' conanfile.py || true)"
    if [ -z "${deploy_func}" ]; then
        log_info "Will use default deployer (copies content of all package in dependency graph)"
        deployer="-d full_deploy"
    else
        log_info "Will use 'deploy' method from recipe."
    fi
else
    #  The user provided an explicit reference.  We still need to grab the name of the app
    #  from the reference though so that we can create an appropriate directory to deploy
    #  the package contents to.
    app_name_version="$(echo ${reference} | cut -d '@' -f 1)"
    app_name="$(echo ${app_name_version} | cut -d '/' -f 1)"

    #  Check if there's a deploy method in the local conanfile.py
    if [ -f "conanfile.py" ]; then
        deploy_func="$(grep 'def deploy' conanfile.py || true)"
        if [ ! -z "${deploy_func}" ]; then
            log_info "Will use 'deploy' method from recipe."
        else
            log_info "Will use default deployer (copies content of all package in dependency graph)"
            deployer="-d runtime_deploy"
        fi
    else
        log_info "No local conanfile.py found, using default deployer"
        deployer="-d runtime_deploy"
    fi
fi

#  Configure the output location
out_dir="${out_dir:-${HOME}/installs/terminus/$app_name}"

#  Deploy
log_info "Will deploy to ${out_dir}"
log_info "--------------------------------------------------------"
log_info "Deploying ${reference}", Deployer: ${deployer}
log_info "--------------------------------------------------------"

mkdir -p "${out_dir}"
cd "${out_dir}"
echo "PWD: ${PWD}"
CMD="conan install ${conanfile_path} -s build_type=${build_type} ${options[@]} --deployer-package ${reference} ${deployer}"
echo "${CMD}"
${CMD}

log_info "--------------------------------------------------------"
log_info "Deployment Complete"
log_info "--------------------------------------------------------"

exit 0