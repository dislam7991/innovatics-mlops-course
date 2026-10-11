---
module: m02
title: "Practical 2: Notebook to production refactor"
solution_tag: m02
start_branch: start-m02
grading: rubric below, part of the 40% practicals grade
time: about 2.5 hours (25 minutes in the session, the rest before Week 3)
source: modules/m02-reproducible-projects/content.md (M02-PACKAGE, 2026-10-08)
---

# Practical 2: Notebook to production refactor

## Goal

A notebook gives a result once. A team needs a project that anyone can run with one command and get the same result. In this practical you finish a Python package for the diamond model, prove that two runs give identical metrics, fix a merge conflict, and get your work reviewed in a pull request.

**This week's evidence:** a tested project; two runs give identical metrics; a reviewed pull request; an automatic check that runs on every push.

| Part | What you do | Time |
|---|---|---|
| A | Get the Week 2 starter. Make a branch. Install. See the 1 expected failure | 10 min |
| B | Trace the refactor. Fill the 3 `TODO M02` blocks | 40 min |
| C | Prove the run is reproducible: `make train` twice, then `cmp` | 15 min |
| D | Fix a merge conflict that has a known answer (local only) | 20 min |
| E | Open a pull request, pass the check, get a review, merge | 45 min, plus waiting for a classmate |

The starter already has the package, `params.yaml`, the `Makefile`, the pinned environment, the pre-commit hooks and the GitHub Actions check. You write 3 lines of code. The rest of the work is Git and review.

## Before you start

- Your Week 0 setup check passed, and `python3.12 --version` prints `Python 3.12.x`.
- You work in your Linux terminal (Ubuntu in WSL2 on Windows). On Windows, the bottom-left corner of VS Code says **WSL: Ubuntu**.
- You have a classmate who reviews your pull request. You review theirs.

## Part A. Set up the Week 2 starter

**A1. Get the starter into your own repo.** Run these from the root of your course repo (the folder that holds `diamond-mlops/`). Skip the `git remote add` line if `git remote -v` already shows `upstream` (Week 0 Step 7 added it).

```bash
git remote -v
git remote add upstream https://github.com/dislam7991/innovatics-mlops-course.git
git fetch upstream
git switch main
git merge --ff-only upstream/start-m02
git push origin main
git switch -c week2-refactor
```

- `upstream` is the course repo. `origin` is your fork. You push only to `origin`.
- After the push, the check on your `main` is red. This is expected: the starter has 1 failing test on purpose. Your pull request makes it green.
- `week2-refactor` is your feature branch. Do all Week 2 work on it.

**A2. Install, turn on the hooks, and run the checks.**

```bash
cd diamond-mlops
make install
make hooks
make lint
make test
make train
```

You should see:

- `make hooks` prints `pre-commit installed at .git/hooks/pre-commit`. From now on, ruff, black, end-of-file-fixer and check-yaml run before each commit.
- `make lint` passes.
- `make test` ends with `1 failed, 10 passed, 2 skipped`. The failed test is `test_clean_removes_duplicates_without_changing_input`. The 2 skipped tests need a trained model.
- `make train` stops with `NotImplementedError: TODO M02: fit the training pipeline`, then `make: *** [Makefile:17: train] Error 1`.

Each failure points to a `TODO M02` block. List all 3 with `grep -rn "TODO M02" src tests`.

## Part B. Trace the refactor, then fill the 3 TODO blocks

### B0. Trace the refactor (10 minutes)

The starter already holds the finished package, so you can spend your time on Git and review. First, see how the notebook became that package. Open `notebooks/01_diamond_exploration.ipynb` next to `src/diamond/`. Fill this table in your pull request description:

| Notebook section | Module and function that does the same job | One setting that moved to `params.yaml` (or "none") |
|---|---|---|
| 1. Data Ingestion & Loading | | |
| 2. Data Cleaning | | |
| 4. Feature Preparation | | |
| 6. Select & Tune the Best Model | | |
| 7. Final Evaluation on the Holdout Set | | |

Tip: five modules describe their matching notebook cell in the docstring at the top ("Notebook equivalent: ...").


Each block has 2 lines: a `# TODO M02` comment and a `raise NotImplementedError(...)` line. Replace **both lines** with **one line** of your own. Change nothing else.

### B1. Fit the model in `train()`

