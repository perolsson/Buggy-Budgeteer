# Buggy Budgeteer

Buggy Budgeteer is a deliberately flawed personal budgeting helper written in pure Python. It is designed for short hackathon events where participants race to uncover as many bugs as possible with help from AI assistants.

## Getting Started

- Requires Python 3.9+ (no external dependencies).
- Clone the repo, then run commands from the project root.
- An intentionally inconsistent sample dataset lives at `data/sample_expenses.json`.
- Optional: create a virtual environment, though nothing needs to be installed.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Provided Entrypoints

- `python -m budget_tracker.cli` launches a minimal interactive prompt.
- `python -m budget_tracker.reporting` prints a quick summary.
- `python -m unittest discover` runs the supplied (buggy) tests.

## What To Expect

The codebase mixes obvious issues (syntax errors, name typos) with more subtle logical and data quality defects. Some tests already fail; others pass even though the implementation is wrong. Not every module is fully covered, so exploratory testing is encouraged.

### Rough Difficulty Guide

- **Easy:** fix crashes on startup, basic parsing errors, broken imports.
- **Medium:** incorrect calculations, mishandled edge cases, inconsistent normalization.
- **Hard:** data races between modules, state persistence bugs, misleading tests.

## Suggested Workflow

1. Run the unit tests to see immediate failures.
2. Explore the CLI using the sample data.
3. Inspect analytics/reporting outputs for suspicious numbers.
4. Iterate on fixes while adding your own tests.

Good luck—every discrepancy is intentional.
