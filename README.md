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
./setup-terminus.py
```

This script will:
- Create a Python virtual environment in `${HOME}/conan`
- Install the latest version of Conan
- Add helper functions to your shell RC file

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

After restarting your shell, you can activate the Conan environment using either method:

1. **Using the helper command:**
   ```bash
   go-conan
   ```

2. **Manual activation:**
   ```bash
   source ${HOME}/conan/bin/activate
   ```

### Step 4: Configure Conan Profile

Conan requires a profile before you can start using it. Run the setup script to configure default settings:

```bash
conan-setup.bash
```

This will:
- Update your shell RC files with necessary environment variables
- Set up default Conan configuration
- Configure the ConanCenter remote

After running this, restart your shell again or source the RC file, then initialize your profile:

```bash
conan profile detect
```

This creates a default profile using ConanCenter as the remote repository.

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
- `terminus-cmake` - CMake utilities and macros
- `terminus-log` - Logging framework
- `terminus-outcome` - Result handling utilities
- `terminus-core` - Core C++ primitives
- `terminus-math` - Mathematical library
- `terminus-nitf` - NITF file format support
- `terminus-image` - Image processing library
- `terminus-astro` - Astro library
- `terminus-platform-lib-cpp` - Platform C++ library
- `terminus-toolbox` - Toolbox library

**Applications and Tools:**
- `terminus-cpp-demos` - C++ demonstration applications
- `terminus-docs` - Documentation repository
- `terminus-repo-utilities` - Repository management tools

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