Open `diamond-mlops/src/diamond/train.py`. In `train()`, find the comment `# TODO M02: fit pipe on X_train and y_train`. The lines above it split the data and build `pipe`. The lines below it save the model.

**Hints.** `pipe` is a scikit-learn `Pipeline`. A pipeline learns from data with its `fit` method. `split(df)` returns 4 values; this function keeps only the training features and labels. The `_` values are the holdout. Training must never see them.

**Check.** Run `make train`. It now prints `Trained HistGradientBoosting ({'max_iter': 400, 'learning_rate': 0.05, 'max_depth': None}) on 43,020 rows`, then the path of the saved model. Then it stops at the next TODO: `NotImplementedError: TODO M02: add holdout scores to metrics`. That is correct for now.

### B2. Score the holdout in `evaluate()`

Open `diamond-mlops/src/diamond/evaluate.py`. In `evaluate()`, find the comment `# TODO M02: score pipe on the holdout and update metrics`. Just above it, `split(df)` gives the 4 data parts and `metrics` starts with the model name. Just below it, the baseline model is trained and scored.

**Hints.**
- `_score(y_true, preds)` (line 34) returns a dict with `mae`, `rmse` and `r2`. The true values come first.
- Score the holdout rows (`X_test`, `y_test`). Scores on training rows look too good. The old notebook made this mistake.
- Add the scores to `metrics`. Do not replace `metrics`: it already holds the model name.
- Read how the baseline is scored a few lines lower.

**Check.** Run `make train`. After the training line it prints `Holdout metrics:` and a JSON block. Compare these values:

| Key | Value |
|---|---|
| `mae`, `rmse`, `r2` | `279.292629032577`, `524.9243546483148`, `0.982563973914643` |
| `baseline` (LinearRegression) `mae` | `802.1583399331982` |
| `n_test`, `seed` | `10755`, `42` |
| `above_10000_usd` | `n_test` `1015`, `mae` `935.5063455800508` |

If `mae`, `rmse` or `r2` differ, go back to the hints.

### B3. Write the duplicate test

Open `diamond-mlops/tests/test_preprocess.py`. Find `test_clean_removes_duplicates_without_changing_input` and its comment `# TODO M02: assert the cleaned row count`. The test adds a copy of the first row to the 3 rows from `_tiny_df()`. The `x` column of `_tiny_df()` is `[3.95, 3.89, 0.0]`.

**Hints.** Count by hand first. How many rows does `df` have? Which row is a copy? Which row has a zero dimension? `clean()` removes both kinds. Write one `assert` that compares the length of `clean(df)` with your count. `test_clean_drops_zero_dimension_rows` in the same file shows the form.

**Check.** Run `make test`. It ends with `13 passed`. The 2 skipped tests now run, because `models/` exists.

## Part C. Prove the run is reproducible

**C1. Run the checks.** Run `make lint` and `make test`. Lint passes. Tests end with `13 passed`.

**C2. Train twice and compare.** From `diamond-mlops/README.md` at tag `m02`:

```bash
make train
cp models/metrics.json /tmp/diamond-metrics-first.json
make train
cmp /tmp/diamond-metrics-first.json models/metrics.json
```

`cmp` prints nothing. No output means the two files are identical, byte for byte. Same code, same data, same config and same environment give the same result. **Take a screenshot** of the terminal that shows the silent `cmp` and the `13 passed` line.

**C3. Commit your work.**

```bash
git status
git add src/diamond/train.py src/diamond/evaluate.py tests/test_preprocess.py
git commit -m "Fill Week 2 TODOs: fit, holdout scores, duplicate test"
```

- `git status` lists only the 3 files. `.gitignore` keeps `models/` and `.venv/` out of Git.
- The hooks run before the commit. If a hook changes a file, the commit stops. Read the change, run the same `git add` line again, and commit again.

## Part D. Fix a merge conflict with a known answer

Two teammates try different learning rates on separate branches. The team decides to keep `0.05`. You merge both branches and fix the conflict. **All branches in this part stay on your computer. Never push them.**

**D1. Make two branches that change the same line.** From `diamond-mlops/`, on `week2-refactor`:

