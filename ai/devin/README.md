# Shared Terminus Devin rules

This directory provides reusable Terminus AI guidance. The common templates in `rules/*.md` are intended for reviewed installation into a consuming repository's `.devin/rules/`. They are not automatically loaded from this location. No automatic installer or formatter enforcement is supplied yet.

## Layout

```text
ai/devin/
├── README.md
└── rules/
    ├── workflow.md
    ├── cpp.md
    ├── bash.md
    ├── python.md
    ├── cmake.md
    ├── conan.md
    ├── markdown.md
    └── repository-hygiene.md
```

## Common templates

| Template | Scope |
| --- | --- |
| [workflow](rules/workflow.md) | Scoped changes, host build/test workflow, verification, release hygiene |
| [C++](rules/cpp.md) | Includes, class layout, namespace lookup, results, multiline test data |
| [Bash](rules/bash.md) | Portable shebang, strict mode, functions, quoting, argument handling |
| [Python](rules/python.md) | File headers, imports, naming, docstrings, typing |
| [CMake](rules/cmake.md) | Toolchain/layout integration, target scope, tests, installation |
| [Conan](rules/conan.md) | Direct tool requirements, settings versus options, package compatibility |
| [Markdown](rules/markdown.md) | Spacing, paragraphs, links, changelogs, project glossary policies |
| [Repository hygiene](rules/repository-hygiene.md) | Ignore patterns, generated artifacts, credentials, configuration location |

Templates use Devin's supported `trigger: always_on` frontmatter. Keep them concise. Narrower activation or skills can be considered when the common set grows.

## Design decisions

- Consolidate C++ guidance for angle-bracket includes, group/alphabetical ordering, class/access layout, shortened namespace lookup, and named `[[maybe_unused]]` parameters. Use explicit multiline test-table formatting.
- Keep API/layout descriptions and glossary requirements project-specific rather than imposing them on unrelated repositories.
- Use `#!/usr/bin/env bash` consistently.
- Treat `compiler.cppstd` as a Conan setting, not an entry in `default_options`. Validate shared/static dependency options rather than applying unsupported options blindly.
- Do not freeze dependency versions into generic rules. Require a directly available CMake executable compatible with the project; `cmake/4.1.2` is the current tested baseline. `terminus_cmake` is a helper package, not a substitute for that executable.
- Respect Conan layout-specific toolchain paths and consuming-project test option names.
- Do not use unconditional `package_id` clearing for compiled packages. Header-only/data-only compatibility must be assessed separately.
- Preserve project headers with accurate metadata and verified public include paths.
- Keep monorepo build commands, deployment flags, central TODO policy, workspace paths, and submodule pinning out of shared templates. Those live only in `terminus_mono/.devin/rules/workspace.md`.

## Adoption

1. Review the common templates against the destination's current rules and any formatter configuration. Agree on any project-specific exceptions before installation.
2. Install only the applicable top-level `rules/*.md` templates under the destination's `.devin/rules/`.
3. Merge or retire duplicate common rules in the destination deliberately; keep its project structure/API/glossary rules. Back up local work and do not overwrite uncommitted changes.
4. Verify frontmatter and review representative C++, Python, Bash, CMake, Conan, and Markdown edits. Agent guidance is not formatter/CI enforcement; a shared formatter and safe synchronization tooling remain separate work.
5. Record adoption in the appropriate project action list. The templates have not yet been rolled out across repositories.
