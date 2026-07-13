---
title: Repositories
layout: default
nav_order: 3
---

# Repository Management

The `tmns-clone-repos.py` script clones all Terminus repositories defined in a profile in a single operation.

## Clone all repositories

Run the script from the directory that will contain the repositories:

```bash
cd ../
tmns-clone-repos.py -vv --all
```

## Options

| Option | Description |
|--------|-------------|
| `--all` | Clone all repositories in the active profile |
| `-v` | Verbose logging |
| `-t <tag>` | Clone only repositories tagged with `<tag>` (can be repeated) |
| `-p <path>` | Use a custom profile file (default: `tmns-profile.cfg`) |
| `-l <path>` | Write output to a log file |

If a destination directory already exists, the script skips that repository.

## Profile format

A profile is an INI-style configuration file. Each repository has its own section, and a global `[profile]` section stores the project name:

```ini
[profile]
project_name = Terminus Workspace

[terminus_cmake]
repo_name = terminus_cmake
build = true
repo_url = git@github.com:Terminus-Geospatial/terminus_cmake.git
branch_name = main
tags = tools,cpp,cmake,build
```

Generate a default profile with:

```bash
tmns-profile-info.py --create-default -p my-profile.cfg
```

Inspect an existing profile with:

```bash
tmns-profile-info.py -p my-profile.cfg
```

## Default repositories

The default profile includes the following repositories:

### Core libraries

- `terminus_cmake` - CMake utilities and macros
- `terminus_log` - Logging framework
- `terminus_outcome` - Result handling utilities
- `terminus_core` - Core C++ primitives
- `terminus_math` - Mathematical library
- `terminus_ipc` - Inter-process communication library
- `terminus_fcs` - Framework Configuration Service
- `terminus_astro` - Astronomical calculations library
- `terminus_nitf` - NITF file format support
- `terminus_image` - Image processing library
- `terminus_platform_lib_cpp` - Platform C++ library
- `terminus_toolbox` - Terminus toolbox utilities

### Applications and tools

- `terminus_cpp_demos` - C++ demonstration applications
- `terminus_docs` - Documentation repository
- `terminus_setup` - Setup and configuration tools

## Tag filtering

Repositories are tagged with categories such as `tools`, `cpp`, `docs`, `build`, `log`, and `error`. Use the `-t` option to clone only the repositories that match a tag:

```bash
tmns-clone-repos.py -t tools
```
