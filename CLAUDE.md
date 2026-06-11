# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A portfolio/showcase project demonstrating skills at the intersection of Web3 and cybersecurity. It is **not** a single application — it is a collection of three independent, self-contained artifacts plus supporting documentation. There is no shared build system, package manifest, dependency lockfile, or test suite spanning the repo; each artifact stands alone.

## Layout

- `cyber-tools/` — `leak_detector.py`, a standalone Python CLI that regex-scans text files for leaked secrets/PII. `leaks.txt` is its test fixture.
- `smart-contracts/` — `SimpleVoting.sol`, a standalone Solidity contract (no Hardhat/Foundry project; the README shows deployment via Remix or a hypothetical Hardhat setup that does not exist in-repo).
- `docs/overview.md` — long-form written analysis of the Web3 security landscape. Pure prose, no code.
- `.github/workflows/code-quality.yml` — the only automation tying the pieces together (see CI section).
- Each subdirectory has its own README; the root `README.md` is the portfolio overview.

## Commands

There is no `make`, `npm`, or `pip` project to install. Work directly with the files.

```bash
# Run the leak detector (defaults to cyber-tools/leaks.txt if no arg)
python cyber-tools/leak_detector.py [target_file]

# Optional dependency — only affects colored output; the tool degrades gracefully without it
pip install colorama

# Lint the Python tool (matches CI)
pylint cyber-tools/leak_detector.py

# Lint Solidity (matches CI; installed globally via npm in CI)
solhint smart-contracts/SimpleVoting.sol
```

There are no unit tests. "Testing" the leak detector means running it against `cyber-tools/leaks.txt` and confirming it reports findings across all categories at `RISK LEVEL: HIGH`.

## CI (`.github/workflows/code-quality.yml`)

Runs on push/PR to `main` and `develop`. Five jobs: Python quality (pylint), Solidity quality (solhint), security/leak scan (runs `leak_detector.py` over all `*.md`/`*.txt`/`*.yml`), documentation presence checks, and project-structure validation. **Every quality step is suffixed with `|| true`**, so the workflow is informational and will not fail the build on lint/scan issues. The structure and documentation jobs assert that specific files exist (`SimpleVoting.sol`, `leak_detector.py`, `leaks.txt`, `docs/overview.md`, the READMEs) and that the root README contains the author attribution and the words "Web3"/"Cyber" — renaming or moving these files will break those assertions.

## Conventions and gotchas

- **`leaks.txt` must only ever contain obviously-fake placeholder values** (e.g. `sk_test_FAKE_KEY_FOR_TESTING_ONLY`). GitHub push protection / secret scanning blocks pushes containing realistic-looking credentials — a prior commit existed specifically to neutralize values that tripped this. When editing test data, keep secrets clearly synthetic.
- **No external calls, no native ASCII-only output for cross-platform safety.** `leak_detector.py` console output uses bracketed ASCII tags like `[EMAIL]`, `[PASSWORD]`, `[RISK]` rather than emoji (a prior commit fixed Unicode encoding errors on Windows). Preserve this style when adding output; do not reintroduce emoji into the Python tool's stdout. (The Markdown READMEs do use emoji — that's fine, they aren't executed.)
- **Adding detection patterns:** extend the `password_patterns` dict or the standalone pattern attributes in `LeakDetector.__init__`, and add a matching `self.findings` category plus a branch in `scan_file` / `generate_report`. Risk level is derived in `generate_report`: HIGH if passwords/api_keys/credit_cards found, MEDIUM if emails/hashes, else LOW.
- **Solidity:** pinned to `^0.8.19`. The contract deliberately avoids external calls (its stated reentrancy-safety argument). Keep access control via the existing `onlyOwner` / `onlyAuthorizedVoter` / `validProposal` modifiers and emit an event for every state change, matching the existing pattern.
- Author attribution ("Abdulaziz Althari") appears in file headers and is asserted by CI — keep it intact.
