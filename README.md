# InnovatiCS MLOps Specialization Bootcamp: course repository

This is the student repository for the bootcamp *From Notebooks to Production*. It holds the weekly materials and the starter code of the one project you build all course long: **Diamond Price Prediction**. Your instructor adds a week when it is ready. This branch holds the materials up to Week 02. Later weeks are on their own `start-mXX` branches.

## What is here

| Folder or file | What it holds |
|---|---|
| `diamond-mlops/` | The diamond project, at the starter state of the current week. Every practical works in this folder |
| `weeks/w00/` to `weeks/w02/` | One folder per week: `practical.md` (what you do and hand in), `content.md` (the reading), `quiz.md` (the questions), the slides as a PDF, and the images the texts use |
| `capstone/` | The capstone brief, the rubric and the two checkpoint briefs. Handed out in Week 1 |
| `.github/workflows/` | The GitHub Actions checks the practicals use. They run in your fork for free, because your fork is public |

Each week, `diamond-mlops/` holds the solution of the week before plus a few `TODO` stubs for the new week. You fill the stubs. The practical says exactly which ones.

## Branches and tags

| Name | What it is |
|---|---|
| `main` | The Week 0 starter, where every fork begins. Your fork's `main` is yours: Week 2 fast-forwards it, later weeks branch from `upstream/start-mXX` |
| `start-mXX` | The starter of Week XX. For example `start-m02` is the Week 2 starter. A starter never changes after it is published |
| `mXX` | The solution of Week XX. The instructor publishes it after the practical deadline |

## One-time setup (Week 0)

1. Sign in to GitHub and select **Fork** on this page. Keep the fork **public**: public forks get free Actions minutes and free branch protection.
2. Clone your fork, not this repository:

   ```bash
   cd ~
   git clone git@github.com:<your-user>/innovatics-mlops-course.git
   cd innovatics-mlops-course
   ```

   Your fork's `main` is the Week 0 starter, so you stay on it. A fork copies only `main`; the other weeks come from `upstream` (step 3).

3. Add this repository as `upstream`, so you can pull new weeks:

   ```bash
   git remote add upstream https://github.com/dislam7991/innovatics-mlops-course.git
   git remote -v
   ```

   `origin` is your fork. You push only to `origin`. `upstream` is this repository. You only fetch from it.

4. Follow `weeks/w00/practical.md`. It ends with `bash scripts/verify_setup.sh`.

## Every week

Each practical starts with a **Part A** that gets the week's starter. The commands are in the practical. The pattern is:

```bash
git fetch upstream
git switch -c week3-data upstream/start-m03   # the branch name and week change
```

Week 2 is the exception: it fast-forwards your `main` to `upstream/start-m02`, so your `main` and the course starter share one history. Every other week lives on its own branch made from `upstream/start-mXX`.

Rules that keep you out of trouble:

- Commit your work before you fetch a new week.
- Never open a pull request against this repository. Open pull requests in your own fork, from your week branch to your `main`. Practical 2 shows how to set the base repository.
- Run every command inside Linux (Ubuntu in WSL2 on Windows) and inside `diamond-mlops/`, unless the practical says otherwise.

## Questions

Ask in the course channel, or bring the error message to the live session. Say which week, which step, and paste the full command and its output.
