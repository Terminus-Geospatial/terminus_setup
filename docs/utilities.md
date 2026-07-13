---
title: Utility Scripts
layout: default
nav_order: 5
---

# Utility Scripts

This page lists all the scripts in the repository, where they live, and what they do.

## Top-level scripts

### `setup-terminus.py`

Main entry point for setting up a Terminus development environment. It creates a Python virtual environment, installs Conan, copies helper scripts into `~/.local/bin`, and configures the shell with the `go-conan` helper.

See [Setup]({% link setup.md %}) for full usage details.

## Conan scripts (`scripts/utils/`)

### `conan-setup.bash`

Installs and configures Conan. It can be executed directly or sourced to modify the current shell. It detects a default Conan profile, applies OS-specific configuration, and optionally exports the environment to `.bashrc`.

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Show help |
| `--python <cmd>` | Python command to use |
| `-c <key>-<value>` | Override a configuration value |
| `-m`, `--minimal` | Skip Conan installation; just configure environment |
| `-u`, `--upgrade` | Upgrade Conan if already installed |
| `-e`, `--export` | Export shell configuration to `.bashrc` |

Configuration is read from `scripts/utils/conan-setup.cfg` and optionally from `~/.conan-setup.cfg`.

### `conan-build.sh`

Builds a single Conan project. See [Building]({% link building.md %}) for options and examples.

### `conan-deploy.sh`

Deploys a Conan package to a local installation directory. See [Building]({% link building.md %}) for options and examples.

### `conan-utils.bash`

Bash helper functions used by the other Conan scripts:

- `getFullGitBranchNameFunc()` - Returns the current Git branch name.
- `getAppNameFromConanfileFunc()` - Extracts the package name from a `conanfile.py`.
- `getAppVersionFromConanfileFunc()` - Extracts the package version from a `conanfile.py`.

### `conan-setup.cfg`

Default configuration file for `conan-setup.bash`. Currently defines the Conan profile to use:

```bash
conan_setup_profile="default"
```

## Python helper scripts (`scripts/utils/`)

### `tmns-clone-repos.py`

Clones Terminus repositories from a profile. See [Repositories]({% link repositories.md %}) for details.

### `tmns-build-all.py`

Builds all repositories in a profile in sequence. See [Building]({% link building.md %}) for details.

### `tmns-profile-info.py`

Inspects or generates Terminus workspace profiles.

| Option | Description |
|--------|-------------|
| `-p <path>`, `--profile-path <path>` | Profile file to read or write |
| `--create-default` | Write a default profile to the specified path |

### `tmns-create-file.py`

Creates new source files with the standard Terminus header and template content. Supported file types are C++ source and header files (`.cpp` and `.hpp`).

| Option | Description |
|--------|-------------|
| `-t <type>` | File type (`cpp`, `hpp`, `py`, `cmake`) |
| `-i`, `--interactive` | Force interactive prompts |
| `--ns <namespace>` | C++ namespace (default: `tmns`) |
| `--author <name>` | Author name (default: `Marvin Smith`) |
| `--purpose <text>` | Purpose or description for the file header |
| `--class <name>` | Class name to add to the template |
| `<output_path>` | Destination path for the new file |

## Bash helper scripts (`scripts/utils/`)

### `log.bash`

Provides colored logging functions for use in other Bash scripts. The available log level is controlled by the `TERMINUS_LOG_LEVEL` or `TERMINUS_VERBOSE` environment variables.

Functions: `log_debug`, `log_trace`, `log_info`, `log_warn`, `log_error`.

### `tmns_bash_aliases.bash`

Defines shell aliases and helper functions. Currently includes:

- `tmns-build-clean` - Removes all `build` directories recursively from the current directory.

## Configuration samples

### `scripts/utils/config/sample-build-config.cfg`

A sample profile for `tmns-build-all.py`. It demonstrates how to define repositories, build modes, clean flags, and tags. Copy this file to create your own build profile.
