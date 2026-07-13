# Terminus Setup

This repository provides the tools and scripts needed to set up the development environment for building and installing Terminus C++ applications and libraries.

[View the documentation on GitHub Pages](https://Terminus-Geospatial.github.io/terminus_setup)

## Overview

Terminus C++ APIs are designed to be built using [Conan](https://conan.io/) for dependency management. While not required, Conan offers significant benefits around versioning and reproducible builds.

## Capabilities

- **Conan environment setup**: Create a Python virtual environment, install Conan, and configure shell integration.
- **Repository management**: Clone the Terminus ecosystem from a profile.
- **Build automation**: Build individual projects or the entire Terminus stack.
- **Deployment**: Deploy built Conan packages to local installation directories.
- **Profile management**: Create and inspect workspace profiles.
- **Helper utilities**: File templates, Conan helper functions, logging, and shell aliases.

## Quick Start

1. Install the system dependencies listed in the [setup documentation](https://Terminus-Geospatial.github.io/terminus_setup/setup/).
2. Run `./setup-terminus.py` to create the Conan environment.
3. Restart your shell and run `go-conan` to activate the environment.
4. Clone the repositories: `tmns-clone-repos.py --all`
5. Build the ecosystem: `tmns-build-all.py`

## Documentation

Full documentation is published to GitHub Pages at:

<https://Terminus-Geospatial.github.io/terminus_setup>

The documentation source lives in the `docs/` folder. The rendered pages are:

- [Setup](https://Terminus-Geospatial.github.io/terminus_setup/setup/)
- [Repositories](https://Terminus-Geospatial.github.io/terminus_setup/repositories/)
- [Building](https://Terminus-Geospatial.github.io/terminus_setup/building/)
- [Utility Scripts](https://Terminus-Geospatial.github.io/terminus_setup/utilities/)
- [Troubleshooting](https://Terminus-Geospatial.github.io/terminus_setup/troubleshooting/)

## Version Information

Current version: **1.0.2** (2026-07-12)

See `changelog.md` for detailed version history and changes.

## TODO

### Future Enhancements

- [ ] **OS-Specific Configurations**: Extend the OS detection framework in `conan-setup.bash` to include platform-specific settings:
  - [ ] macOS: Configure Xcode toolchain paths
  - [ ] Linux: Set distribution-specific package manager paths
  - [ ] Windows: Configure Visual Studio environment
  - [ ] Cross-platform: Handle different compiler configurations

- [ ] **Profile Management**: Add profile backup and restore functionality
- [ ] **Remote Configuration**: Implement custom Conan remote setup for enterprise environments
- [ ] **Dependency Validation**: Add checks for required system dependencies before setup

### Known Issues

- [ ] GDAL and OpenCV must be installed via system package managers (not available through Conan)
- [ ] Windows support requires WSL2 for full functionality

