---
trigger: always_on
---

# Repository hygiene

- Keep generated build trees, compiled objects/libraries/executables, deployment output, runtime databases, logs, caches, large fixtures, and test artifacts out of source control.
- Add narrowly scoped ignore patterns for artifacts actually produced by the project: C++ `build/`, `cmake-build-*/`, `*.o`, `*.a`, `*.so`, `*.dylib`; Python `__pycache__/`, `*.pyc`, `.venv/`, `*.egg-info/`, and `dist/`; platform/editor temporary files as appropriate.
- Do not blanket-ignore intentionally shared IDE settings, test fixtures, or package metadata already tracked by a repository. Preserve existing conventions and review the staged diff.
- Never commit credentials, dotenv secrets, or machine-local configuration. Prefer ignored local overrides and the established secrets mechanism; an example environment file must contain placeholders only.
- Ignore rules do not remove already tracked files or make secrets safe. Report accidentally tracked sensitive files and obtain approval before destructive cleanup or history rewriting.
- Do not add new configuration under compatibility directories such as `.windsurf/`; use `.devin/` for active agent rules and preserve project-specific files during any migration.
