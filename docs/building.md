---
title: Building
layout: default
nav_order: 4
---

# Building Terminus

## Build a single project

`conan-build.sh` builds an individual Conan project from the current directory. It expects a `conanfile.py` in the source root.

```bash
conan-build.sh -r -c -B
```

### Options

| Option | Description |
|--------|-------------|
| `-r`, `--release` | Build in Release mode (default is Debug) |
| `-c`, `--clean` | Clean the build directory before building |
| `-f`, `--force` | Force a clean without prompting when the current directory is the build root |
| `-n`, `--no-package` | Skip packaging and deployment |
| `-s <dir>`, `--source-root <dir>` | Source directory (default: current directory) |
| `-b <dir>`, `--build-root <dir>` | Build directory (default: `./build`) |
| `-v`, `--verbose` | Enable verbose output |
| `-x`, `--no-deploy` | Skip deployment even if the recipe has a `deploy()` method |
| `-C <channel>`, `--channel <channel>` | Conan user/channel (default: `branches/development`) |
| `-B`, `--build-missing` | Build missing dependencies |
| `-o <option>`, `--option <option>` | Pass a Conan package option (repeatable) |
| `-h`, `--help` | Show help |

The script runs `conan install`, `conan build`, and `conan export-pkg`. If the recipe defines a `deploy()` method and deployment is not disabled, it then calls `conan-deploy.sh` to deploy the package.

## Build the entire ecosystem

`tmns-build-all.py` reads a profile and builds every repository in sequence.

```bash
tmns-build-all.py --config tmns-profile.cfg
```

### Options

| Option | Description |
|--------|-------------|
| `-v` | Log at debug level |
| `-r` | Build in release mode |
| `-d` | Build in debug mode |
| `-c` | Clean repositories before building |
| `-x` | Continue building even if a repository fails |
| `-p <path>` | Path to a profile file |
| `--ignore-profiles` | Ignore any local profile and use the default repository list |
| `-l <path>` | Write output to a log file |
| `--build-missing` | Build missing dependencies |

If no profile is provided, the script looks for `tmns-profile.cfg` in the current directory. If that is not found, it falls back to a hard-coded default list of repositories.

## Build configuration

The build profile controls:

- Which repositories are built
- Build modes (`debug`, `release`, `relwithdebinfo`)
- Whether a clean build is performed
- Whether missing dependencies are built
- Repository-specific paths and settings

A sample configuration file is available at `scripts/utils/config/sample-build-config.cfg`. Copy it to create a custom profile:

```bash
cp scripts/utils/config/sample-build-config.cfg my-profile.cfg
```

Then edit the file and pass it to the build scripts:

```bash
tmns-clone-repos.py --profile my-profile.cfg
tmns-build-all.py --config my-profile.cfg
```

## Deploy a built package

`conan-deploy.sh` installs and deploys a Conan package to a local directory. It can work from the current `conanfile.py` or from an explicit reference.

```bash
conan-deploy.sh
conan-deploy.sh terminus_cpp_demos/1.0.0@branches/develop -d ./deployment
```

### Options

| Option | Description |
|--------|-------------|
| `-d <dir>`, `--dest <dir>` | Deployment destination (default: `~/installs/terminus/<name>`) |
| `-r`, `--release` | Install the Release version |
| `-C <channel>`, `--channel <channel>` | Channel suffix (default: `branches/develop`) |
| `-o <option>`, `--option <option>` | Forward a Conan option |
| `-h`, `--help` | Show help |

The script detects whether the recipe defines a `deploy()` method. If not, it uses the default deployer, which copies the package and its dependency graph to the destination.
