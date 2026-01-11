#!/usr/bin/env python3
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
#       File:    setup-terminus.py
#       Author:  Marvin Smith
#       Date:    11/19/2025
#

#  Python Standard Libraries
import argparse
import logging
import os
import shutil
import subprocess
import sys

DEFAULT_VENV_PATH = os.path.join( os.environ.get("HOME"), 'conan' )

LOG_FORMAT = '%(asctime)s - %(levelname)-8s - %(message)s'

def is_valid_python(string):

    #  If it's a root-relative python version,
    pyversion = subprocess.run([string,'--version'], check=True, capture_output=True).stdout.decode('utf-8')
    logging.info( f'Python ({string}) version: {pyversion.split(" ")[1].strip()}' )
    return string


def parse_command_line():

    parser = argparse.ArgumentParser( description = 'Setup Virtual Environment for Terminus Apps.' )

    parser.add_argument( '-v', '--verbose',
                         dest = 'log_level',
                         default = logging.INFO,
                         action = 'store_const',
                         const = logging.DEBUG,
                         help = 'Use verbose logging' )

    parser.add_argument( '--venv-path',
                         dest = 'venv_path',
                         default = DEFAULT_VENV_PATH,
                         help = 'Where to install Python VENV' )

    parser.add_argument( '-o',
                         '--create-if-exists',
                         dest = 'create_if_exists',
                         default = False,
                         action = 'store_true',
                         help = 'Create environment even if it exists.' )

    parser.add_argument( '-p', '--python',
                         dest = 'python_path',
                         default = 'python3',
                         type = is_valid_python,
                         help = 'Python installation' )

    parser.add_argument( '--dry-run',
                         dest = 'dry_run',
                         default = False,
                         action = 'store_true',
                         help = 'Print commands which would be executed, then exit.' )

    parser.add_argument( '--skip-conan',
                         dest = 'skip_conan',
                         default = False,
                         action = 'store_true',
                         help = 'Skip Conan setup.' )

    parser.add_argument( '--skip-shell',
                         dest = 'skip_shell',
                         default = False,
                         action = 'store_true',
                         help = 'Do not modify shell RC files.' )

    parser.add_argument( '--bash',
                         dest = 'use_bash',
                         default = False,
                         action = 'store_true',
                         help = 'Update ~/.bashrc for helper scripts.' )

    parser.add_argument( '--zsh',
                         dest = 'use_zsh',
                         default = False,
                         action = 'store_true',
                         help = 'Update ~/.zshrc for helper scripts.' )

    return parser.parse_args()

def run_command( logger, command, desc, dry_run, exit_if_fail = True ):

    if dry_run:
        logger.info( f'command: {command}' )
    else:
        logger.debug( f'command: {command}' )
        result = subprocess.run( command, shell = True, check = True, capture_output = True )
        if result.returncode != 0:
            logger.error( f'Unable to properly {desc}: ',
                          result.stdout.decode('utf-8') )
            if exit_if_fail:
                sys.exit(1)
        logger.debug( result.stdout.decode('utf-8'))

def removing_existing( logger, venv_path, dry_run ):

    logger.info( f'Removing existing environment' )
    cmd = f'rm -rv {venv_path}'
    run_command( logger, cmd, 'delete existing environment', dry_run )


def build_virtual_environment( logger, venv_path, python_path, dry_run ):

    logger.info( f'Building new Virtual Environment' )
    cmd = f'{python_path} -m venv {venv_path}'
    run_command( logger, cmd, 'creating new venv', dry_run )

def setup_virtual_environment( logger, python_path, venv_path, dry_run ):

    cmd = f'. {venv_path}/bin/activate && pip install --upgrade pip'
    run_command( logger, cmd, 'updating pip', dry_run )

    cmd = f'. {venv_path}/bin/activate && pip install conan'
    run_command( logger, cmd, 'installing conan', dry_run )

def update_tmns_shell( logger, shell_path, dry_run ):

    if not os.path.exists( shell_path ):
        logger.warning( f'Shell RC file does not exist: {shell_path}' )
        return

    logger.info( f'Updating {shell_path}' )

    with open( shell_path, 'r' ) as fin:
        text = fin.read()

    home_dir = os.environ.get( "HOME" )
    local_bin = os.path.join( home_dir, '.local', 'bin' )
    path_value = os.environ.get( 'PATH', '' )

    if local_bin in path_value.split( ':' ):
        logger.info( f'{local_bin} is already in PATH.' )
    else:
        logger.info( f'{local_bin} is not in PATH; adding.' )
        line = 'export PATH="${HOME}/.local/bin:${PATH}"\n'
        if dry_run:
            logger.info( f'Would append PATH update to {shell_path}' )
        else:
            with open( shell_path, 'a' ) as fout:
                fout.write( line )

    if 'tmns-import' in text:
        logger.info( 'tmns-import already defined. skipping' )
    else:
        logger.info( f'tmns-import is not defined.  Adding to {shell_path}' )
        block = '\n# Added by terminus-repo-utilities: install-local.bash\nfunction tmns-import() {\n   source ${HOME}/.local/bin/tmns_bash_aliases.bash\n}\n'
        if dry_run:
            logger.info( f'Would append tmns-import function to {shell_path}' )
        else:
            with open( shell_path, 'a' ) as fout:
                fout.write( block )

