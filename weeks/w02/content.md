# M02 content: Reproducible Projects, Git and Code Quality (Week 2)

Topic-based teaching content for Week 2. Daniel learns the module from this file. The deck, practical, quiz and instructor notes in this folder are built from it.

| Field | Value |
|---|---|
| Work item | M02-PACKAGE (Week 2 package) |
| Author | Claude, 2026-10-08 |
| Reviewer | Codex |
| Scope authority | `CURRICULUM.md` Week 2 (Big question, 5 objectives, Concepts, Practical 2, Quiz 2) |
| Evidence | `source-map.md` (with its "Corrections from M02-RESEARCH" table), `evidence/notes.md` Parts A to C, `evidence/videos.md`, `research.md` |
| Code | Tag `m02` = e057569 (answer key). Branch `start-m02-v2` = f3c03dd (starter: `m02` with 3 functions left as TODO) |

**How to read this file.** Topics follow the session plan. Each topic has an objective, the explanation, the diamond example, limits and common mistakes, a diagram spec, the demo or practical link, and Sources. Measured numbers name the command and the revision. Fictional examples are labeled.

**The diamond numbers** (measured, `make train` at `m02`): HistGradientBoosting, seed 42, 10,755 holdout rows, MAE 279.29 USD, RMSE 524.92 USD, R2 0.9826. Full precision is in `AGENTS.md` section 10. The package prints MAE `279.292629032577`, within the 1e-6 tolerance.

---

## Topic 1. Why notebooks break, and what "reproducible" means

**Objective.** Students can explain why a notebook result is hard to reproduce and can state the reproducibility equation. (Objective 1.)

**Explanation.**
- Reproducible means: **same code + same data + same config + same environment = same result.** Change any one input and you may get a different number. The other four weeks of "ops" build on this: Week 3 versions the data, Week 4 records the config and code of every run, Week 7 freezes the environment in an image.
- In production, "reproduce" means rerunning our own pipeline and getting the same `metrics.json`. It does not mean repeating a paper.
- Notebooks hide four problems:
  1. **Hidden state.** Variables live in the kernel's memory. A cell can use a value that no visible cell produces any more.
  2. **Out-of-order execution.** You can run the split cell before the cleaning cell. The notebook shows the code but not the order you ran it in.
  3. **Copy-paste reuse.** The same cleaning code gets pasted into a second notebook and drifts.
  4. **No tests.** Nothing checks that cleaning drops the right rows or that the config matches the model.
- Hardcoded paths and parameters make it worse: `SEED = 42` in the imports cell, `test_size=0.2` inside the split cell. To change an experiment you edit code.
- A notebook is still the right tool for exploring. The problem starts when the notebook is the only way to produce the model.

**Diamond example.**
- Our notebook (`diamond-mlops/notebooks/01_diamond_exploration.ipynb`) says this itself in its last cell: monolithic, stateful, hardcoded, no tests, no one-command reproduce.
- Out-of-order demo (measured for M02-RESEARCH on the `m02` data, `evidence/notes.md` Part C section 4):
  - Cells are named by notebook section. JupyterLab shows no cell numbers. The imports cell at the top sets `SEED = 42`. Section 1 (load) reads the CSV: 53,940 rows. Section 2 (cleaning) drops 146 duplicates, then 19 zero-dimension rows: 53,775 rows. Section 4 (feature preparation) splits 80/20.
  - Run in order: holdout 10,755 rows, train 43,020 rows.
  - Skip the cleaning cell (restart, run the imports cell, the section 1 cell, then the section 4 cell): holdout 10,788 rows. Same code, different data in the split, different metrics.
- The old diamond notebook once scored its model on rows it had trained on. Nobody saw it, because a notebook has no test that says "evaluate on the holdout". `evaluate.py` now names this in its docstring.

**Limits and common mistakes.**
- The raw file has 20 zero-dimension rows. One is also a duplicate, so cleaning removes 165 rows, not 166. Say "146 duplicates, then 19 zero-dimension rows".
- Do not say notebooks are bad. Say notebooks are for exploring, packages are for running.

**Diagram spec.** (a) Four inputs (code, data, config, environment) into one box "same result". (b) Two runs of the same cells: 1 → 3 → 5 → 12 gives 10,755 holdout rows; 1 → 3 → 12 gives 10,788.

**Demo link.** Session 0:15 to 0:50. Open the notebook, restart the kernel, run only the imports cell, the section 1 cell and the section 4 cell, show `len(X_test)` = 10,788. Then "Restart and run all": 10,755.

