# AI-Assisted Selenium → Playwright Migration

This repository contains the AI orchestration setup for migrating a Python pytest-selenium suite (400+ tests, 60+ Page Objects) to pytest-playwright using **Claude Code** as the AI assistant. The `rules/CLAUDE.md` file is loaded automatically on every Claude Code session and enforces consistent locator strategy, naming conventions, and migration constraints; `prompts/` contains two reusable conversion prompts (one for Page Objects, one for test files) each with realistic before/after examples; `verification/verify_migration.py` is a static analysis script that catches 8 common AI migration mistakes and exits with code 1 in CI to block bad migrations from merging; and `docs/approach.md` details the context management strategy (PO signature chunking, shared migration-context.md injection) and the parallel subagent orchestration plan that reduces a multi-day manual migration to under an hour of wall-clock time.

## Quick start

```bash
# Verify a migrated file or directory
python verification/verify_migration.py tests/playwright/

# Run migrated tests
pytest tests/playwright/ --browser chromium
```

## File map

| Path | Purpose |
|------|---------|
| `rules/CLAUDE.md` | AI config — loaded on every session |
| `prompts/convert-page-object.md` | Reusable prompt for PO migration |
| `prompts/convert-test.md` | Reusable prompt for test file migration |
| `verification/verify_migration.py` | Anti-pattern checker (8 rules, CI-ready) |
| `verification/verify-migration.md` | Verifier documentation + CI setup |
| `docs/approach.md` | Context strategy + parallel agent design |
| `migration-assessment.md` | Claude Code skill — reusable for any migration |

## Reusable Skill: `/migration-assessment`

`migration-assessment.md` is a **Claude Code skill** that generalises this entire assessment pattern to any framework migration — not just Selenium → Playwright.

### How to install

Copy the skill file to your Claude Code skills directory:

```bash
cp migration-assessment.md ~/.claude/skills/migration-assessment.md
```

Then restart Claude Code. The skill will be available as:

```
/migration-assessment
```

### What it does

When invoked, the skill asks for:
1. **Source framework** — what you're migrating *from* (e.g. Selenium, Mocha, Redux)
2. **Target framework** — what you're migrating *to* (e.g. Playwright, Vitest, Zustand)
3. **Language** — Python, TypeScript, JavaScript, etc.
4. **Scope** — number of files (sizes the parallelism section)
5. **Output directory** — where to write the files (default: `./migration-assessment/`)

It then generates the full deliverable set — AI rules config, two conversion prompts with before/after examples, a verification script catching 8+ anti-patterns, an approach doc with parallel subagent design, and a README — tailored to that specific migration.
