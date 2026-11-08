---
trigger: always_on
---

# Terminus engineering workflow

- Read the repository's rules, recipe, neighboring code, and relevant tests before editing. Preserve project-specific behavior and existing public APIs unless the task requires changes.
- Keep changes scoped. Do not reformat unrelated code, discard local work, or replace project-specific rules during common-rule updates.
- Preserve existing copyright/license banners and comments. New source files use the neighboring Terminus banner and file metadata with accurate dates and attribution, not copied example names or years.
- Keep agent configuration in `.devin/`. Shared templates live in `terminus_setup/ai/devin/rules/`; they are not automatically active there.
- For host Conan builds, activate the configured environment with `go-conan` in each new terminal, then use `conan-build.sh -c` from the package root. Check helper flags before adding options; do not assume every repository has identical layout or test paths.
- Run CTest with `--output-on-failure` in the actual generated build tree and platform where the binaries were built. Conan layouts may place it below `build/`; do not run Linux binaries directly on macOS.
- Reproduce failures before fixing them. Replace placeholder tests with meaningful assertions, not skips or unconditional success. Do not weaken tests to hide implementation defects.
- Verify relevant tests and `git diff --check`; report the platform/configuration tested and anything not verified. Do not describe mocked builds as real builds.
- Keep dependency pins and consumer/package-test requirements consistent; verify which source/package revisions a build actually consumes.
- Use concise Keep a Changelog entries and distinguish planned features from implemented behavior. Follow the repository's action-item tracking policy.
- Never commit credentials, caches, generated binaries, runtime data, imagery fixtures, or test output. Preserve dependency security controls. Do not commit or push unless requested.
