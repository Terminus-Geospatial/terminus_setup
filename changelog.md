# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),

## [1.0.2] - 2026-07-12

### Added
- GitHub Pages documentation site under `docs/`.
- GitHub Actions workflow to deploy the Jekyll site to Pages.
- Setup, repositories, building, utilities, and troubleshooting documentation pages.

### Changed
- README now links to the live GitHub Pages documentation and no longer includes the full repository structure.
- Setup instructions use `python3` and `brew install python` instead of hardcoded Python versions.

### Fixed
- Removed a premature `exit 0` in `scripts/utils/conan-build.sh` so the deployment block can run.

## [1.0.1] - 2026-01-18

### Added
* Creating upload-all script for conan packages.

### Changed
* Updating setup scripts to wire up a conan cache.

## [1.0.0] - 2026-01-11

### Changed
- Adding Terminus Astro to repo list
- Adding Terminus Toolbox to repo list
- Removing Terminus-Coord from repo list

## [0.0.4] - 2025-11-26
### Added
- Adding Terminus Platform C++ API library to default profile list.

## [0.0.3] - 2025-11-22
### Changed
- Adding Framework Configuration Service to default profile list.

## [0.0.2] - 2025-11-15

### Changed
- Updated `conan-build.sh` so it fails early if no conanfile in current folder.

## [0.0.1]

### Added
- Adding this changelog
- Formalizing versioning
- Refactoring setup script

