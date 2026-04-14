#!/usr/bin/env python3
"""
verify_migration.py — Playwright migration anti-pattern checker.

Usage:
    python verify_migration.py tests/playwright/
    python verify_migration.py tests/playwright/pages/login_page.py

Exit codes:
    0 — No FAIL findings (may have WARNs)
    1 — One or more FAIL findings
"""

import ast
import re
import sys
import json
from dataclasses import dataclass, field
from pathlib import Path


# ── Finding ────────────────────────────────────────────────────────────────────

@dataclass
class Finding:
    rule: str
    level: str  # FAIL | WARN | PASS
    line: int | None = None
    detail: str = ""


# ── Checks ─────────────────────────────────────────────────────────────────────

def check_no_selenium_imports(source: str, tree: ast.Module) -> list[Finding]:
    """FAIL if any selenium import exists."""
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                if name.startswith("selenium"):
                    findings.append(Finding(
                        rule="no-selenium-imports",
                        level="FAIL",
                        line=node.lineno,
                        detail=f"Selenium import found: '{name}'",
                    ))
    return findings or [Finding(rule="no-selenium-imports", level="PASS")]


def check_no_time_sleep(source: str, tree: ast.Module) -> list[Finding]:
    """FAIL if time.sleep() is called."""
    findings = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "sleep"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "time"
        ):
            findings.append(Finding(
                rule="no-time-sleep",
                level="FAIL",
                line=node.lineno,
                detail="time.sleep() found — delete it; Playwright auto-waits",
            ))
    return findings or [Finding(rule="no-time-sleep", level="PASS")]


def check_no_webdriverwait(source: str, tree: ast.Module) -> list[Finding]:
    """FAIL if WebDriverWait is referenced."""
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "WebDriverWait":
            findings.append(Finding(
                rule="no-webdriverwait",
                level="FAIL",
                line=node.lineno,
                detail="WebDriverWait found — delete it; Playwright auto-waits",
            ))
    return findings or [Finding(rule="no-webdriverwait", level="PASS")]


def check_no_find_element(source: str, tree: ast.Module) -> list[Finding]:
    """FAIL if find_element or find_elements is called."""
    findings = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in ("find_element", "find_elements")
        ):
            findings.append(Finding(
                rule="no-find-element",
                level="FAIL",
                line=node.lineno,
                detail=f".{node.func.attr}() found — replace with page.get_by_* or page.locator()",
            ))
    return findings or [Finding(rule="no-find-element", level="PASS")]


def check_no_wait_for_timeout(source: str, tree: ast.Module) -> list[Finding]:
    """FAIL if page.wait_for_timeout() is used as a sleep substitute."""
    findings = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "wait_for_timeout"
        ):
            findings.append(Finding(
                rule="no-wait-for-timeout",
                level="FAIL",
                line=node.lineno,
                detail="page.wait_for_timeout() found — use expect(locator).to_be_visible() instead",
            ))
    return findings or [Finding(rule="no-wait-for-timeout", level="PASS")]


def check_no_plain_assert_on_element(source: str, tree: ast.Module) -> list[Finding]:
    """
    FAIL if assert is used on element state (text, is_displayed, etc.)
    instead of expect(...) web-first assertions.
    """
    findings = []
    # Regex: assert <something>.text or assert <something>.is_displayed()
    # or assertEqual / assertTrue patterns in source text
    patterns = [
        (r"\bassert\b.*\.text\b", "assert on .text — use expect(locator).to_have_text()"),
        (r"\bassert\b.*\.is_displayed\(\)", "assert on .is_displayed() — use expect(locator).to_be_visible()"),
        (r"\bself\.assertEqual\b", "unittest assertEqual — use expect(locator) web-first assertion"),
        (r"\bself\.assertTrue\b.*is_display", "unittest assertTrue on is_displayed — use expect(locator).to_be_visible()"),
        (r"\bself\.assertFalse\b.*is_display", "unittest assertFalse on is_displayed — use expect(locator).to_be_hidden()"),
    ]
    for i, line in enumerate(source.splitlines(), start=1):
        for pattern, detail in patterns:
            if re.search(pattern, line):
                findings.append(Finding(
                    rule="no-plain-assert-element",
                    level="FAIL",
                    line=i,
                    detail=detail,
                ))
    return findings or [Finding(rule="no-plain-assert-element", level="PASS")]


