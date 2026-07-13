---
title: Setup
layout: default
nav_order: 2
---

# Setup

## Prerequisites

### System requirements

- **Python**: 3.10 or higher
- **Git**: For cloning repositories
- **CMake**: For building C++ projects
- **C++ compiler**: GCC 9+ or Clang 10+

### Platform-specific dependencies

#### Fedora / RHEL / CentOS

```bash
sudo dnf install cmake g++ gdal-devel opencv-devel python3
```

#### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install cmake build-essential libgdal-dev libopencv-dev python3
```

#### macOS

```bash
brew install cmake python
```

This installs the latest stable Python 3 release. The `python3` command should be available in your PATH after installation.

```bash
python3 --version
```

#### Windows (WSL2)

Use WSL2 and follow the Ubuntu/Debian instructions inside the WSL2 environment.

### Important notes

- **GDAL and OpenCV** must be installed via the system package manager because they are not configured through Conan.
    - This is possible, but tricky due to the number of dependencies each packages.
- The setup script creates a Python virtual environment at `${HOME}/conan` by default.
- The setup process modifies your shell RC file (`.bashrc` or `.zshrc`).

## Initial setup

Run the main setup script to create the Conan environment:

```bash
./setup-terminus.py -p python3
```

### Options

| Option | Description |
|--------|-------------|
| `-p <python_version>` | Python executable to use (default: `python3`) |
| `--venv-path <path>` | Custom virtual environment path (default: `${HOME}/conan`) |
| `--dry-run` | Show commands without executing them |
| `--skip-conan` | Skip Conan installation and environment setup |
| `--skip-shell` | Do not modify shell RC files |
| `--bash` | Update `.bashrc` explicitly |
| `--zsh` | Update `.zshrc` explicitly |
| `-v` | Verbose logging |

The script performs the following:

1. Copies helper scripts from `scripts/utils/` into `~/.local/bin`.
2. Creates a Python virtual environment at the configured path.
3. Installs the latest Conan release into the virtual environment.
4. Adds the `go-conan` helper function to your shell RC file.

## Activate the Conan environment

After setup, restart your terminal or source the updated RC file:

```bash
source ~/.zshrc   # macOS default
source ~/.bashrc  # Linux default
```

Then activate the environment with:

```bash
go-conan
```

You can also activate the virtual environment directly:

```bash
source ${HOME}/conan/bin/activate
```

## Configure Conan profile

Create a default Conan profile:

```bash
conan profile detect
```

This creates a default profile at `~/.conan2/profiles/default`. For advanced configuration, edit that file directly.

## Next steps

- Clone the Terminus repositories: [Repositories]({% link repositories.md %})
- Build the ecosystem: [Building]({% link building.md %})
