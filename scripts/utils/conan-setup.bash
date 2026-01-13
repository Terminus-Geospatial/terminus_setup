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
#    File:    conan-setup.bash
#    Author:  Marvin Smith
#    Date:    7/5/2023
#
#    Purpose:  Setup Conan
#

if [ "${BASH_SOURCE[0]}" != "$0" ] && [ ! -z "$PS1" ]; then
    #  This script is being sourced from an interactive shell.  Setup error handling
    # properly for a sourced Bash script so that we don't terminate the shell script is
    # being sourced in if there is an error.  Also, be sure to restore the current shell
    # configuration when the sourced script exists.
    succeed='return 0'
    fail='return 1'
    set +o history
    set -e
    trap 'log_error "Conan setup failed"; set +e; false; return' ERR
    trap 'trap - ERR RETURN; unset succeed fail __user __pass; set +e; set -o history' RETURN
else
    #  Script is running in its own dedicated shell (non-interactive).  No need to preserve
    #  the shell configuration for a user.
    succeed='exit 0'
    fail='exit 1'
    set -e
    trap 'log_error "Conan setup failed"' ERR
    trap 'trap - ERR' RETURN
fi

#------------------------------------#
#-          Help Method             -#
#------------------------------------#
function usage() {
    echo "usage: $(basename $0)"
    echo
    echo "usage: source $(basename $0)"
}

function details() {
    echo 'This script makes sure we have Conan properly installed and configured so'
    echo 'it can be used in the Terminus Integrated Build Process.  It can be run in 2 ways:'
    echo
    echo "    - Execute : Just do Conan setup.  Conan will be available in '~/.local/bin', but"
    echo "      you are responsible for making sure it is in the PATH."
    echo
    echo "    - Source : Do Conan setup and make available additional variables/functions in"
    echo "      the current shell, including modifying PATH."
    echo
    echo "This script requires Python 3.10+.  It will try using 'python3' command directly."
}

function show_help() {
    echo "Terminus Integrated Build Process - Conan Setup Script"
    echo
    usage
    echo
    details
    echo
}

#----------------------------------------------------#
#-              Start the Primary Script            -#
#----------------------------------------------------#

#  Bring the required utilities into scope
__dir_scripts="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
eval "$(cat "$__dir_scripts/log.bash")"

#  Parse the Command-Line
__wheelhouse=''
__cli_config=()
__use_minimal_setup="${conan_setup_use_minimal:-false}"
__upgrade=false
__export=false
__python_cmd='python3'

while [ $# -gt 0 ]; do
    case $1 in
        -h | --help)
            show_help
            $succeed
            ;;
        --python)
            shift
            __python_cmd="$1"
            ;;
        -c | --config)
            shift
            __cli_config+=("$1")
            ;;
        -m | --minimal)
            __use_minimal_setup='true'
            ;;
        -u | --upgrade)
            __upgrade=true
            ;;
        -e | export)
            __export=true
            ;;
        *)
            if [ -z "$__wheelhouse" ]; then
                __wheelhouse="$1"
            else
                log_error "Unrecognized option '$1'"
                $fail
            fi
            ;;
    esac
    shift
done


log_info '------------------------------------------'
log_info ' Getting ready to use Conan'
log_info '------------------------------------------'

#  Configure the script
__env_config=($(env | grep conan_setup || true ))

__config_path_default="$__dir_scripts/conan-setup.cfg"
if [ ! -f "$__config_path_default" ]; then
    log_error "Could not find the default config file at '$__config_path_default'"
    $fail
fi

log_info "Loading Conan setup configuration defaults"
declare -A conan_setup_repos
eval "$(cat "$__config_path_default")"

#  Check if user already has a file
__config_path_user="$HOME/.conan-setup.cfg"
if [ -f "$__config_path_user" ]; then
    log_info "Loading Conan setup configuration for user"
    eval "$(cat "$__config_path_user")"
fi

function set_config() {
    #  Function used when setting values from the environment or CLI args
    __key="$(echo "$1" | cut -d '-' -f 1)"
    __val="$(echo "$1" | cut -d '-' -f 2)"

    if [ -z "$__val" ]; then
        log_error "Missing value for configuration '$__key'"
        return 1
    fi

    if [ "$__key" == "conan_setup_repos" ]; then
        conan_setup_repos=()
        #  More material left out here
    else
        eval "$__key=\"$__val\""
    fi
}

#  Override values from configuration file using environment variables
for __keyval in ${__env_config[@]}; do
    set_config "$__keyval"
done

#  Override values from configuration file using CLI args
for __keyval in ${__cli_config[@]}; do
    set_config "$__keyval"
done

#  Print configuration and environment
log_debug "Printing final environment and configuration"
for __v in $(env | grep CONAN ); do
    log_debug '(env)' $__v
done
for __v in $(declare -p | grep conan_setup | grep -v conan_setup_repos | cut -d' ' -f3-); do
    log_debug '(cfg)' $__v
