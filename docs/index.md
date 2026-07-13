---
title: Home
layout: default
nav_order: 1
---

# Terminus Setup

This repository provides the tools and scripts needed to set up a development environment for building and installing Terminus C++ applications and libraries.

## Overview

Terminus C++ projects are built with [Conan](https://conan.io/) for dependency management. The scripts here automate the Conan environment, clone the Terminus ecosystem, and build and deploy applications in a consistent way.

## Capabilities

- **Environment setup**: `setup-terminus.py` creates a Python virtual environment, installs Conan, copies helper scripts into `~/.local/bin`, and wires shell shortcuts.
- **Conan setup**: `conan-setup.bash` installs and configures Conan, detects a default profile, and applies OS-specific settings.
- **Repository management**: `tmns-clone-repos.py` clones the Terminus repositories defined in a profile.
- **Build automation**: `conan-build.sh` builds a single Conan project, while `tmns-build-all.py` builds the entire profile in sequence.
- **Deployment**: `conan-deploy.sh` deploys a built Conan package to a local installation directory.
- **Profile management**: `tmns-profile-info.py` inspects existing profiles and creates default ones.
- **Helper utilities**: `tmns-create-file.py`, `conan-utils.bash`, `log.bash`, and `tmns_bash_aliases.bash` provide file templates, Conan helper functions, logging, and shell aliases.

## Quick Start

1. Install the system prerequisites listed in [Setup]({% link setup.md %}).
2. Run `./setup-terminus.py` to create the Conan environment.
3. Restart your shell and run `go-conan` to activate the environment.
4. Clone the Terminus repositories with `tmns-clone-repos.py --all`.
5. Build the ecosystem with `tmns-build-all.py`.

For details on each step, see the pages below.

## Documentation

- [Setup]({% link setup.md %}) - Install the Conan environment and system dependencies.
- [Repositories]({% link repositories.md %}) - Clone and manage Terminus repositories.
- [Building]({% link building.md %}) - Build the Terminus ecosystem.
- [Utility Scripts]({% link utilities.md %}) - Reference for all helper scripts.
- [Troubleshooting]({% link troubleshooting.md %}) - Common issues and fixes.
