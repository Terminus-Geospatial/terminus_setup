Terminus Setup
==========================

This repo has the necessary tools for setting up the tools required to build and install Terminus.

## Overview

Terminus C++ APIs are designed to be built using Conan.  This is not explicitly required, however Conan offers a few major benefits, specifically around versioning.

---

## Step 0: Setup Prerequisites

### Notes about Dependencies

GDAL and OpenCV currently do not install via conan.

### Fedora/RHEL

For RHEL/Fedora/CentOS users, the following will install the core dependencies.

```bash
sudo dnf install cmake g++ gdal-devel opencv-devel
```

### MacOS

Use Homebrew to setup required dependencies.

```bash
brew install cmake python3.13
```

---

## Step 1: Setup Conan
If you already have conan installed, then skip this this.  Make sure to enable conan on your system path.

If you do not have conan installed, run the following:

```bash
./setup-terminus.py
```

This will create a Python virtual environment in `${HOME}/conan` with conan installed.

## Step 2: Restart your shell or re-source the particular rc file.

If you are on MacOS, you will likely need to use ZSH.
```bash
. ~/.zshrc
```

For Linux or otherwise Bash users...
```bash
. ~/.bashrc
```

## Step 3: Import Conan

If you use this install script, it adds a command `go-conan` inside your shell RC file.

* ZSH: `${HOME}/.zshrc`
* BASH: `${HOME}/.bashrc`

Run one of the two following commands to import the conan environment.

1. `go-conan`
2. `. ${HOME}/conan/bin/activate`

## Step 4: Setup Conan

Conan requires a profile before you can start importing libraries.

Run the following command for default use-cases.

```bash
conan-setup.bash
```

This will update your `~/.bashrc` and `~/.zshrc`.  You will want to restart your terminal or re-source the appropriate rc file.

```bash
. ${HOME}/.bashrc
```

Next, setup your profile settings.  For the uninitiated, this is likely good enough:

```bash
conan profile detect
```

This will setup your conan profile to use `conancenter`.

## Step 5: Clone Terminus Repos

This repo packages a command-line tool for cloning all repositories in a single shot.

First, navigate back to a common area

```bash
cd ../
tmns-clone-repos.py -vv --all
```

