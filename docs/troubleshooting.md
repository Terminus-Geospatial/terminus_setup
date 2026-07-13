---
title: Troubleshooting
layout: default
nav_order: 6
---

# Troubleshooting

## Common issues

### Conan not found

- Ensure you have activated the Conan environment with `go-conan`.
- Check that `${HOME}/conan/bin/activate` exists.
- Verify that `~/.local/bin` is in your `PATH`.

### Build failures

- Verify all system dependencies are installed (CMake, compiler, GDAL, OpenCV, Python).
- Check that your C++ compiler version is compatible (GCC 9+ or Clang 10+).
- Ensure the Conan default profile is configured with `conan profile detect`.
- Use verbose logging (`-v` or `-vv`) to capture the full error message.

### Missing dependencies during build

- Use the `--build-missing` flag to let Conan build dependencies that are not in the cache.
- Confirm that GDAL and OpenCV are installed via the system package manager.

## Getting more help

1. Check `changelog.md` for recent updates.
2. Review the sample configuration files in `scripts/utils/config/`.
3. Run scripts with verbose output (`-v` or `-vv`).
4. Inspect the generated profiles with `tmns-profile-info.py -p <profile>`.
