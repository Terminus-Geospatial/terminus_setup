---
trigger: always_on
---

# C++ standards

- Use angle brackets for includes unless a private/generated file requires quotes. Order groups: C++ standard library, third-party libraries, then Terminus libraries; alphabetize within each group. Include what the file uses rather than relying on incidental transitive includes.
- Use `#pragma once` in headers. Keep one primary class per header unless closely related local/helper types justify otherwise. Put non-template implementation in `.cpp` files where practical.
- Follow existing Terminus naming: types such as `Foo_Bar`, descriptive snake_case functions/variables, and nested `tmns::...` namespaces. Do not rename existing APIs merely to apply a naming preference.
- Use four-space indentation, spaces inside nonempty function-call/declaration parentheses, and opening braces on their own lines for new functions, classes, and control-flow blocks. Avoid unrelated formatting churn.
- Keep class access sections ordered `public`, `protected`, `private`. Within each section, group types/aliases first, then existing variable declarations and functions consistently with neighboring classes; order methods as getters/setters, utility functions, and static functions where applicable. Keep protected/private data after methods. Do not create empty sections just to match a template.
- Follow the repository's function separator and namespace-closing conventions. Where `.cpp` files use visual separators before function definitions, continue that pattern for new definitions, using the function's name in the separator. Preserve existing separators/comments; do not add or remove comments as unrelated cleanup.

```cpp
/****************************************/
/*          Function_Name               */
/****************************************/
```

- Shorten namespace references using enclosing-namespace lookup where unambiguous. For example, inside `tmns::example::worker`, `config::Options` can refer to `tmns::example::config::Options` when that sibling namespace is declared and visible. Outside the shared namespace, use full qualification or a clear alias; do not assume a sibling namespace exists. Do not add global `using namespace` directives to public headers.
- Keep unused parameter names and mark them `[[maybe_unused]]`, for example `void notify( [[maybe_unused]] int event_id );`; do not comment the names out.
- Use the existing Terminus `Result<T>`/`Optional<T>` APIs for fallible operations where appropriate. Check success before accessing values; preserve useful error context. Verify the current Outcome API rather than copying stale examples.
- Use readable multiline initializers for nested records and test tables: one case per block, one field per line, and nested maps expanded by entry. Compact scalar lists and individual key/value pairs are acceptable when clearly readable.

```cpp
const std::vector<Test_Case> test_cases {
    {
        "single property",
        "ipc_service=zmq",
        {
            { "ipc_service", "zmq" }
        }
    },
    {
        "empty input",
        "",
        {}
    }
};
```

- Prefer expandable table-driven tests with descriptive case names and `SCOPED_TRACE`. Assert successful results before inspecting values, cover meaningful edge cases, and preserve failures as regression tests.
- Use an existing checked-in formatter configuration if present. These rules are guidance, not a claim that a formatter or CI enforcement is installed; do not invent or apply a new formatting configuration without review.

## Canonical header layout

For new headers, use the following structure. Replace `<copyright-year>`, `<filename>`, `<author>`, and `<creation-date>` with accurate project metadata; do not copy example identities or update existing copyright years incidentally. Preserve the repository's license wording. The namespace, class, and members below are illustrative: use the actual component and only the access sections/members it needs. Add third-party includes between the standard-library and Terminus groups when required; omit empty include groups.

```cpp
/**************************** INTELLECTUAL PROPERTY RIGHTS ****************************/
/*                                                                                    */
/*                    Copyright (c) <copyright-year> Terminus LLC                      */
/*                                                                                    */
/*                                All Rights Reserved.                                */
/*                                                                                    */
/*          Use of this source code is governed by LICENSE in the repo root.          */
/*                                                                                    */
/**************************** INTELLECTUAL PROPERTY RIGHTS ****************************/
/**
 * @file    <filename>
 * @author  <author>
 * @date    <creation-date>
 */
#pragma once

// C++ Standard Libraries
#include <string>

// Terminus Libraries
#include <terminus/error.hpp>

namespace tmns::example {

class Configuration_Source
{
    public:
        using Value = std::string;

        Result<Value> read();

    protected:
        void reset();

    private:
        std::string m_value;

}; // End of Configuration_Source Class

} // end of tmns::example namespace
```

Align the banner with neighboring files after substituting metadata. Use verified public include paths such as `<terminus/error.hpp>`, not historical paths copied from unrelated examples. Definitions for the non-template methods belong in a `.cpp` file. Keep public types/aliases, variables when genuinely public, and functions grouped in that order; keep protected/private types and functions ahead of their data members. Within function groups, prefer getters/setters, utility functions, then static functions when applicable.
