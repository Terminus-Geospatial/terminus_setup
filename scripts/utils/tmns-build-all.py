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
#    File:    tmns-build-all.py
#    Author:  Marvin Smith
#    Date:    8/2/2024
#
#    Purpose:  Build tmns applications in a more advanced way

#  Python Standard Libraries
import argparse
import configparser
import logging
import os
import subprocess


# Global Const Value
DEFAULT_PROFILE_PATH='tmns-profile.cfg'

DEFAULT_REPO_LIST = ['terminus-cmake',
                     'terminus-log',
                     'terminus-outcome',
                     'terminus-core',
                     'terminus-math',
                     'terminus-nitf',
                     'terminus-image',
                     'terminus-cpp-demos']

class TerminusRepo:

    def __init__( self,
                  repo_name,
                  repo_path,
                  build_modes,
                  clean_repo,
                  build_missing ):
        self.repo_name     = repo_name
        self.repo_path     = repo_path
        self.build_modes   = build_modes
        self.clean_repo    = clean_repo
        self.build_missing = build_missing

        #  Build modes, if none, will get both release and debug
        if len(self.build_modes) == 0:
            self.build_modes = ['release','debug']

        #  Clean always if more than one build mode
        if len(self.build_modes) > 1:
            self.clean_repo = True

    def get_build_command( self, build_mode, clean_repo, build_missing ):

        build_flags = { 'release': '-r',
                        'debug': '' }

        clean_flag = { True: '-c',
                       False: '' }

        bm_flag = { True: '--build-missing',
                    False: '' }

        cmd = f'conan-build.sh {build_flags[build_mode]} {clean_flag[clean_repo]} {bm_flag[build_missing]}'

        return cmd

    def build( self ):

        logger = logging.getLogger('Repo.build')

        #  Check if the directory is installed
        if os.path.exists( self.repo_path ) == False:
            logger.info( f'    {self.repo_name} not found. Skipping' )
            return

        #  Jump to repo
        orig_path = os.getcwd()
        os.chdir( self.repo_path )

        for build_mode in self.build_modes:
            build_cmd = self.get_build_command( build_mode    = build_mode,
                                                clean_repo    = self.clean_repo,
                                                build_missing = self.build_missing )
            logger.debug( f'Build Command: {build_cmd}' )

            ret = subprocess.run( build_cmd,
                                  shell=True,
                                  stdout=subprocess.PIPE )

            if ret.returncode != 0:
                logging.error( 'Failed to build.  Details: ' + ret.stdout.decode() )
                return False

        #  Back up
        os.chdir(orig_path)

        return True

    def to_log_string(self, offset = 4 ):

        gap = ' ' * offset
        output  = gap +  '- Repo\n'
        output += gap + f'    - Name: {self.repo_name}\n'
        output += gap + f'    - Path: {self.repo_path}\n'
        output += gap + f'    - Build Modes: {self.build_modes}\n'
        output += gap + f'    - Clean Repo: {self.clean_repo}\n'
        return output

class TerminusProfile:

    def __init__(self, repos):
        self.repos = repos

    def to_log_string(self):

        output  =  'Terminus Profile:\n'
        output += f'    repos (cnt: {len(self.repos)})\n'
        for repo in self.repos:
            output += repo.to_log_string( 4 )
        return output


