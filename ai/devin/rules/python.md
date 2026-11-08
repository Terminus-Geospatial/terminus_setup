---
trigger: always_on
---

# Python standards

- Executable Python scripts start with `#!/usr/bin/env python3`. Use the repository's Terminus IP banner and file metadata for new source files; preserve existing attribution and comments.
- Group imports in this order: standard library, third-party packages, then Terminus/project modules. Alphabetize within each group unless a dependency requires a different order. Keep existing import-group labels and do not create empty groups.
- Use descriptive snake_case function/variable names and follow PEP 8 except for the Terminus preference for spaces inside nonempty call/declaration parentheses, for example `load_config( config_path )`.
- Add meaningful docstrings to new functions/classes and type hints to new interfaces where practical. Keep argument parsing, orchestration, and reusable logic separate.
- Prefer `pathlib` and existing repository utilities when consistent with neighboring code. Resolve resource paths explicitly rather than assuming the current working directory or a developer's home path.
- Use argument lists for subprocesses, check exit status, and propagate useful context. Never interpolate untrusted data into shell commands or log secrets.
- Handle failures at useful boundaries; do not wrap every expression in a broad catch. Use the project's existing exception/result and logging conventions.
- Add regression tests for changed behavior. Check syntax and run relevant tests using the configured environment; do not add dependencies or change tooling merely to format a small edit.
