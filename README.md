# Terminus Setup

This repository provides the necessary tools and scripts for setting up the development environment required to build and install Terminus C++ applications and libraries.

## Overview

Terminus C++ APIs are designed to be built using Conan for dependency management. While not explicitly required, Conan offers significant benefits, particularly around versioning and reproducible builds.

### What's Included

- **Conan Setup**: Automated installation and configuration of Conan package manager
- **Repository Management**: Tools for cloning and managing multiple Terminus repositories
- **Build Automation**: Scripts for building the entire Terminus ecosystem
- **Profile Management**: Configuration system for different development setups
- **Utility Scripts**: Various helper scripts for common development tasks

### Repository Structure

```
terminus_setup/
├── setup-terminus.py          # Main setup script for Conan environment
├── scripts/utils/             # Utility scripts directory
│   ├── conan-setup.bash       # Conan installation and configuration
│   ├── tmns-clone-repos.py    # Repository cloning tool
│   ├── tmns-build-all.py      # Build automation script
│   ├── tmns-profile-info.py   # Profile information utility
│   └── config/                # Configuration files
│       └── sample-build-config.cfg
└── README.md                  # This file
```

## Prerequisites

### System Requirements

- **Python**: 3.10 or higher
- **Git**: For cloning repositories
- **CMake**: For building C++ projects
- **C++ Compiler**: GCC 9+ or Clang 10+

### Platform-Specific Dependencies

#### Fedora/RHEL/CentOS

For RHEL/Fedora/CentOS users, the following will install the core dependencies:

```bash
sudo dnf install cmake g++ gdal-devel opencv-devel python3.13
```

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install cmake build-essential libgdal-dev libopencv-dev python3.13
```

#### macOS

Use Homebrew to setup required dependencies:

```bash
brew install cmake python3.13
```

#### Windows (WSL2)

It's recommended to use WSL2 on Windows. Follow the Ubuntu/Debian instructions once WSL2 is set up.

### Important Notes

- **GDAL and OpenCV**: These libraries currently need to be installed via system package managers as they are not available through Conan
- **Virtual Environment**: The setup script creates a Python virtual environment at `${HOME}/conan`
- **Shell Configuration**: The setup process modifies your shell RC file (`.bashrc` or `.zshrc`)

## Installation Guide

### Step 1: Setup Conan Environment

If you already have Conan installed and configured, you can skip this step. Otherwise, run the following command to set up Conan in a dedicated virtual environment:

```bash
./setup-terminus.py -p python3.14
```

**Options:**
- `-p <python_version>`: Specify Python version (default: `python3`)
- `--venv-path <path>`: Custom virtual environment path (default: `${HOME}/conan`)
- `--dry-run`: Show commands without executing them
- `--skip-conan`: Skip Conan setup only
- `-v`: Verbose output

This script will:
- Create a Python virtual environment at `${HOME}/conan` using the specified Python version
- Install the latest version of Conan in the virtual environment
- Add the `go-conan` helper function to your shell RC file (if not already present)

### Step 2: Restart Your Shell

The setup script modifies your shell configuration. You'll need to restart your terminal or source the appropriate RC file:

**For ZSH (macOS default):**
```bash
source ~/.zshrc
```

**For Bash (Linux default):**
```bash
source ~/.bashrc
```

### Step 3: Activate Conan Environment

After restarting your shell, you can activate the Conan environment using the helper command:

```bash
go-conan
```

This will activate the virtual environment at `${HOME}/conan` and make the `conan` command available.

**Alternative manual activation:**
```bash
source ${HOME}/conan/bin/activate
```

### Step 4: Configure Conan Profile

Conan requires a profile before you can start using it. Initialize your profile:

```bash
conan profile detect
```

This creates a default profile using ConanCenter as the remote repository. For advanced configuration, you can manually edit the profile at `~/.conan2/profiles/default`.

## Repository Management

### Step 5: Clone Terminus Repositories

This repository includes a command-line tool for cloning all Terminus repositories in a single operation:

```bash
cd ../  # Navigate to your desired development directory
tmns-clone-repos.py -vv --all
```

#### Repository Cloning Options

The `tmns-clone-repos.py` script supports several options:

- `--all`: Clone all repositories in the default profile
- `-vv`: Verbose output for debugging
- `--tags <tags>`: Clone only repositories with specific tags
- `--profile <path>`: Use a custom profile configuration

#### Default Repository List

The default profile includes the following repositories:

**Core Libraries:**
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

**Applications and Tools:**
- `terminus_cpp_demos` - C++ demonstration applications
- `terminus_docs` - Documentation repository
- `terminus_setup` - Setup and configuration tools

## Building Terminus

### Using the Build Automation Script

Once repositories are cloned, you can build the entire ecosystem using the automated build script:

```bash
tmns-build-all.py --config tmns-profile.cfg
```

#### Build Configuration

The build process is controlled by configuration files that specify:
- Which repositories to build
- Build modes (debug, release, etc.)
- Clean build options
- Repository-specific settings

Sample configuration files are available in `scripts/utils/config/`.

#### Build Modes

Supported build modes include:
- `debug` - Debug build with symbols
- `release` - Optimized release build
- `relwithdebinfo` - Release with debug information

## Advanced Usage

### Custom Profiles

You can create custom profiles for different development scenarios:

1. Copy the sample configuration:
   ```bash
   cp scripts/utils/config/sample-build-config.cfg my-profile.cfg
   ```

2. Modify the profile to suit your needs:
   - Enable/disable specific repositories
   - Set custom build modes
   - Configure repository URLs and branches

3. Use your custom profile:
   ```bash
   tmns-clone-repos.py --profile my-profile.cfg
   tmns-build-all.py --config my-profile.cfg
   ```

### Utility Scripts

Several utility scripts are available for common tasks:

- `tmns-profile-info.py` - Display profile information
- `tmns-create-file.py` - Create new files with proper headers
- `conan-utils.bash` - Conan utility functions
- `log.bash` - Logging utilities for shell scripts

## Troubleshooting

### Common Issues

**Conan not found:**
- Ensure you've activated the Conan environment with `go-conan`
- Check that `${HOME}/conan/bin/activate` exists

**Build failures:**
- Verify all system dependencies are installed
- Check that your C++ compiler is compatible
- Ensure Conan profile is properly configured

**Repository cloning issues:**
- Verify SSH keys are configured for Git access
- Check network connectivity
- Ensure you have proper repository permissions

### Getting Help

For additional help:
1. Check the changelog for recent updates: `changelog.md`
2. Review sample configuration files in `scripts/utils/config/`
3. Use verbose output (`-vv`) for debugging
4. Check the Terminus documentation repository after cloning

## Version Information

Current version: **1.0.0** (2026-01-11)

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

