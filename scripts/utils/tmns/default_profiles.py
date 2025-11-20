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
#    File:    default_profiles.py
#    Author:  Marvin Smith
#    Date:    11/19/2025
#
#    Purpose:  Define default Terminus repo metadata and profiles.

#  Python Standard Libraries

from tmns.profile import Profile, Repo


DEFAULT_REPO_LIST = {
    'terminus-setup': {
        'url': 'git@github.com:Terminus-Geospatial/terminus-setup.git',
        'default_branch': 'main',
        'tags': ['tools'],
    },
    'terminus-cmake': {
        'url': 'git@github.com:Terminus-Geospatial/terminus-cmake.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp', 'cmake', 'build'],
    },
    'terminus-log': {
        'url': 'git@github.com:Terminus-Geospatial/terminus-log.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp', 'log'],
    },
    'terminus-outcome': {
        'url': 'git@github.com:Terminus-Geospatial/terminus-outcome.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp', 'error'],
    },
    'terminus-core': {
        'url': 'git@bitbucket.org:msmith81886/terminus-core',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus-math': {
        'url': 'git@bitbucket.org:msmith81886/terminus-math',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus-coord': {
        'url': 'git@github.com:Terminus-Geospatial/terminus-coord.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus-nitf': {
        'url': 'git@bitbucket.org:msmith81886/terminus-nitf',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus-image': {
        'url': 'git@bitbucket.org:msmith81886/terminus-image',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus-cpp-demos': {
        'url': 'git@bitbucket.org:msmith81886/terminus-cpp-demos',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus-docs': {
        'url': 'git@github.com:Terminus-Geospatial/terminus-docs.git',
        'default_branch': 'main',
        'tags': ['docs'],
    },
}


def default_repo_list():
    """
    Returns a list of default repos for the Terminus toolchain
    """
    repos = []

    for repo_name, cfg in DEFAULT_REPO_LIST.items():
        repos.append(Repo(
            repo_name=repo_name,
            build=True,
            repo_url=cfg['url'],
            branch_name=cfg['default_branch'],
            tags=cfg['tags'],
        ))

    return repos

def default_profile():
    '''
    Creates a default profile the user can use to make a profile document.
    '''

    return Profile(
        project_name='Terminus Workspace',
        repos=default_repo_list(),
    )