done
for __k in ${!conan_setup_repos[@]}; do
    log_debug "(cfg) conan_setup_repos[$__k]=${conan_setup_repos[$__k]}"
done


#------------------------------------------------#
#-          Install and Configure Conan         -#
#------------------------------------------------#

# When Conan is installed, it will be installed in the ~/.local directory by default.
#  Add this to the path so we can use conan directly when sourcing this file.
#
if [ ! -z "$PYTHONUSERBASE" ]; then
    __conan_path="$PYTHONUSERBASE/bin"
else
    __conan_path="${HOME}/.local/bin"
fi
export PATH="$__conan_path:$PATH"

if [ "$__use_minimal_setup" == 'false' ]; then
    log_info 'Locating Conan'
    __cmd_conan="$(which conan 2> /dev/null || true)"
    if [ -z "$__cmd_conan" ] || ${__upgrade}; then
        log_info "Conan not available or an upgrade is requested.  Installing."
        log_info "Checking Python installation."

        # Use the specified Python command (defaults to python3)
        __cmd_python="$__python_cmd"

        if [ -z "$__cmd_python" ]; then
            log_error "Python not available.  Install Python3 or SCL Python3."
            $fail
        fi

        if [ ! -z "$__wheelhouse" ]; then
            log_info "Installing Conan $conan_setup_install_version using an offline Python package wheelhouse"
            $__cmd_python -m pip install --user --no-index --find-links "$__wheelhouse" conan
        else
            log_info "Downloading and installing Conan."
            $__cmd_python -m pip install --user conan

        fi
    fi
fi

__conan_version="$(conan --version | cut -d ' ' -f3 )"
log_info "Using conan $__conan_version"

#--------------------------------------------#
#-          Setup Conan Profile             -#
#--------------------------------------------#

log_info 'Setting up Conan profile'

# Check if default profile exists
if [ -f "${HOME}/.conan2/profiles/default" ]; then
    log_info "Conan profile already exists at ${HOME}/.conan2/profiles/default"
else
    log_info "Creating default Conan profile"
    conan profile detect
fi

#--------------------------------------------#
#-          OS-Specific Configuration      -#
#--------------------------------------------#

# Detect operating system
__os_name="$(uname -s)"
__os_version="$(uname -r)"

case "$__os_name" in
    Darwin*)
        # macOS specific configuration
        log_debug "Detected macOS system"
        # Add macOS-specific settings here
        ;;
    Linux*)
        # Linux specific configuration
        log_debug "Detected Linux system"
        # Add Linux-specific settings here
        ;;
    CYGWIN*|MINGW*|MSYS*)
        # Windows specific configuration
        log_debug "Detected Windows system"
        # Add Windows-specific settings here
        ;;
    *)
        log_warn "Unknown operating system: $__os_name"
        ;;
esac

#--------------------------------------------#
#-          Setup Remotes (Someday)         -#
#--------------------------------------------#

#--------------------------------------------#
#-          Export Conan Settings           -#
#--------------------------------------------#

#  Bring in more utility functions
eval "$(cat "$__dir_scripts/conan-utils.bash")"

log_info "Conan data will be stored in '${CONAN_USER_HOME:-$HOME}/.conan2'"

log_info '--------------------'
log_info 'Conan setup complete'
log_info '--------------------'

#  If the '-e' option was provided, and we are not being sourced, then export configuration to the user's
#   .bashrc.  This will allow us to run conan directly.
if $__export && [ ! -z "$PS1" ]; then
    log_info 'Exporting Conan shell configuration'

    #  Write the contents of the file that sets env variables needed to run the 'conan'
    #  command directly.  We write to a separate file so that it is easy to update the
    #  contents without needing to update the user's bashrc again.
    __env_file_name='.conan-setup.env'
    __env_file="$HOME/$__env_file_name"
    echo '$!/usr/bin/env bash' > $__env_file
    echo "export PATH=\"$__conan_path:\$PATH\"" >> $__env_file

    #  Add a line to the user's bashrc if it doesn't already exist.
    set +e
    __brc="$HOME/.bashrc"
    __found="$(cat "$__brc" | grep "$__env_file_name" >/dev/null 2>&1 || true )"
    if [ -z "$__found" ]; then
        log_info "Sourcing Conan shell configuration in ${env_file}"
        echo >> $__brc
        echo '# Conan configuration' >> $__brc
        echo "source ~/$__env_file_name" >> $__brc
        echo >> $__brc
    fi
    set -e

    log_info "Export successful"
    log_info "-----------------------------------------------------"
    log_info "Restart your shell to run 'conan' commands directly."
    log_info "-----------------------------------------------------"
elif [ ! -z "$PS1" ]; then
    log_info '-----------------------------------------------------------------'
    log_info "To use the 'conan' command directly without needing to source"
    log_info "this script, re-run the script with the '-e' option, which will"
    log_info "export the shell configuration to your .bashrc."
    log_info
    log_info 'Note that this is not normally required, but can be useful.'
    log_info '-----------------------------------------------------------------'
fi

