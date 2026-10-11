---
item: P-07 (Capstone package)
title: "Capstone rubric"
grading: 100 points. The capstone is 30% of the course grade
source: CURRICULUM.md "Capstone rubric (100 points)" (2026-10-14). Area names and points are copied from it. The part-point levels are new in this file
---

# Capstone rubric

Total: 100 points. The capstone is 30% of the course grade.

The reviewer grades the commit at your `capstone-submission` tag, and your demo and walkthrough on demo day. The brief is in `capstone/brief.md`.

**How points work.** Each area has 3 levels: full, part, and 0. The reviewer can give any number between the levels when the work sits between them. A required part (brief, "You already build most of it") that is missing loses points in the area that lists it below.

## The 7 areas

| Area | Points | Full marks when | Part marks | 0 points |
|---|---|---|---|---|
| 1. Reproducibility | 15 | A fresh clone and the README commands rebuild the model and the metrics. Dependencies are pinned | 8: it runs, but the reviewer had to fix a step or guess a missing one | It does not run from a fresh clone |
| 2. Data quality and traceability | 15 | Validation stops bad data before training. The deployed model is the registered version that the `champion` alias points to. That version traces to its MLflow run, data version, code commit and params | 8: validation works, or tracing works, but not both; or the deployed model is not the registered `champion` | Neither |
| 3. Automation and delivery | 15 | The pipeline runs on a schedule or a trigger. The API and the batch job work and have tests. They run from a Docker container. CI blocks bad code and a worse model. CD deploys that container to AWS on infrastructure that Terraform built | 8: the API and the container work, and 2 of pipeline, CI and CD work | No working API or container, or only 1 of pipeline, CI and CD works |
| 4. Monitoring and recovery | 20 | The dashboard and the drift report work. Live error is measured. The feedback loop trains a challenger and records the champion vs challenger decision. The demo shows a failed quality check and a rollback to the previous `champion` | 10: monitoring works, but the demo misses the feedback decision or the rollback | No monitoring and no recovery |
| 5. Own feature | 10 | It works in the demo, and you explain why it is useful | 5: it works only in part, or you cannot explain it | Missing |
| 6. Documentation | 10 | The README and `docs/architecture.md` let a stranger run and understand the system. The diagram matches the code. Each tool has a reason | 5: one of the two documents is weak or out of date | Neither document |
| 7. Explanation and walkthrough | 15 | Clear demo in time. Good answers to trade-off questions. The small change on request works | 8: clear demo, but weak answers or the change does not work | No walkthrough, or you cannot explain your own code |

## Which required part counts where

| Required part | Area |
|---|---|
| Validated and versioned data (pandera, DVC) | 2 |
| Tracked experiments and a registered `champion` (MLflow) | 2 |
| Orchestrated training pipeline (Prefect) | 3 |
| Tested API and a batch job (FastAPI) | 1 and 3 |
| Container (Docker) | 3 |
| CI with a quality gate, and CD (GitHub Actions) | 3 |
| Infrastructure in Terraform on AWS | 3 |
| Monitoring with a drift report and a dashboard | 4 |
| Feedback loop with a champion vs challenger decision | 4 |
| Rollback | 4 |
| `docs/architecture.md` | 6 |

## Notes for the reviewer

- Run the submission from a fresh clone **before** demo day. Use only the README. Write down each step you had to fix. That list decides area 1.
- Check out the `capstone-submission` tag, not the branch.
- The AI-use policy applies. If the student cannot explain a part in the walkthrough, that part earns no points in its area.
- If the live system fails on demo day, the student may show a recorded backup. Grade areas 1 to 6 from the fresh-clone run and the recording. Grade area 7 from the explanation.
- Track B uses the same rubric. "Model and metrics" in area 1 means the student's own model and metrics.
- At about 15 minutes per student, 20 students take about 5 hours per round (CURRICULUM, "Daniel's prep").