```bash
git switch -c practice-base
git switch -c lr-fast
sed -i 's/learning_rate: 0.05/learning_rate: 0.1/' params.yaml
git commit -am "Try learning_rate 0.1"
git switch practice-base
git switch -c lr-slow
sed -i 's/learning_rate: 0.05/learning_rate: 0.03/' params.yaml
git commit -am "Try learning_rate 0.03"
git switch practice-base
```

Each `sed` line changes one value in `params.yaml`. You can also edit the line in VS Code.

**D2. Merge both branches.** Run `git merge lr-fast`, then `git merge lr-slow`. The first merge is a fast-forward. The second stops with `CONFLICT (content): Merge conflict in diamond-mlops/params.yaml`. Open `params.yaml`:

```
<<<<<<< HEAD
    learning_rate: 0.1
=======
    learning_rate: 0.03
>>>>>>> lr-slow
```

The part above `=======` is your current branch. The part below is the branch you merge in.

**D3. See the hook catch a mistake (optional).** Run `git add params.yaml` and `git commit --no-edit` with the markers still in the file. The `check-yaml` hook fails with `could not find expected ':'`. No commit is made. The hook stops broken config from entering Git.

**D4. Apply the team decision.** Replace the 5 lines (3 marker lines and 2 values) with this one line. Keep the 4 spaces at the start:

```
    learning_rate: 0.05
```

Then finish the merge and prove the answer:

```bash
git add params.yaml
git commit --no-edit
make train
git diff week2-refactor -- params.yaml
```

- `make train` prints `"mae": 279.292629032577` again. The metrics prove that the config is back to the team's choice.
- `git diff` prints nothing: `params.yaml` matches your real branch.
- Write down the MAE line for your pull request description.

**D5. Clean up.** Run `git switch week2-refactor`, then `git branch -D lr-fast lr-slow practice-base`. Now `git branch` lists `main` and `week2-refactor` only.

## Part E. Pull request, review and merge

**E1. Push your branch.** Run `git push -u origin week2-refactor`. Then open the **Actions** tab of your fork on GitHub. If GitHub asks you to enable workflows, enable them.

**E2. Open the pull request into your own `main`.**

1. On your fork on GitHub, select **Compare & pull request**.
2. Check the top line. **base repository** must be **your fork**, and **base** must be `main`. GitHub often selects the course repo. Change it. Never open this pull request against the course repo.
3. Title: `Week 2: fit, holdout scores, duplicate test`.
4. Description: one line for each TODO you filled. Then the MAE after the Part D fix, and that `git diff week2-refactor -- params.yaml` printed nothing.
5. Select **Create pull request**.

**E3. Wait for the green check.** The check **Diamond code checks** runs `make install`, `make lint` and `make test` on GitHub. It takes a few minutes. If it is red, open the failed step and read the first error. Run the same `make` target on your computer, fix, commit and push.

**E4. Get a review, and review a classmate.** Send your pull request link to your classmate. The reviewer opens **Files changed**, reads the diff, and checks 5 points:

1. Does it do what the pull request says? Read the diff, not the description.
2. Do tests cover the change, and is the check green?
3. Do config and code agree? No new hardcoded numbers.
4. No secrets, no `.env`, no model or data files.
5. Can I understand it? Clear names, small changes.

The reviewer leaves **at least 1 comment** on a line (select the `+` next to the line). Then the reviewer selects **Review changes**, **Comment**, and **Submit review**. A question is a good comment. "Looks good" alone is not enough. Do the same for your classmate's pull request.

**E5. Answer the review and merge.**

1. Reply to each comment. If a change is needed, commit it on `week2-refactor` and push. The check runs again.
2. When the check is green and each comment has a reply, select **Merge pull request**, then **Confirm merge**.
3. Select **Delete branch**. On your computer, run `git switch main`, `git pull` and `git branch -d week2-refactor`. The check on `main` is now green.

## What to submit

Submit the way your instructor asks, before the Week 3 session:

1. The link to your merged pull request.
2. The screenshot from Part C2: the silent `cmp` and `13 passed`.

## Done when

- [ ] `grep -rn "TODO M02" src tests` prints nothing.
- [ ] `make train` run twice gives identical `models/metrics.json`: `cmp` prints nothing.
- [ ] `make test` ends with `13 passed`, and `make lint` passes.
- [ ] The conflict is fixed with `learning_rate: 0.05`. The pull request description shows MAE `279.292629032577`.
- [ ] The check is green on the pull request.
- [ ] The pull request shows at least 1 review comment from a classmate, and your reply.
- [ ] The pull request is merged into your own `main`, and the branch is deleted.
- [ ] You left at least 1 review comment on a classmate's pull request.

