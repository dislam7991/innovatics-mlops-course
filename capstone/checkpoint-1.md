---
item: P-07 (Capstone package)
title: "Checkpoint 1: Reproducible, automated training"
due: end of Week 5
covers: Weeks 2 to 5
solution_tag: m05
grading: 10% of the course grade (the 2 checkpoints are 20% together)
source: CURRICULUM.md section 3 and "Checkpoint 1" in Week 5 (2026-10-14); diamond-mlops/README.md and Makefile at tag m05
---

# Checkpoint 1: Reproducible, automated training

## Goal

Weeks 2 to 5 turned a notebook into a training system. Checkpoint 1 asks one question: **can someone else run it, and can they trust what it produces?**

You submit your diamond project as it stands after Week 5. A reviewer clones it and runs your Prefect flow. The flow validates the data, trains, evaluates, and registers the model only if it is better. Then, in a short live walkthrough, you explain how it works and make a small change.

There is no new dataset and no new tool. This checkpoint checks that the Week 2 to 5 parts work **together** from a fresh clone.

## What the reviewer must see

| # | The reviewer sees | Week |
|---|---|---|
| 1 | A fresh clone installs, gets the data, and runs the flow end to end: `validate_data`, `train_model`, `evaluate_model`, `register_if_better` | 2, 3, 5 |
| 2 | Bad data is rejected before training. The flow fails at `validate_data`, and no model is trained | 3, 5 |
| 3 | Every MLflow run traces back to its data version, code commit and params. At `m05` these are the tags `data_md5`, `git_commit` and `git_dirty`, and the logged params | 4 |
| 4 | `champion` moves only when the new model is better. An equal or worse model leaves it where it is | 4, 5 |
| 5 | A forced failure on the first attempt is retried, and the flow then succeeds | 5 |

These commands come from `diamond-mlops/Makefile` at tag `m05`. Your project must still support them, or your README must name the commands that replace them:

| Command | What it does |
|---|---|
| `make install` | Creates `.venv` and installs the hash-locked requirements |
| `make prefect` | Starts the local Prefect server. Keep it running in its own terminal |
| `make flow` | Runs the training flow once |
| `make flow-retry` | Runs the flow with a failure on the first attempt of `validate_data` |
| `make serve` | Serves the flow on a 10-minute schedule. Keep it running in its own terminal |
| `make mlflow` | Starts the MLflow UI at `http://127.0.0.1:5000` |
| `make test` | Runs the tests |

## What to submit

Submit the way your instructor asks, before the end of Week 5:

1. **A Git tag named `checkpoint-1`** on the commit you want graded, pushed to your fork. Commits after the tag are not graded.
2. **A README section "Checkpoint 1: run it from a fresh clone".** The commands in order, from `git clone` to a finished flow run. Include how a fresh clone gets the data. Say which terminal each long-running command needs.
3. **A bad-data test the reviewer can repeat.** Commands that make `data/raw/diamonds.csv` bad, run the flow, and put the data back. Example: set one `price` to a negative number, run `make flow`, then restore the file with `.venv/bin/dvc checkout --force data/raw/diamonds.csv`. Without `--force`, DVC refuses to overwrite a changed file. Write what the reviewer should see. At `m05`, `validate_data` has 2 retries, so the bad data fails 3 attempts, then the flow fails.
4. **4 screenshots**: (a) the Prefect UI with a completed run and its 4 tasks; (b) the flow log with the failed first attempt and the retry; (c) the MLflow run page of your current `champion`, with its tags; (d) the MLflow runs table for all your runs, with these columns shown: the params `seed`, `test_size` and `model.name`, and the tags `git_commit`, `git_dirty` and `data_md5`.

Create the tag from the root of your fork, on your final commit:

```bash
git tag checkpoint-1
git push origin checkpoint-1
```

## The live walkthrough (5 to 10 minutes)

In the Week 6 session, or at a time your instructor gives you:
- Show one flow run in the Prefect UI. Say what each task does and what happens if it fails.
- Open the MLflow run of your `champion`. Show how you know which data, code and params made it.
- Answer one question about a design choice. Example: "Why does `register_if_better` compare RMSE, and not only MAE?"
- Make one small change on request, and run it. Example: change the retry count, or change a validation rule.

The AI-use policy applies. You may use AI tools. You must explain and change your own code.

## Rubric

Total: 100 points. The weights come from CURRICULUM.md.

| Criterion | Full points | Part points | 0 points |
|---|---|---|---|
| 1. Fresh clone runs the flow end to end (25) | The reviewer follows your README from `git clone` to a completed flow run with the 4 tasks. No fixes needed | 13: it runs, but the reviewer had to fix or guess a step | It does not run |
| 2. Bad data rejected (15) | Your bad-data test makes the flow fail at `validate_data`. No model is trained. The message names the problem | 8: validation fails, but training still starts, or the message is unclear | Bad data is trained on |
| 3. Every run traceable (20) | Every training run in the reviewer's fresh-clone MLflow store, and every run in screenshot (d), has the params, `git_commit`, `git_dirty` and `data_md5`. The `champion` run has `git_dirty` `false`, and its tags match the tagged commit and the DVC pointer | 10: one or more runs miss a tag or param, or the `champion` tags do not match | No tracking |
| 4. `champion` replaced only by a better model (15) | Screenshot or demo of a run that did not replace `champion`, and the reason in the log | 8: the gate exists, but no run shows it working | `champion` moves on every run |
| 5. Forced failure retries (10) | Screenshot (b): the first attempt fails, the retry succeeds, and the flow completes | 5: the failure shows, but the retry does not | No retry |
| 6. Live walkthrough (15) | Clear explanation. Good answer to the design question. The small change works | 8: clear explanation, but the change does not work | No walkthrough, or you cannot explain your code |

## Common problems

| Problem | Likely cause | Fix |
|---|---|---|
| A fresh clone has no `data/raw/diamonds.csv` | A local DVC remote is not part of a clone | Put the data step from Week 3 in your README |
| `make flow` cannot reach the server | `make prefect` is not running | Start it in a separate terminal first |
| Two runs at once change the same files | `make serve` is still running while you train by hand | Stop the serve process before manual training |
| `git_dirty` is `true` on your champion | You trained with uncommitted changes | Commit, then run the flow again |
| The reviewer gets different metrics | Changed `params.yaml` or data that is not committed | Commit `params.yaml`, `dvc.lock` and the `.dvc` pointer |
