---
name: migration-assessment
description: Generate a complete AI-assisted migration assessment deliverable set for any framework/library migration. Produces: AI rules config (CLAUDE.md), reusable conversion prompts with before/after examples, a verification script catching common AI migration mistakes, an approach doc, and a README. Mirrors the structure used in technical take-home assessments for senior QA/engineering roles.
---

You are helping produce a **complete AI-assisted migration assessment** for a framework or technology migration. Follow these steps exactly.

## Step 1 — Gather context

Ask the user (or infer from context) the following. If any are already clear from the conversation, skip asking:

1. **Source framework** — what are we migrating *from*? (e.g., Selenium, Mocha, Redux, REST)
2. **Target framework** — what are we migrating *to*? (e.g., Playwright, Vitest, Zustand, GraphQL)
3. **Language** — Python, TypeScript, JavaScript, Java, etc.
4. **Scope** — roughly how many files? (helps size the parallelism section)
5. **Output directory** — where to write the files (default: `./migration-assessment/`)

Once you have all five, proceed to Step 2 without further questions.

## Step 2 — Create directory structure

```
{output_dir}/
├── rules/
│   └── CLAUDE.md
├── prompts/
│   ├── convert-unit.md          # "unit" = the smallest migratable thing (Page Object, component, module…)
│   └── convert-test.md          # or convert-file.md if not test-focused
├── verification/
│   ├── verify-migration.md
│   └── verify_migration.{ext}   # script in the target language's ecosystem
├── docs/
│   └── approach.md
└── README.md
```

## Step 3 — Write each file

### `rules/CLAUDE.md`

Structure:
1. **Project identity** — one paragraph: what migration this is, what AI tool is used, what the AI must always/never do.
2. **Locator / API priority chain** — numbered table from most-preferred to least-preferred API. Be concrete: show actual code, not descriptions.
3. **Never do** — bulleted list of the 6–10 most common AI literal-translation mistakes for this specific migration. Each bullet:
   - Names the Selenium/source pattern
   - Explains *why* it's wrong in the target framework (not just "don't do it")
   - Shows the correct replacement
4. **File structure rules** — directory layout, naming conventions, import paths, class/function templates.
5. **API equivalents table** — two-column table: source API | target API.
6. **Coexistence rules** — how source and target code live in the same repo during migration (separate dirs, shared fixtures, CI independence).
7. **Parallel subagent orchestration** (bonus) — dependency graph, what runs in Phase 0/1/2/3, agent handoff format (JSON manifest), orchestrator pseudo-code.

### `prompts/convert-unit.md`

The "unit" is the smallest independently migratable piece (Page Object, React component, service module, etc.).

Structure:
- Role statement + rules reference
- Input slot: `{{SOURCE_UNIT}}`
- Step-by-step instructions (numbered, exhaustive — cover every pattern that appears in typical source files)
- Output format: migrated file only, then a `# ---MANIFEST---` JSON block
- **Before/After example** — realistic, ~30–60 lines each, showing every tricky pattern
- Context limit note: how to feed dependencies as signatures

### `prompts/convert-test.md` (or `convert-file.md`)

Structure:
- Role statement + rules reference
- Input slots: `{{SOURCE_TEST}}` + `{{MIGRATED_UNIT_SIGNATURES}}`
- Step-by-step instructions covering:
  - Lifecycle mapping (setUp/tearDown → fixtures, beforeEach → hooks, etc.)
  - Assertion style (sync assertEqual → framework-native expect)
  - Test isolation requirements
  - Import changes
- **Before/After example** — realistic test file
- **Context limit strategy** — explain signature chunking, shared context file injection, bottom-up processing order

### `verification/verify-migration.md`

- Table of 8+ anti-patterns: rule ID | level (FAIL/WARN) | what it catches
- Sample output showing PASS/FAIL/WARN per rule with line numbers
- JSON report format for CI
- GitHub Actions workflow snippet (or equivalent CI config) showing:
  - The verification step as a required check
  - FAIL → blocks merge (exit code 1)
  - WARN → posts PR comment, requires human sign-off

### `verification/verify_migration.{ext}`

A runnable script. For Python targets: use `ast` module + regex, not just grep. For JS/TS targets: use AST parsing (acorn, typescript compiler API, or regex fallback). For Java: regex on source lines.

Must catch **at least 8** anti-patterns:
- Source framework imports still present (FAIL)
- Explicit sleep/wait calls (FAIL)
- Source framework wait helpers (FAIL)
- Source framework element finders (FAIL)
- Sleep-equivalent target API used as wait (FAIL)
- Sync assertions on element state instead of framework-native (FAIL)
- Last-resort locator without review comment (WARN)
- Source framework test base class (FAIL)

Script must:
- Accept a file path or directory as argument
- Output human-readable PASS/FAIL/WARN per rule with line numbers
- Write a `migration_report.json` machine-readable output
- Exit 0 if no FAILs, exit 1 if any FAILs

### `docs/approach.md`

Sections:
1. **Tool choice** — why Claude Code + CLAUDE.md (or chosen tool), what makes it better than alternatives
2. **Context management strategy** — signature chunking, shared context file, split large files, bottom-up order
3. **Migration order** — phased plan with estimated wall-clock time (parallel vs sequential)
4. **Parallel subagent design** — dependency graph ASCII art, what runs concurrently, agent handoff JSON format, orchestrator pseudo-code
5. **Risk areas** — table of 5–7 migration-specific risks and their mitigations

### `README.md`

One paragraph covering: tool choice, language, file map, how to run the verification script, pointer to approach.md.
Then a quick-start table:

| Path | Purpose |
|------|---------|
| `rules/CLAUDE.md` | AI config |
| `prompts/convert-unit.md` | Unit conversion prompt |
| `prompts/convert-test.md` | Test conversion prompt |
| `verification/verify_migration.*` | Anti-pattern checker |
| `docs/approach.md` | Strategy + parallel agent design |

## Step 4 — Quality checks before finishing

Before writing files, mentally verify:
- [ ] The locator/API priority chain is **numbered** and shows **actual code**, not descriptions
- [ ] Every "never do" rule names the source pattern, explains why it's wrong in the target, and shows the fix
- [ ] Before/after examples are syntactically valid in the target language
- [ ] The verification script catches ≥8 anti-patterns and exits with code 1 on FAIL
- [ ] The parallel subagent section has a dependency graph and agent handoff JSON format
- [ ] Coexistence rules address how both old and new code live in the same repo

## Tone and style

- All rules must be **concrete** — show actual API calls, not descriptions
- Anti-patterns must come from **real migration mistakes**, not theoretical ones
- Before/after examples must be **realistic** (30–60 lines, multiple patterns in one file)
- The verification script must be **runnable** — test it mentally against a known-bad file