def check_no_xpath_locators(source: str, tree: ast.Module) -> list[Finding]:
    """WARN if XPath locators are used (allowed as last resort but flagged for review)."""
    findings = []
    xpath_pattern = re.compile(r'(?:xpath=|By\.XPATH|"//|\'//)')
    for i, line in enumerate(source.splitlines(), start=1):
        if xpath_pattern.search(line):
            # Allow if there's a TODO comment on the same line
            if "# TODO: replace XPath" not in line:
                findings.append(Finding(
                    rule="no-xpath",
                    level="WARN",
                    line=i,
                    detail="XPath locator found without '# TODO: replace XPath' comment — review and replace with semantic locator",
                ))
    return findings or [Finding(rule="no-xpath", level="PASS")]


def check_no_unittest_testcase(source: str, tree: ast.Module) -> list[Finding]:
    """FAIL if test class still inherits from unittest.TestCase."""
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                base_name = ""
                if isinstance(base, ast.Attribute):
                    base_name = f"{base.value.id if isinstance(base.value, ast.Name) else ''}.{base.attr}"
                elif isinstance(base, ast.Name):
                    base_name = base.id
                if "TestCase" in base_name:
                    findings.append(Finding(
                        rule="no-unittest-testcase",
                        level="FAIL",
                        line=node.lineno,
                        detail=f"Class '{node.name}' still inherits from {base_name} — convert to plain pytest class or functions",
                    ))
    return findings or [Finding(rule="no-unittest-testcase", level="PASS")]


# ── Runner ─────────────────────────────────────────────────────────────────────

CHECKS = [
    check_no_selenium_imports,
    check_no_time_sleep,
    check_no_webdriverwait,
    check_no_find_element,
    check_no_wait_for_timeout,
    check_no_plain_assert_on_element,
    check_no_xpath_locators,
    check_no_unittest_testcase,
]


def verify_file(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {
            "file": str(path),
            "findings": [{"rule": "syntax", "level": "FAIL", "line": e.lineno, "detail": str(e)}],
            "passed": False,
        }

    all_findings = []
    for check in CHECKS:
        all_findings.extend(check(source, tree))

    has_fail = any(f.level == "FAIL" for f in all_findings)
    return {
        "file": str(path),
        "findings": [
            {"rule": f.rule, "level": f.level, "line": f.line, "detail": f.detail}
            for f in all_findings
        ],
        "passed": not has_fail,
    }


def format_results(results: list[dict]) -> str:
    lines = []
    total_pass = total_fail = total_warn = 0

    for result in results:
        lines.append(f"\n{'─' * 60}")
        lines.append(f"FILE: {result['file']}")
        lines.append(f"{'─' * 60}")
        for f in result["findings"]:
            loc = f" — line {f['line']}" if f["line"] else ""
            lines.append(f"  {f['level']:<5} [{f['rule']}]{loc}: {f['detail']}")
            if f["level"] == "PASS":
                total_pass += 1
            elif f["level"] == "FAIL":
                total_fail += 1
            elif f["level"] == "WARN":
                total_warn += 1

    lines.append(f"\n{'═' * 60}")
    lines.append(f"SUMMARY: {total_pass} passed · {total_fail} failed · {total_warn} warnings")
    overall = "PASS" if total_fail == 0 else "FAIL"
    lines.append(f"RESULT:  {overall}")
    lines.append(f"{'═' * 60}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: verify_migration.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.is_file():
        paths = [target]
    else:
        paths = sorted(target.rglob("*.py"))

    # Skip __init__.py and conftest.py
    paths = [p for p in paths if p.name not in ("__init__.py",)]

    if not paths:
        print("No Python files found.")
        sys.exit(0)

    results = [verify_file(p) for p in paths]

    # Human-readable output
    print(format_results(results))

    # Machine-readable output for CI
    json_output = Path("migration_report.json")
    json_output.write_text(json.dumps(results, indent=2))
    print(f"\nJSON report written to: {json_output}")

    any_fail = any(not r["passed"] for r in results)
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