## Rubric

Total: 100 points.

| Criterion | Full points | Part points | 0 points |
|---|---|---|---|
| 1. The 3 TODOs (30) | Fit on training rows, score on the holdout, test asserts the right count. MAE `279.292629032577` | 10 points for each correct block | No block correct, or the holdout is used for training |
| 2. Reproducibility proof (20) | Screenshot shows the silent `cmp` and `13 passed` | 10: only one of the two shown | Neither shown |
| 3. Merge conflict (15) | Description shows the MAE after the fix and the empty `params.yaml` diff | 8: conflict fixed, evidence incomplete | Not done |
| 4. Pull request (15) | Into your own `main`. Green check. Only the 3 files changed. Description has the B0 trace table | 8: merged, one of these missing | No pull request |
| 5. Review (20) | At least 1 useful comment received and answered. You left a useful comment on a classmate's pull request | 10: only one side done | No review |

- 80 to 100 points: complete.
- 50 to 79 points: partly complete.
- 49 points or less: not complete.

## Troubleshooting

| You see | Likely cause | Fix |
|---|---|---|
| `Makefile:<line>: *** missing separator.  Stop.` | A recipe line in the `Makefile` starts with spaces | Run `git restore Makefile`. Recipe lines start with a tab |
| `make: command not found` | `make` is not installed. A fresh Ubuntu 24.04 WSL has none | `sudo apt update`, then `sudo apt install -y make` |
| `python3.12: not found` during `make install` | Your Ubuntu is not 24.04. Plain `wsl --install` gives Ubuntu 26.04, which has no Python 3.12 | Repeat Week 0 Step 1 with `wsl --install -d Ubuntu-24.04` |
| `fatal: Not possible to fast-forward, aborting.` | Your `main` has commits that the starter does not have | Ask your instructor before you change `main` |
| The commit stops: `files were modified by this hook` | black or end-of-file-fixer fixed a file. The fix is not staged | Run `git status`, `git add` the file, commit again |
| `NotImplementedError: TODO M02 ...` still appears | The `raise` line is still there, or the file is not saved | Delete both TODO lines and save. Run `grep -rn "TODO M02" src tests` |
| `make test` shows `2 skipped` | No trained model yet. This is normal before `make train` | Run `make train`, then `make test` |
| `cmp` prints `differ: byte ...` | Something changed between runs: `params.yaml` was edited, or a package was added with `pip install` | Run `git diff params.yaml`. After a `pip install`, run `rm -rf .venv` and `make install` |
| `could not find expected ':'` when you commit | Conflict markers are still in `params.yaml` | Remove every `<<<<<<<`, `=======` and `>>>>>>>` line. Keep one value |
| The check is red, but `make lint` and `make test` pass on your computer | You did not push the last commit, or the workflow is in the wrong folder | Run `git status` and `git push`. The workflow must be `.github/workflows/checks.yml` at the repo root, one level above `diamond-mlops/` |
| No check appears on the pull request | Workflows are off in your fork | Open the **Actions** tab, enable workflows, and push a new commit |
| The pull request shows the course repo as base | GitHub chose the parent repo | Close it. Open a new one with **base repository** set to your fork |

## Resources

- **Required (20 minutes):** GitHub Docs, "Resolving a merge conflict using the command line": https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line (checked 2026-10-06).
- **Optional deeper reading:**
  - Pro Git, "Basic Branching and Merging": https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
  - GitHub Docs, "GitHub flow": https://docs.github.com/en/get-started/using-github/github-flow
  - pytest, "Good Integration Practices": https://docs.pytest.org/en/stable/explanation/goodpractices.html
  - pre-commit documentation: https://pre-commit.com/
  - Python Packaging User Guide, "src layout vs flat layout": https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/

## Before Week 3

- Take Quiz 2.
- Optional: in your fork, open **Settings**, then **Branches**, and add a rule for `main` that requires the check and 1 review. Branch protection is free on public repos. Private repos need a paid GitHub plan (checked 2026-10-06).
- Week 3 validates and versions the diamond data. It reads the same `params.yaml`.
