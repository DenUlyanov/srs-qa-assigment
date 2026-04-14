# Migration Approach

## Tool Choice: Claude Code + CLAUDE.md

I chose **Claude Code** with a `CLAUDE.md` rules file as the AI orchestration layer.
`CLAUDE.md` is automatically loaded into context on every interaction, which means every agent session
starts with the same locator priority chain, naming conventions, and hard constraints — no need to
re-paste rules into each prompt. Claude Code also supports subagents with the `Agent` tool, enabling
genuine parallel execution for Phase 1 (Page Objects) and Phase 2 (test files).

Alternative considered: **Cursor** with `.cursorrules`. Equivalent rules file support, but no native
subagent API — parallelism would have to be orchestrated externally via a shell script.

---

## Context Management Strategy

### The core problem
A single test file may import 5 Page Objects, a shared `BasePage`, custom utilities, and project-level
config. Feeding all that source code into a 100K-token window leaves little room for output, and
causes the AI to lose focus on the actual conversion task.

### Solution: signatures-only context + shared migration-context.md

**1. PO signatures instead of full source.**
After migrating each Page Object, generate a compact signature block:
```python
# LoginPage (tests/playwright/pages/login_page.py) — ALREADY MIGRATED
class LoginPage:
    def __init__(self, page: Page) -> None: ...
    def navigate(self) -> None: ...
    def login(self, username: str, password: str) -> None: ...
    def error_message(self) -> Locator: ...
```
A 200-line PO compresses to ~10 lines. Five POs = ~50 lines of context instead of ~1000.

**2. `migration-context.md` — always injected.**
A lightweight file (~500 tokens) checked into the repo root during migration:
```markdown
# Migration Context
- Base URL: http://localhost:3000
- Test user: admin@example.com / secret123
- All POs inherit from BasePage (navigate, scroll_to_bottom, wait_for_page_load)
- Shared fixtures in tests/playwright/conftest.py
- data-testid attributes use kebab-case: data-testid="submit-btn"
- Custom assertion helper: expect_toast(page, message) in tests/playwright/utils/assertions.py
```
This prevents the AI from asking the same environment questions repeatedly.

**3. Split large test files.**
Files with 30+ tests are split into feature-grouped batches before migration.
Each batch is sent as a separate prompt with the same PO signatures and context file.

**4. Bottom-up processing order.**
`utilities → BasePage → Page Objects → test files`
Never send a test to the AI before its POs are migrated. The signatures must come from the actual
migrated Playwright file, not inferred from the Selenium version.

---

## Migration Order

```
Phase 0  Shared utilities + BasePage        (1 agent, sequential, ~15 min)
   │
Phase 1  All 60+ Page Objects               (parallel agents, ~20 min)
   │     No inter-PO dependencies → maximum parallelism
   │     Each agent: 1 source file + CLAUDE.md + utility signatures
   │
Phase 2  All 400+ test files                (parallel, grouped by PO)
   │     Group tests by their PO dependencies
   │     Each group runs concurrently; agents within a group can also run in parallel
   │     Each agent: 1 test file + CLAUDE.md + PO signatures + migration-context.md
   │
Phase 3  Verification                       (sequential, ~5 min)
         Run verify_migration.py tests/playwright/
         Fix any FAIL findings before opening PR
```

**Total estimated wall-clock time with parallel agents: ~45–60 minutes** for a 400-test suite.
Sequential manual migration of the same suite: 4–8 days.

---

## Parallel Subagent Design (Claude Code)

Claude Code's `Agent` tool allows launching subagents in parallel in a single message.
Each subagent operates in a git worktree (isolated copy of the repo) and writes its output file
plus a JSON manifest.

### Dependency graph

```
[utils/base_page.py] ──┐
[utils/helpers.py]  ──┤
                       ▼
              [login_page.py] ──┐
              [checkout_page.py]──┤
              [search_page.py] ──┤──► [test_login.py]
              [cart_page.py]   ──┤    [test_checkout.py]
              [dashboard_page.py]──┘   [test_search.py]
                                       ...
```

### What runs concurrently

- **Phase 1**: All PO agents. No ordering constraints between them.
  Example: 60 Page Objects → 12 agents × 5 POs each, all running simultaneously.

- **Phase 2**: Test agents grouped by PO dependency cluster.
  Tests that only use `LoginPage` can run while tests that use `CheckoutPage + CartPage` also run.
  The only constraint: a test agent cannot start until all its required POs are in the manifest.

### Agent handoff format

Each agent outputs:
1. The migrated `.py` file written to `tests/playwright/`
2. A JSON manifest alongside it:

```json
{
  "source": "tests/selenium/pages/login_page.py",
  "output": "tests/playwright/pages/login_page.py",
  "public_methods": ["navigate", "login", "error_message", "user_avatar"],
  "locator_strategy": {
    "navigate": "goto",
    "login": "get_by_label + get_by_role",
    "error_message": "get_by_role(alert)"
  },
  "xpath_todos": 0,
  "warnings": []
}
```

The orchestrator reads all Phase 1 manifests and generates the signature blocks for Phase 2 agents.
This is deterministic: agents don't need to communicate directly with each other.

### Orchestrator pseudo-code (Claude Code session)

```python
# Phase 1 — parallel PO migration
po_files = glob("tests/selenium/pages/*.py")
batches = chunk(po_files, size=5)
agent_results = []
for batch in batches:
    # Launch all batches in parallel (single Agent tool message)
    agent_results.extend(run_agents_parallel(batch, prompt=convert_page_object_prompt))

# Collect manifests
manifests = collect_manifests("tests/playwright/pages/")
signatures = build_signature_blocks(manifests)

# Phase 2 — parallel test migration
test_files = glob("tests/selenium/test_*.py")
for test_file in test_files:
    required_pos = extract_po_dependencies(test_file)
    context = signatures[required_pos] + migration_context_md
    run_agent(test_file, prompt=convert_test_prompt, context=context)
```

---

## Risk Areas & Mitigations

| Risk | Mitigation |
|------|-----------|
| Dynamic XPath locators that can't be replaced | `no-xpath` WARN rule flags them; human review required before merge |
| `driver.execute_script()` with complex JS | Migrate to `page.evaluate()` — add `# TODO: verify JS` comment for review |
| File upload via `send_keys` on hidden input | Use `page.set_input_files(locator, path)` — call out in CLAUDE.md |
| iframe interactions | `page.frame_locator("iframe[name='...']")` — add to CLAUDE.md equivalents table |
| Alert dialogs (`driver.switch_to.alert`) | `page.on("dialog", lambda d: d.accept())` — must be registered before action |
| Flaky tests that relied on Selenium's slower execution | These will surface faster in Playwright; do not re-add sleeps — fix the root cause |
| Test ordering dependencies in the original suite | Each Playwright test must be independent; uncover and fix ordering bugs during migration |