def install_helper_scripts( logger, dry_run, skip_shell, use_bash, use_zsh ):

    home_dir = os.environ.get( "HOME" )
    if home_dir is None:
        logger.error( 'HOME environment variable is not set.' )
        return

    scripts_dir = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), 'scripts' )
    source_dir = os.path.join( scripts_dir, 'utils' )

    if not os.path.isdir( source_dir ):
        logger.error( f'Utilities source directory not found: {source_dir}' )
        return

    dest_dir = os.path.join( home_dir, '.local', 'bin' )
    logger.info( f'Installing helper scripts from {source_dir} to {dest_dir}' )

    if dry_run:
        logger.info( 'Dry-run enabled; not copying files or updating shell configuration.' )
    else:
        os.makedirs( dest_dir, exist_ok = True )

        for root, dirs, files in os.walk( source_dir ):
            rel_root = os.path.relpath( root, source_dir )
            target_root = dest_dir if rel_root == '.' else os.path.join( dest_dir, rel_root )
            os.makedirs( target_root, exist_ok = True )
            for filename in files:
                src_path = os.path.join( root, filename )
                dst_path = os.path.join( target_root, filename )
                shutil.copy2( src_path, dst_path )

    if skip_shell:
        return

    shell_paths = []

    if use_bash:
        shell_paths.append( os.path.join( home_dir, '.bashrc' ) )
    if use_zsh:
        shell_paths.append( os.path.join( home_dir, '.zshrc' ) )

    if not shell_paths:
        for candidate in [ '.zshrc', '.bashrc' ]:
            candidate_path = os.path.join( home_dir, candidate )
            if os.path.exists( candidate_path ):
                shell_paths.append( candidate_path )

    for shell_path in shell_paths:
        update_tmns_shell( logger, shell_path, dry_run )

def run_conan_setup( logger, python_path, venv_path, dry_run ):

    # Check if virtual environment already exists
    if os.path.exists( venv_path ):
        logger.info( f'Virtual environment already exists at {venv_path}' )
    else:
        logger.info( f'Creating virtual environment at {venv_path}' )
        build_virtual_environment( logger, venv_path, python_path, dry_run )

    # Setup the virtual environment and install conan
    setup_virtual_environment( logger, python_path, venv_path, dry_run )

    # Add go-conan alias to shell
    update_shell_scripts( logger, venv_path, dry_run )

def update_shell_scripts( logger, venv_path, dry_run ):

    #  Iterate over available scripts
    for shell_rc in [ f'{os.environ.get("HOME")}/.bashrc', f'{os.environ.get("HOME")}/.bash_profile', f'{os.environ.get("HOME")}/.zshrc' ]:

        if os.path.exists( shell_rc ):

            #  Only update if RC file actually exists
            logger.info( f'Updating: {shell_rc}' )

            #  Check if shell script has the import function already
            add_command = False
            with open( shell_rc, 'r' ) as fin:
                text = fin.read()
                if 'go-conan' in text:
                    logger.warning( f'The command "go-conan" already in {shell_rc}' )
                else:
                    add_command = True

            if add_command:
                cmd  = f'\necho "# This function added by Terminus setup-conan script." >> {shell_rc}\n'
                cmd += f'echo "function go-conan() {{" >> {shell_rc}\n'
                cmd += f"echo '    . {venv_path}/bin/activate' >> {shell_rc}\n"
                cmd += f"echo '}}' >> {shell_rc}"
                run_command( logger, cmd, 'adding conan alias', dry_run )

def main():

    logging.basicConfig( level = logging.INFO, format = LOG_FORMAT )
    logger = logging.getLogger( 'terminus-setup' )

    cmd_args = parse_command_line()

    #  Setup logging
    logger.setLevel( cmd_args.log_level )
    logger.debug( 'Running Terminus setup tool' )

    #  Check if environment already is setup
    install_helper_scripts( logger,
                            cmd_args.dry_run,
                            cmd_args.skip_shell,
                            cmd_args.use_bash,
                            cmd_args.use_zsh )

    if cmd_args.skip_conan:
        logger.info( 'Skipping Conan setup.' )
    else:
        run_conan_setup( logger,
                         cmd_args.python_path,
                         cmd_args.venv_path,
                         cmd_args.dry_run )

if __name__ == '__main__':
    main()
