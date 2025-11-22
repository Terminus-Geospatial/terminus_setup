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
    'terminus_setup': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_setup.git',
        'default_branch': 'main',
        'tags': ['tools'],
    },
    'terminus_cmake': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_cmake.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp', 'cmake', 'build'],
    },
    'terminus_log': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_log.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp', 'log'],
    },
    'terminus_outcome': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_outcome.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp', 'error'],
    },
    'terminus_core': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_core.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus_math': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_math.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus_fcs': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_fcs.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus_coord': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_coord.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus_nitf': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_nitf.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus_image': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_image.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus_cpp_demos': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_cpp_demos.git',
        'default_branch': 'main',
        'tags': ['tools', 'cpp'],
    },
    'terminus_docs': {
        'url': 'git@github.com:Terminus-Geospatial/terminus_docs.git',
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