def load_profile( profile_path,
                  ignore_profiles,
                  build_modes,
                  clean_repos,
                  build_missing ):

    print( f'Ignore Profiles: {ignore_profiles}' )
    #  If the user provided a profile and it doesn't exist, exit now
    if profile_path != None and os.path.exists( profile_path ) == False:
        print( f'User provided profile ({profile_path}) does not exist. Exiting.' )
        return None

    #  Otherwise, if the profile is none, look for a default profile
    elif profile_path is None and ( ignore_profiles != True and os.path.exists( DEFAULT_PROFILE_PATH ) == True):
        print( f'Found default profile ({DEFAULT_PROFILE_PATH}). Using that.' )
        profile_path = DEFAULT_PROFILE_PATH

    #  otherwise, use default repo and options
    elif profile_path is None or ignore_profiles:
        repos = []
        for repo in DEFAULT_REPO_LIST:
            repos.append( TerminusRepo( repo_name     = repo,
                                        repo_path     = repo,
                                        build_modes   = build_modes,
                                        clean_repo    = clean_repos,
                                        build_missing = build_missing ) )

        profile = TerminusProfile( repos = repos )
        return profile

    #  If we have a valid profile, parse it
    profile_cfg = configparser.ConfigParser()

    print( f'Loading Profile: {profile_path}' )
    profile_cfg.read( profile_path )

    repos = []

    #  Get the list of repos
    for repo in profile_cfg.get('app','repos').split('\n'):

        repo_name = repo.strip(' \n')

        #  Get repo block
        repo_info = profile_cfg[repo_name]

        #  Skip if build is set to false
        if repo_info.getboolean('build') == False:
            print( f' Skipping {repo_name} as profile wants to skip building' )
            continue

        repo_path       = repo_info.get('path')
        cfg_build_modes = repo_info.get('build_modes').split(',')
        cfg_clean_repo  = repo_info.getboolean('clean_repo')

        if not clean_repos is None:
            cfg_clean_repo = clean_repos

        repos.append( TerminusRepo( repo_name     = repo_name,
                                    repo_path     = repo_path,
                                    build_modes   = cfg_build_modes,
                                    clean_repo    = cfg_clean_repo,
                                    build_missing = build_missing ) )

    profile = TerminusProfile( repos = repos )

    return profile

def parse_command_line():

    parser = argparse.ArgumentParser( description='Build tmns libraries in sequence' )

    parser.add_argument( '-v',
                          dest = 'log_severity',
                          default = 'INFO',
                          required = False,
                          action = 'store_const',
                          const = 'DEBUG',
                          help = 'Log at debugging level' )

    parser.add_argument( '-r',
                         dest = 'build_modes',
                         action = 'append_const',
                         default=[],
                         const = 'release',
                         required= False,
                         help = 'Build in release mode.' )

    parser.add_argument( '-d',
                         dest = 'build_modes',
                         action = 'append_const',
                         const = 'debug',
                         required= False,
                         help = 'Build in debug mode.' )

    parser.add_argument( '-c',
                         dest = 'clean_repos',
                         action = 'store_true',
                         default = None,
                         required= False,
                         help = 'Clean repos when building.' )

    parser.add_argument( '-x',
                         dest = 'allow_failures',
                         default = False,
                         action = 'store_true',
                         help = 'Keep building repos even if others fail.' )

    parser.add_argument( '-p',
                         dest='profile_path',
                         default = None,
                         required = False,
                         help = 'Define a profile to use for setting up build.' )

    parser.add_argument( '--ignore-profiles',
                         default=False,
                         dest = 'ignore_profiles',
                         action = 'store_true',
                         required = False,
                         help = 'Default behavior is to look for tmns-profile.cfg in the local filesystem.  This skips that.' )

    parser.add_argument( '-l', '--log-path',
                         dest = 'log_file_path',
                         default = None,
                         required = False,
                         help = 'Write output to log path.' )

    parser.add_argument( '--build-missing',
                         dest = 'build_missing',
                         action = 'store_true',
                         default = False,
                         help = 'Tell build system to build missing repos' )

    return parser.parse_args()

def configure_logging( options ):

    severity = logging.getLevelName( options.log_severity )

    if options.log_file_path is None:
        logging.basicConfig( level = severity )
    else:
        logging.basicConfig( level = severity, filename = options.log_file_path )
    logging.debug( 'Logger Initialized' )

def main():

    cmd_args = parse_command_line()

    #  Load the profile, if desired
    profile = load_profile( cmd_args.profile_path,
                            cmd_args.ignore_profiles,
                            cmd_args.build_modes,
                            cmd_args.clean_repos,
                            cmd_args.build_missing )

    #  Exit if task failed
    if profile is None:
        return 1

    #  Setup Logging
    configure_logging( cmd_args )
    logger = logging.getLogger( 'tmns-build-all' )

    logger.info( f'Build Modes: {cmd_args.build_modes}' )

    for repo in profile.repos:
        logger.info( f'    Building: {repo.repo_name}' )

        res = repo.build()

        if cmd_args.allow_failures == False and res == False:
            logger.error( 'Halting Build' )
            return 1


if __name__ == '__main__':
    main()