**Sources.** Notebook imports cell, sections 1, 2, 4 and 9 at tag `m02`; `evidence/notes.md` Part C section 4; scikit-learn "Common pitfalls and recommended practices", section "Controlling randomness" (https://scikit-learn.org/stable/common_pitfalls.html, checked 2026-10-06); `sources/planning/Diamond_Notebook_Audit.md` (training-row scoring story).

---

## Topic 2. Project layout: from notebook cells to a package

**Objective.** Students can map notebook sections to package modules and say why the code lives in `src/`. (Objective 2.)

**Explanation.**
- A Python **package** is a folder of modules you can import by name: `from diamond.preprocess import clean`. Each module has one job.
- The **`src/` layout** puts the package under `src/`. Tests must then import the *installed* package, not whatever folder you happen to be in. This catches "works on my machine" import bugs early. `make install` installs the package in editable mode (`pip install -e .`), so edits take effect without reinstalling.
- Top level of the project: `src/` (code), `tests/`, `params.yaml` (experiment settings), `pyproject.toml` (package metadata, pins, tool settings), `Makefile` (commands), `.gitignore`, `.pre-commit-config.yaml`.
- Each module has a `python -m diamond.<module>` entry point. The Makefile calls those.
- One preprocessing function serves both training and prediction. The saved pipeline contains the preprocessor, so prediction cannot drift from training (train/serve skew).

**Diamond example.** Cell-to-module map at `m02`:

| Notebook section | Module | Job |
|---|---|---|
| 1. Load | `data.py` | Read `data/raw/diamonds.csv`; clear error if missing |
| 2. Clean, 4. Feature preparation (split) | `preprocess.py` | `clean()`, `build_preprocessor()`, `split()` |
| Constants | `config.py` | Paths, feature lists, quality order, `load_params()` |
| 5. Bake-off, 6. Tune | `train.py` | `candidate_models()`, `build_model()`, `train()` |
| 7. Holdout and 7.1 baseline | `evaluate.py` | Scores, baseline, `metrics.json` |
| 8. Persist | `predict.py` | Load the pipeline, predict one record |

- Five of the seven modules name their notebook cell in the docstring ("Notebook equivalent: ..."). `config.py` and `__init__.py` do not.
- `pyproject.toml` lines 28 to 29 tell setuptools to find packages under `src`.

**Limits and common mistakes.**
- Running `python src/diamond/train.py` fails on the relative imports. Use `python -m diamond.train` (or `make train`).
- A test that passes only because you ran pytest from inside `src/` is not a real pass. The editable install removes that trap.

**Diagram spec.** Left: notebook sections as stacked cells. Right: the six `src/diamond/` files. Arrows per row of the table above.

**Demo link.** Session 1:25 to 2:10, live refactor of 2 notebook sections: show the section 2 cell next to `preprocess.clean()`, and the section 4 cell next to `preprocess.split()`.

**Sources.** `diamond-mlops/README.md` lines 55 to 66 and `src/diamond/*.py` at `m02`; Python Packaging User Guide, "src layout vs flat layout" (https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/, checked 2026-10-06); pytest "Good Integration Practices" (https://docs.pytest.org/en/stable/explanation/goodpractices.html, checked 2026-10-06).

---

## Topic 3. Config outside code: `params.yaml`

**Objective.** Students can move every experiment setting into `params.yaml` and explain why a missing config must fail. (Objective 2.)

**Explanation.**
- Rule: every value that changes an experiment result lives in `params.yaml`. Code reads it; code never repeats it.
- Benefits: one place to change; `git diff params.yaml` shows exactly what changed between two runs; Week 3 (DVC) and Week 4 (MLflow) read the same file.
- What stays in code: things that are facts, not choices. The feature names and the quality order of `cut`, `color` and `clarity` are facts about the data, so they live in `config.py`.
- **Silent defaults are a bug.** If the config file is missing and the code quietly uses built-in defaults, you train a model nobody asked for. `load_params()` opens the file directly, so a missing file raises `FileNotFoundError`.
- Use `yaml.safe_load`, never `yaml.load` without a safe loader: `safe_load` builds only plain data (dicts, lists, numbers, strings).

**Diamond example.**
- `params.yaml` at `m02`: `seed: 42`, `test_size: 0.2`, `model.name: HistGradientBoosting`, `model.params: {max_iter: 400, learning_rate: 0.05, max_depth: null}`. The values come from the notebook's tuning cell.
- `preprocess.split()` reads `seed` and `test_size`. `train.train()` reads `model.name` and `model.params`. Nothing in `src/` names the model.
- The YAML comment warns: HistGradientBoosting takes `max_iter`, not `n_estimators`. The test `test_unknown_model_and_invalid_hyperparameter_fail` proves a wrong key fails at test time, not after 2 minutes of training.
- The course reference repo once returned defaults when `params.yaml` was missing. `m02` removed that, and `test_missing_config_fails_instead_of_silently_using_defaults` guards it.

**Limits and common mistakes.**
- `max_depth: null` in YAML becomes Python `None` (unlimited depth). Students often write `None`, which YAML reads as the string `"None"`.
- Hydra (used by Psitron) is a richer config tool. Name it as an option only.

**Diagram spec.** `params.yaml` in the center; arrows to `preprocess.split()` (seed, test_size) and `train.build_model()` (name, params); a dashed arrow to "Week 3 DVC, Week 4 MLflow".

**Demo link.** Change `learning_rate` to 0.1 and run `make train`: MAE 282.76, RMSE 530.14, R2 0.9822 (measured 2026-10-08). The diff in `params.yaml` explains the diff in `metrics.json`. Then `git restore params.yaml`.

**Sources.** `params.yaml`, `src/diamond/config.py` lines 32 to 36, `src/diamond/train.py` lines 90 to 113, `tests/test_config_matches_code.py` at `m02`; PyYAML CHANGES 6.0 and safety warning (`evidence/notes.md` Part A1 item 11, checked 2026-10-06).

---

## Topic 4. Dependencies and environments

**Objective.** Students can create the project environment with one command and explain pins and the lock file. (Objective 2.)

**Explanation.**
- A **virtual environment** (`.venv`) is a private copy of Python packages for one project. Two projects never fight over versions.
- A **pin** fixes the exact version: `scikit-learn==1.7.2`. Without pins, a library release can change your results or break your code with no change on your side.
- Two files:
  - `pyproject.toml` lists the *direct* dependencies with exact pins, plus the dev tools (pytest, black, ruff, pre-commit).
  - `requirements.txt` is the **lock file**: every package, including dependencies of dependencies, with exact versions and hashes. `requirements.in` is its short input.
- `pip install --require-hashes` refuses any file whose hash does not match the lock. You get the same versions on every machine, and each downloaded file is checked. Linux and macOS may download different wheel files of the same version; each is still checked against a recorded hash.
- Python is pinned to 3.12 only (`requires-python = ">=3.12,<3.13"`). The Python packaging guide warns against upper bounds for libraries. For a course app it is right: every student runs the same interpreter.

**Diamond example.** `Makefile` `install` target at `m02`:
```
python3.12 -m venv .venv
$(PYTHON) -m pip install --require-hashes -r requirements.txt
$(PYTHON) -m pip install --no-deps --no-build-isolation -e .
$(PYTHON) -m pip check
```
Line 3 installs our package without fetching anything new. `pip check` confirms nothing conflicts.

**Limits and common mistakes.**
- `pip install pandas` inside `.venv` "to fix something" breaks the lock. Change `requirements.in`, regenerate, commit both files.
- Students on an Ubuntu other than 24.04 get "command not found" for `python3.12`. Plain `wsl --install` gives Ubuntu 26.04, which has Python 3.14 only. Week 0 setup installs `Ubuntu-24.04`, which ships Python 3.12.
- Alternatives: conda (also manages non-Python libraries), poetry and uv (manage pins and the lock for you). The course uses venv + pip because every other tool builds on it.

**Diagram spec.** `requirements.in` (direct pins) → compile step → `requirements.txt` (all pins + hashes) → `make install` → `.venv`.

**Demo link.** Run `make install` live only if the network is fast; otherwise show the terminal from a prepared run.

**Sources.** `pyproject.toml`, `requirements.in`, `requirements.txt`, `Makefile` lines 9 to 13 at `m02`; pip "Secure installs" (https://pip.pypa.io/en/stable/topics/secure-installs/), Python `venv` docs (https://docs.python.org/3/library/venv.html), Packaging guide "Writing your pyproject.toml" (https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), all checked 2026-10-06.

---

## Topic 5. Make: one command per job

**Objective.** Students can run and read the project Makefile. (Objective 2.)

**Explanation.**
- A **Makefile** gives each job a short name: `make install`, `make train`, `make test`. A new team member does not need to know the long commands.
- The same locked tools run in three places. You run the Make targets in your terminal. GitHub Actions runs `make install`, `make lint` and `make test`. The pre-commit hook runs ruff and black directly on staged files, with no tests. Same tool versions everywhere means the same lint result everywhere.
- Rules: a recipe line starts with a **tab**, not spaces. `.PHONY` lists targets that are jobs, not files, so `make test` runs even if a file called `test` exists. `$(PYTHON)` is a variable.
- A bare `make` runs the first target. In our Makefile that is `install`. Always name the target.

**Diamond example.** At `m02` the Makefile has 8 targets: `install`, `train`, `evaluate`, `test`, `lint`, `format`, `hooks`, `predict`. `make train` runs `python -m diamond.train` then `python -m diamond.evaluate`, so every training run writes `metrics.json`. Lines 2 to 6 limit CPU threads to keep laptop memory use predictable.

**Limits and common mistakes.**
- `Makefile:<line>: *** missing separator.  Stop.` means a recipe line starts with spaces. VS Code can convert tabs; set the Makefile to use tabs.
- Make is standard on Linux and macOS. Windows students run it inside WSL2 Ubuntu.

**Diagram spec.** Three boxes: terminal (`make lint`, `make test`), pre-commit (ruff and black on staged files, no tests), GitHub Actions (`make install`, `make lint`, `make test`). All point to one box: the same locked tools in `.venv`.

**Sources.** `Makefile` at `m02`; GNU Make manual, "Phony Targets" and "Recipe Syntax" (https://www.gnu.org/software/make/manual/make.html, verified 2026-10-06 from the manual source on GNU Savannah).

---

## Topic 6. Git basics: commits, staging, `.gitignore`, undoing safely

**Objective.** Students can commit, inspect and undo changes safely, and keep generated files out of Git. (Objective 3.)

**Explanation.**
- Git tracks snapshots of a project. Three local areas: the **working directory** (files you edit), the **staging area** (what goes into the next commit) and the **repository** (the commit history). A **remote** (GitHub) is a shared copy.
- Daily commands: `git status`, `git diff`, `git add <file>`, `git commit -m "..."`, `git log --oneline`, `git push`, `git pull`.
- One-time setup: `git config --global init.defaultBranch main` (`git init` still makes `master` otherwise) and `git config --global core.editor "code --wait"` (avoid getting stuck in vim).
- **What never goes in Git:** `.venv/`, `models/`, `.env`, caches. `.gitignore` lists them. A model file is an output: anyone can rebuild it with `make train`.
- **Undoing:**
  - Discard an unstaged edit: `git restore <file>`.
  - Get one file back from an older commit: `git restore --source=<commit> -- <file>`.
  - Undo a commit that is already pushed: `git revert --no-edit <commit>`. It adds a new commit that reverses the old one. History stays intact for everyone.
  - `git reset --hard <commit>` deletes commits and uncommitted work. Never use it on commits you pushed. It cannot take a file path; `git reset --hard HEAD~1 -- file` fails with `Cannot do hard reset with paths`.
- `git switch <branch>` and `git switch -c <new-branch>` replace the older `git checkout` for branches. Git 2.43 (Ubuntu 24.04) marks `switch` and `restore` as "experimental" in its manual. They are safe to use; the label was removed in Git 2.51.

**Diamond example.**
- `diamond-mlops/.gitignore` at `m02` has 12 lines, including `.venv/`, `.env`, `models/` and `notebooks/executed/`. After `make train`, `git status` shows a clean tree.
- `.gitattributes` keeps Linux line endings for `*.sh`, `*.py`, `*.yaml`, `*.toml` and `Makefile`. Without it, Windows Git can add CRLF endings and break Bash scripts and Make.
- Spot the bug: a `.gitignore` line `.bin` matches only a file literally named `.bin`. `model.bin` is still committed. The fix is `*.bin`.

**Limits and common mistakes.**
- Older material (Psitron, the old Git deck) teaches `master`, `git checkout -b` and `git reset --hard <commit> -- <file>`. The last form is wrong. Use the commands above.
- `git add .` stages every file that `.gitignore` does not cover, for example a stray `aws-keys.txt` or `credentials.json`. `.gitignore` already covers `.env`. Prefer `git add <file>` and read `git status` first.
- `git revert` without `--no-edit` opens an editor. If it is vim: type `:wq` and press Enter.

**Diagram spec.** (a) Working directory → `git add` → staging → `git commit` → repository → `git push` → remote. (b) Reset vs revert: reset moves the branch back and drops C3; revert adds C4 that undoes C3.

**Sources.** `.gitignore`, `.gitattributes` at `m02`; Git reference pages git-switch, git-restore, git-revert, git-reset, gitignore, gitattributes (https://git-scm.com/docs, checked 2026-10-06, behaviors tested on Git 2.43.0); GitHub Docs "Associating text editors with Git" (checked 2026-10-06); `evidence/notes.md` Part A2.

---

## Topic 7. Branching strategy: GitHub Flow

**Objective.** Students can work on a short feature branch and merge it through a pull request. (Objective 3.)

**Explanation.**
- **GitHub Flow** (the course default): `main` is always working. For each change: create a branch from `main`, commit, push, open a pull request, checks run, a teammate reviews, merge, delete the branch.
- Branches are cheap. One branch per small change. Small PRs get reviewed faster and break less.
- Alternatives:
  - **Trunk-based development:** everyone commits to `main` (or very short branches, hours not days), with strong automated tests. Used by small and very large teams. It is close to GitHub Flow.
  - **Git Flow:** long-lived `develop` and `release` branches. Made for software shipped as scheduled releases. Heavy for a team that deploys often.

**Diamond example.** All Week 2 practical work happens on a branch called `week2-refactor`. This build repo works the same way: each module's code arrives as one pull request.

**Limits and common mistakes.**
- Some sources say trunk-based is "for small teams". Do not repeat that; large companies use it too.
- Working directly on `main` and pushing skips review and checks. Branch protection (Topic 8) can block it.

**Diagram spec.** A loop: branch → commits → push → PR → checks → review → merge → delete branch → back to `main`.

**Sources.** GitHub Docs "GitHub flow" (https://docs.github.com/en/get-started/using-github/github-flow, checked 2026-10-06); trunkbaseddevelopment.com (community site, checked 2026-10-06).

---

## Topic 8. Pull requests, code review and merge conflicts

**Objective.** Students can open a PR, review a classmate's PR, and resolve a merge conflict by hand. (Objective 3.)

**Explanation.**
- A **pull request** (PR) asks to merge one branch into another. The PR page shows the diff, the check results and the review comments.
- **What a reviewer checks** on ML code:
  1. Does it do what the PR says? Read the diff, not the description.
  2. Do tests cover the change, and do the checks pass?
  3. Does config agree with code? No new hardcoded numbers.
  4. No secrets, no `.env`, no model or data files.
  5. Can I understand it? Names, small functions.
- Review outcomes on GitHub: **Comment**, **Approve**, **Request changes**.
- A **merge conflict** happens when two branches change the same lines. Git stops and marks the file:
  ```
  <<<<<<< HEAD
      learning_rate: 0.1
  =======
      learning_rate: 0.03
  >>>>>>> lr-slow
  ```
  The part above `=======` is your current branch. The part below is the branch you merge in. You edit the file to the right final text, delete all three marker lines, then `git add <file>` and `git commit`.
- **Branch protection** can require a passing check and an approving review before merge. It is free for public repositories. Private repositories need a paid GitHub plan (Pro, Team or Enterprise).

**Diamond example.** The known-answer conflict exercise: two branches change `learning_rate` in `params.yaml` (0.1 and 0.03). The team decision is to keep 0.05. After resolving, `make train` must print MAE 279.29 again. The metrics prove the answer. Measured 2026-10-08: committing with the markers still in the file fails the `check-yaml` hook (`could not find expected ':'`); after the fix, MAE is `279.292629032577`.

**Limits and common mistakes.**
- Leaving a marker line in `params.yaml`. YAML fails to parse, and the `check-yaml` hook stops the commit. That is the hook doing its job.
- Resolving by picking "both" in VS Code without reading. For a single value you need one line.
- GitHub's conflict guide uses `git add .`. Prefer `git add params.yaml`.

**Diagram spec.** The conflict block above on a real `params.yaml` line, with labels "your branch" and "incoming branch". A PR page sketch: diff, checks, review, merge button.

**Demo link.** Session 2:10 to 2:40: branch, PR, review, conflict, live on the demo repo.

**Sources.** GitHub Docs "Pull request reviews" (https://docs.github.com/en/pull-requests/reference/pull-request-reviews), "Resolving a merge conflict using the command line" (https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line), "Branches" and protected branches (https://docs.github.com/en/pull-requests/reference/branches), all checked 2026-10-06; Pro Git "Basic Branching and Merging".

---

## Topic 9. Linting vs formatting: ruff and black

**Objective.** Students can tell a lint error from a format change and fix both with Make. (Objective 4.)

**Explanation.**
- A **linter** reads code and reports likely bugs and bad patterns: an unused import, an undefined name, a mutable default argument. **ruff** is our linter.
- A **formatter** rewrites the layout of code (spacing, line breaks, quotes) to one style. It does not change behavior. **black** is our formatter.
- Why bother: lint finds bugs before they run. A formatter ends style arguments, so a diff shows only real changes.
- `make lint` only *checks* (`ruff check` and `black --check`) and fails if anything is wrong. CI runs this. `make format` *fixes* (`ruff check --fix` and `black`). You run it.
- Ruff rule letters in our config: `E` and `W` (pycodestyle errors and warnings), `F` (Pyflakes: unused imports, undefined names), `I` (import order), `B` (bugbear: likely bugs), `UP` (upgrade old syntax).
- Name the rules explicitly. Ruff 0.16.0 (July 2026) changed its default rule set from 59 to 413 rules. A project without `select` got new errors overnight. Ours did not.

**Diamond example.** `pyproject.toml` lines 31 to 40 at `m02`: black and ruff both use line length 100, so they never disagree. `[tool.ruff.lint] select = ["E", "W", "F", "I", "B", "UP"]`.

Demo (measured on `start-m02-v2` with the TODOs filled, 2026-10-08): in `src/diamond/preprocess.py`, add `import os` as its own block, with one blank line before and one after, right below `from __future__ import annotations`. `make lint` reports `Found 1 error.`: F401, `os` imported but unused. `make format` removes the line again.

**Limits and common mistakes.**
- Place the demo import exactly as above. Without the blank line after it, ruff also reports I001 (import order): 2 errors. On line 1 it reports 9 errors and hides the lesson.
- Older tutorials put `select` directly under `[tool.ruff]`. That form is deprecated; use `[tool.ruff.lint]`.
- Ruff also has a formatter (`ruff format`), designed as a drop-in for black. Pick one formatter; do not alternate.

**Diagram spec.** One code snippet, two panels: left "linter says" (F401 flagged), right "formatter does" (spacing changed, behavior same).

**Sources.** `pyproject.toml` lines 31 to 40 and `Makefile` lines 26 to 32 at `m02`; Ruff "Configuring Ruff", rules list and formatter pages (https://docs.astral.sh/ruff/, checked 2026-10-06); Black docs (https://black.readthedocs.io/en/stable/, checked 2026-10-06); hands-on tests at the pinned versions, `evidence/notes.md` Part A3 section 7.

---

## Topic 10. pre-commit hooks

**Objective.** Students can install the hooks and recover when a hook stops a commit. (Objective 4.)

**Explanation.**
- A **Git hook** is a script Git runs at a fixed moment. **pre-commit** is a tool that manages hooks that run before each commit, on the staged files.
- If a hook fails, there is no commit. If a hook *fixes* a file (black reformats it), the commit also stops, because the fixed file is not staged. Read the change, `git add` it, and commit again.
- The hooks must use the same tool versions as `make lint` and CI. Otherwise the hook passes and CI fails, or the reverse.
- Hooks are installed per clone with `make hooks`. A fresh clone has none until you run it.

**Diamond example.** `.pre-commit-config.yaml` at `m02` has 4 local hooks: ruff, black, end-of-file-fixer and check-yaml. All call executables in `diamond-mlops/.venv/bin/`, the same locked versions as `make lint`. The paths start with `diamond-mlops/` because pre-commit runs from the Git root, one folder above the project.

**Limits and common mistakes.**
- "My commit vanished": a hook edited a file. `git status`, `git add`, commit again.
- `git commit --no-verify` skips hooks. CI runs ruff and black again through `make lint`, so those failures only move later. CI does not run `end-of-file-fixer` or `check-yaml`, so those problems can reach a green PR. Do not skip hooks.
- Our config uses `language: system`. pre-commit 4.4.0 renamed it `unsupported`; the old name still works in our pinned 4.6.2.
- Running the full test suite in a hook makes every commit slow. Keep tests in `make test` and CI.

**Diagram spec.** `git commit` → hooks (ruff, black, end-of-file, check-yaml) → pass: commit created; fail or fixed: read, `git add`, commit again.

**Sources.** `.pre-commit-config.yaml`, `Makefile` line 35, README lines 84 to 108 at `m02`; pre-commit docs (https://pre-commit.com/, checked 2026-10-06); `evidence/notes.md` Part A3 sections 5 and 7.

---

## Topic 11. Testing ML code with pytest

**Objective.** Students can write a small pytest unit test for preprocessing and explain the config-matches-code test. (Objective 5.)

**Explanation.**
- **pytest** finds files named `test_*.py` and runs every function named `test_*`. A test passes when no `assert` fails.
- What to test in ML code this week:
  1. **Preprocessing** on a tiny hand-made DataFrame: you know the exact right answer.
  2. **Shapes and contracts:** 9 output columns; unknown categories fail loudly.
  3. **Config, code and artifact agree:** `params.yaml` names a model the code can build, with valid hyperparameters, and the saved model and `metrics.json` match it.
- What *not* to test this week: "the model is good enough". That is a quality gate, Week 9.
- Tools: `tmp_path` gives a temporary folder; `monkeypatch` swaps a value for one test (for example a path).
- Tests should be fast. All 13 `m02` tests run in seconds because none trains the real model.

**Diamond example.**
- `tests/test_preprocess.py` (5 tests): zero-dimension rows are dropped; the preprocessor outputs 9 columns; duplicates are removed and the input is not changed; `Ideal` encodes above `Premium` and an unknown cut fails; the split is repeatable and disjoint.
- `tests/test_config_matches_code.py` (7 tests) exists because of a real defect: `params.yaml` named one model, `metrics.json` another, and the code could build neither. The repo could not regenerate its own results.
- `tests/test_predict.py` (1 test) saves and reloads a tiny `LinearRegression` pipeline in `tmp_path`. It checks the prediction contract, not the trained model.
- On a fresh clone, `make test` gives 11 passed and 2 skipped. The 2 artifact tests need `models/` from `make train`. After training: 13 passed.
- Practical TODO: in `test_clean_removes_duplicates_without_changing_input`, the student writes `assert len(clean(df)) == 2`. Three rows plus one duplicate, minus one zero-dimension row, gives 2.

**Limits and common mistakes.**
- Zoomcamp homework says tests need `tests/__init__.py`. With our `src/` layout and editable install, they do not.
- A test that reads the full CSV and trains is an integration test. Keep it out of the fast suite.

**Diagram spec.** Test ladder: unit (preprocess, Week 2) → contract (config matches code and artifact, Week 2) → data validation (Week 3) → quality gate (Week 9).

**Sources.** `tests/` at `m02`; pytest "Good Integration Practices", "How to monkeypatch", "How to use temporary directories" (https://docs.pytest.org/, checked 2026-10-06); `evidence/notes.md` Part C section 1.

---

## Topic 12. Seeds and determinism: `make train` twice

**Objective.** Students can prove a training run is repeatable. (Objective 2; the week's evidence.)

**Explanation.**
- A random seed fixes the sequence of "random" numbers. The same seed gives the same split and the same model.
- In `m02` the seed comes from `params.yaml` and goes to two places: `train_test_split(random_state=seed)` and each model's `random_state`.
- Pinned library versions matter as much as the seed. A scikit-learn upgrade moved the diamond MAE from 279.29 to 278.16 with the same seed.
- **Proof:** run `make train` twice and compare the two `metrics.json` files byte for byte with `cmp`. No output means identical.

**Diamond example.** README lines 42 to 47 at `m02`:
```
make train
cp models/metrics.json /tmp/diamond-metrics-first.json
make train
cmp /tmp/diamond-metrics-first.json models/metrics.json
```
Measured for M02-RESEARCH: the two runs were byte-identical. `metrics.json` also holds the linear baseline on the same split and the MAE on stones above 10,000 USD, so a single score is never read alone.

**Limits and common mistakes.**
- The Makefile limits threads for memory reasons. Do not teach "limit threads to get the same result" as a scikit-learn rule; the official docs do not say it.
- Comparing MAE to the notebook as a string fails (`279.292629032577` vs `279.29262903257705`). Compare numbers with a tolerance.

**Diagram spec.** Run 1 and run 2 → two `metrics.json` → `cmp` → no output = same result.

**Sources.** README lines 37 to 47, `Makefile` lines 2 to 6, `preprocess.split()`, `train.candidate_models()` at `m02`; scikit-learn "Controlling randomness" (checked 2026-10-06); `evidence/notes.md` Part C section 1; `AGENTS.md` section 10 (the 278.16 note).

---

## Topic 13. A first automatic check: GitHub Actions

**Objective.** Students can read a green or red check on their PR and run the same commands locally. (Concept: first automatic check. Week 9 explains every line.)

**Explanation.**
- **GitHub Actions** runs a workflow file from `.github/workflows/` on GitHub's machines when an event happens, such as a push or a PR.
- Our workflow `checks.yml` runs three commands on every push and PR: `make install`, `make lint`, `make test`. The result shows as a green tick or a red cross on the PR.
- It runs the same Make targets you run, so "it passed on my machine" and "it passed in CI" mean the same thing.
- Two safety details students will see again in Week 9: `permissions: contents: read` (the workflow's `GITHUB_TOKEN` cannot write to the repository; the job's steps still run code on the runner) and actions pinned to a full commit SHA instead of a moving tag.
- CI does not train on every push yet. Week 9 adds training and a quality gate.

**Diamond example.** `.github/workflows/checks.yml` at `m02` (repository root): Ubuntu 24.04 runner, Python 3.12.14, `working-directory: diamond-mlops`.

**Limits and common mistakes.**
- The workflow lives at the repository root, not inside `diamond-mlops/`. A copy in the wrong folder never runs.
- Required status checks treat a *skipped* check as passing.
- Red check: open the failed step's log, find the first error, run the same `make` target locally.

**Diagram spec.** Shared with Topic 5: three places, same locked tools.

**Sources.** `.github/workflows/checks.yml` at `m02`; GitHub Docs "Building and testing Python" (https://docs.github.com/en/actions/tutorials/build-and-test-code/python) and "Secure use reference" (https://docs.github.com/en/actions/reference/security/secure-use), checked 2026-10-06.

---

## Topic 14. Safe loading of model files

**Objective.** Students know that loading a model file can run code. (Supports review checklist item 4.)

**Explanation.** `joblib` and `pickle` files can execute Python code when loaded. Load only files you trained or trust. This is one more reason model files stay out of Git and get rebuilt by `make train`. The joblib docs now point to `skops.io` for models from outside your team.

**Diamond example.** README lines 81 to 82 at `m02`; `predict.py` loads `models/diamond_pipeline.joblib`.

**Sources.** joblib persistence docs (https://joblib.readthedocs.io/en/stable/user_guide/persistence.html, checked 2026-10-06).

---

## How the topics fit the Week 2 session

| Time | Part | Topics |
|---|---|---|
| 0:00 to 0:15 | Recap Week 1, practical questions | |
| 0:15 to 0:50 | Why notebooks break; live out-of-order run | 1 |
| 0:50 to 1:15 | Layout, config, dependencies, Make | 2, 3, 4, 5 |
| 1:15 to 1:25 | Break | |
| 1:25 to 2:10 | Live refactor of 2 notebook sections; seeds; `make train` twice | 2, 12 |
| 2:10 to 2:40 | Git live: branch, PR, review, conflict | 6, 7, 8 |
| 2:40 to 3:00 | ruff, black, pre-commit, pytest, the CI check | 9, 10, 11, 13 |
| 3:00 to 3:25 | Practical start | |
| 3:25 to 3:30 | Wrap, quiz, Week 3 preview | |

## Slide candidates

- Where we are (Week 2 lit). The big question. The reproducibility equation (diagram).
- Out-of-order demo: 10,755 vs 10,788 (diagram).
- Notebook to package map (diagram). Project tree. `params.yaml` snippet. Silent defaults are a bug (`config.py` snippet).
- Pins and the lock (diagram). Makefile snippet. Same tools in three places (diagram).
- Git three areas (diagram). Undo table: restore, revert, reset. `.gitignore` snippet. GitHub Flow loop (diagram).
- Reviewer checklist. Conflict markers (diagram). Branch protection note.
- Lint vs format. Ruff config snippet. pre-commit flow (diagram). Test snippet. Test ladder.
- `make train` twice (README snippet). CI check.
- Alternatives table. Common mistakes table. Practical brief. Quiz topics. Next week.
- Speaker notes keep: the 165 vs 166 row detail, the ruff 0.16 default change, `language: system`, the `tests/__init__.py` myth, the thread-limit caveat.
