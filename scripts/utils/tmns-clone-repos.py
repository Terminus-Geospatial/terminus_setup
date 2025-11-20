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
#    File:    tmns-clone-repos.py
#    Author:  Marvin Smith
#    Date:    11/19/2025
#

#  Python Libraries
import argparse
import configparser
import logging
import os

from tmns.default_profiles import default_profile
from tmns.profile import Profile, Repo

DEFAULT_PROFILE_PATH = "tmns-profile.cfg"

def load_profile( profile_path = None ) -> Profile:

    if profile_path is None:
        profile_path = DEFAULT_PROFILE_PATH

    if os.path.exists( profile_path ):

        cfg = configparser.ConfigParser()
        cfg.read( profile_path )

        project_name = cfg.get( 'profile', 'project_name', fallback = 'Unknown Profile' )

        repos = []
        for section in cfg.sections():
            if section == 'profile':
                continue

            repo_name = cfg.get( section, 'repo_name', fallback = section )
            build     = cfg.getboolean( section, 'build', fallback = True )
            repo_url  = cfg.get( section, 'repo_url', fallback = '' )
            branch    = cfg.get( section, 'branch_name', fallback = 'main' )
            tags_raw  = cfg.get( section, 'tags', fallback = '' )
            tags      = [ tag.strip() for tag in tags_raw.split(',') if tag.strip() ]

            repos.append( Repo( repo_name   = repo_name,
                                build       = build,
                                repo_url    = repo_url,
                                branch_name = branch,
                                tags        = tags ) )

        return Profile( project_name = project_name,
                        repos        = repos )

    return default_profile()

def parse_command_line():

    parser = argparse.ArgumentParser( description='Clone all repos for the primary Terminus "stack".')

    tag_list = []
    profile = load_profile()
    for repo in profile.repos:
        for tag in repo.tags:
            if not tag in tag_list:
                tag_list.append( tag )

    parser.add_argument( '-v',
                          dest = 'log_level',
                          default = logging.INFO,
                          required = False,
                          action = 'store_const',
                          const = logging.DEBUG,
                          help = 'Log at debugging level' )

    parser.add_argument( '-l', '--log-path',
                         dest = 'log_file_path',
                         default = None,
                         required = False,
                         help = 'Write output to log path.' )

    parser.add_argument( '--all',
                         dest = 'repo_set',
                         default = 'all',
                         action = 'store_const',
                         const = 'all',
                         help = 'Clone all repos for the project.' )

    parser.add_argument( '-t',
                         dest = 'tags',
                         action = 'append',
                         default=[],
                         required= False,
                         help = f'Clone repos with a specific tag. Expected Tags: {tag_list}' )

    return parser.parse_args()

def configure_logging( options ):

    if options.log_file_path is None:
        logging.basicConfig( level = options.log_level )
    else:
        logging.basicConfig( level = options.log_level, filename = options.log_file_path )

def main():

    #  Load command-line arguments
    cmd_args = parse_command_line()

    #  Setup logging
    configure_logging( cmd_args )

    profile = load_profile()

    #  Iterate over repo list
    for repo in profile.repos:

        if len( cmd_args.tags ) > 0:
            matched = False
            for tag in repo.tags:
                if tag in cmd_args.tags:
                    matched = True
                    break
            if matched is False:
                continue

        repo_url     = repo.repo_url
        repo_name    = repo.repo_name
        branch_name  = repo.branch_name

        #  Skip cloning if the destination directory already exists
        if os.path.exists( repo_name ):
            logging.info( f"Skipping clone of '{repo_name}' because directory already exists (expected branch '{branch_name}')." )
            continue

        clone_cmd = f'git clone {repo_url} {repo_name}'
        logging.debug( f'Command: {clone_cmd}' )
        os.system( clone_cmd )

        #  Checkout the requested branch
        checkout_cmd = f'git -C {repo_name} checkout {branch_name}'
        logging.debug( f'Command: {checkout_cmd}' )
        os.system( checkout_cmd )

if __name__ == '__main__':
    main()
