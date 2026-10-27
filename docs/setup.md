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
5. Runs `conan-setup.bash` to detect/create a default Conan profile and configure remotes from `conan-setup.cfg` / `~/.conan-setup.cfg`.
6. Creates a default `~/.terminus/docker.env` file for `tmns-docker-build` credentials.

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

`setup-terminus.py` already runs `conan-setup.bash`, which detects/creates a default Conan profile and adds the remotes defined in `scripts/utils/conan-setup.cfg` (overridable via `~/.conan-setup.cfg`).

To re-run the Conan configuration manually from the repo:

```bash
bash scripts/utils/conan-setup.bash
```

This creates a default profile at `~/.conan2/profiles/default`. For advanced configuration, edit that file directly — except the `[options]` section, which is managed by `conan-setup.bash` (see below).

### Shared dependency options

`conan-setup.bash` regenerates a managed `[options]` section in the default profile on every run. The option list lives in `scripts/utils/conan-setup.cfg`:

- `conan_setup_options_common` — applied on every OS. Only include options the recipe defines on all platforms.
- `conan_setup_options_linux` — applied only on Linux, for options the recipe only defines there (e.g. `ffmpeg/*:with_vaapi`, `opencv/*:with_wayland`).

Centralizing these options guarantees every Terminus project computes the same package ID for shared dependencies, so packages like OpenCV and FFmpeg are built once per `(os, arch, build_type)` and reused everywhere — instead of each repo compiling its own variant. The current defaults produce a feature-rich, headless OpenCV (no X11/Wayland display backends; video IO via FFmpeg with VAAPI through libdrm), matching `terminus_conan/recipies/opencv/build-opencv.sh`. On EL10 this also avoids the `xorg/system` recipe pulling the retired `libXScrnSaver-devel` package.

To change the options:

1. Edit `conan_setup_options_common` / `conan_setup_options_linux` in `scripts/utils/conan-setup.cfg` (or override them in `~/.conan-setup.cfg` for machine-local changes).
2. Re-run `bash scripts/utils/conan-setup.bash` to rewrite the profile's `[options]` section.
3. Rebuild affected dependencies — changed options produce new package IDs, so the first build after a change compiles from source again.

## Configure Docker build credentials

If you plan to use `tmns-docker-build` for containerized builds, update the default credentials created at `~/.terminus/docker.env`:

```bash
# Edit the generated env file
vim ~/.terminus/docker.env
```

Replace the placeholder values with the correct Conan remote login:

```bash
CONAN_REMOTE=terminus-conan
CONAN_LOGIN_USERNAME=your-username
CONAN_PASSWORD=your-password
```

This file is read by `tmns-docker-build` and passed to the container with `docker run --env-file`, so the password does not appear on the command line.

## Next steps

- Clone the Terminus repositories: [Repositories]({% link repositories.md %})
- Build the ecosystem: [Building]({% link building.md %})
