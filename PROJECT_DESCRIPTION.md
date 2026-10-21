# Project description

A Python command-line expense tracker that records spending, lists expenses, and summarizes totals by category, with unit tests and GitHub Actions automation.

- Built a CLI with `argparse` offering `add` (amount, category, optional note), `list`, and `summary` subcommands, with expenses persisted to a local JSON file.
- Implemented validation and aggregation in a separate tracker module: rejects non-positive amounts, normalizes categories to lowercase, rounds to two decimals, and computes per-category and overall totals.
- Wrote unit tests with `unittest` and set up a GitHub Actions workflow that runs the suite on Python 3.12 on every push to `main`.
- Extended the CI pipeline to call the Anthropic API to generate this project description and commit the result back to the repository.
