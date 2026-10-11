---
module: m02
title: "Quiz 2: Reproducible Projects, Git and Code Quality"
questions: 10
time: 15 minutes, open notes
grading: part of the 10% quizzes grade (one point per question)
source: modules/m02-reproducible-projects/content.md (M02-PACKAGE draft, 2026-10-08, not yet approved)
---

# Quiz 2: Reproducible Projects, Git and Code Quality

Opens at the end of the Week 2 session. 10 questions, 15 minutes, open notes. Questions 5 and 7 are short written answers. All other questions have one correct answer. Every question uses the diamond project at tag `m02`.

---

## Questions

**1. Which four inputs must stay the same for a training run to give the same result?**

- A. Code, data, config and environment.
- B. Code, data, seed and GPU.
- C. Notebook, CSV file, Python version and laptop.
- D. Code, model file, `metrics.json` and Git history.

**2. In the diamond notebook, the section 2 cell removes duplicates and zero-dimension rows, and the section 4 cell splits the data. A student restarts the kernel and runs only the imports cell, the section 1 cell (load) and the section 4 cell. The holdout now has 10,788 rows instead of 10,755. Why?**

- A. The seed changes every time the kernel restarts.
- B. The cleaning cell never ran, so the split used uncleaned data. Same code, different data in the split.
- C. The split cell uses a different `test_size` when it runs alone.
- D. JupyterLab caches an old copy of the CSV file.

**3. Which value belongs in `params.yaml`, and which belongs in `src/diamond/config.py`?**

- A. Both `learning_rate` and the quality order of `cut` go in `params.yaml`, so all values live in one file.
- B. `learning_rate` goes in `config.py`. The quality order of `cut` goes in `params.yaml`.
- C. `learning_rate` goes in `params.yaml`, because it is an experiment choice. The quality order of `cut` goes in `config.py`, because it is a fact about the data.
- D. Neither. Both stay hardcoded in `train.py` next to the code that uses them.

**4. You pushed a commit to `main` yesterday. Your teammates already pulled it. Today you find it breaks the tests. Which command undoes it safely?**

- A. `git reset --hard HEAD~1`
- B. `git restore --source=HEAD~1 -- .`
- C. `git revert --no-edit <commit>`
- D. `git switch -c undo-commit`

**5. (Short answer) Read this `.gitignore`. After `git add .`, the file `models/model.bin` stays out of Git, but `export/model.bin` gets committed. Which line does nothing for `.bin` files, and what should it be?**

```
.venv/
.env
models/
.bin
```

**6. The diamond team deploys small changes several times a week. Which branching strategy does the course use, and why?**

- A. Git Flow, because long-lived `develop` and `release` branches are best for any team that runs CI.
- B. GitHub Flow: `main` always works, and each change goes through a short branch, a pull request, checks and a review.
- C. Trunk-based development, because it only works for small teams.
- D. No branches. Everyone pushes to `main`, so review is not needed.

**7. (Short answer) You run `git merge lr-slow` and Git stops. `params.yaml` now contains the block below. The team decided to keep `learning_rate: 0.05`. Write the final text of these lines, and the two Git commands that finish the merge.**

```
<<<<<<< HEAD
    learning_rate: 0.1
=======
    learning_rate: 0.03
>>>>>>> lr-slow
```

**8. You add `import os` to `src/diamond/preprocess.py` and never use it. `make lint` fails with `F401 [*] 'os' imported but unused`. Which statement is correct?**

- A. black reported it, because black finds unused imports.
- B. ruff, the linter, reported it. `make lint` only checks. `make format` runs `ruff check --fix` and removes the line.
- C. `make lint` changed the file, so you only need to commit again.
- D. It is a style issue only, so the commit is safe to push.

**9. You run `git commit`. The black hook reformats one of your files, and no commit is created. What should you do?**

- A. Run `git commit --no-verify`. CI never runs the same checks, so skipping is safe.
- B. Run `make hooks` again, because the hooks are broken.
- C. Run `git reset --hard` and write the change again.
- D. Read the change with `git status` and `git diff`, `git add` the fixed file, and commit again.

**10. Which test does not belong in the Week 2 fast test suite?**

- A. `clean()` on a tiny hand-made DataFrame drops a zero-dimension row.
- B. The preprocessor outputs 9 columns, and an unknown `cut` value fails.
- C. A test that trains on the full CSV and asserts the model MAE is below 300 USD.
- D. `params.yaml` names a model the code can build, with valid hyperparameters.
