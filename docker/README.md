# Terminus Container Images

This directory contains container image definitions for the Terminus build ecosystem. They are based on CentOS Stream 10, which enables the CRB repo needed for `libva-devel` and `libdrm-devel` pulled in by ffmpeg's VAAPI hardware-acceleration options.

## Images

| Dockerfile | Tag | Purpose |
| :--- | :--- | :--- |
| `Dockerfile.runtime` | `terminus-runtime-centos10` | Runtime base with C/C++ standard libraries and certificates. |
| `Dockerfile.build` | `terminus-build-centos10` | Extends `terminus-runtime-centos10` with compilers, CMake, Python, Conan, and the Terminus build scripts. |

## Building

From the repo root:

```bash
# Runtime image
docker build -f docker/Dockerfile.runtime -t terminus-runtime-centos10 .

# Build image (depends on terminus-runtime-centos10)
docker build -f docker/Dockerfile.build -t terminus-build-centos10 .
```

Or use the helper script:

```bash
docker/build-images.sh
```

You can override the default tags:

```bash
TERMINUS_RUNTIME_TAG=my-runtime:latest TERMINUS_BUILD_TAG=my-build:latest docker/build-images.sh
```

## Running the build container

```bash
docker run --rm -it -v $(pwd):/src terminus-build-centos10
```

## Notes

- `Dockerfile.build` runs `conan-setup.bash` to create a default Conan profile and configure the remotes from `conan-setup.cfg`. If the configured remote is unreachable, this step is allowed to fail so the image can still be used with a manually configured cache.
- Package names may need adjustment for the final RHEL 10 release.
- CentOS Stream 10 was chosen over UBI 10 because UBI's default repos do not include CRB, which is required for `libva-devel` and `libdrm-devel`. Enabling CRB on UBI would require a RHEL subscription/entitlement.
