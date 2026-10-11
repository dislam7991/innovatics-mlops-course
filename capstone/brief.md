---
item: P-07 (Capstone package)
title: "Capstone brief: End-to-End MLOps"
handed_out: Week 1
grading: 30% of the course grade. Rubric in capstone/rubric.md
source: CURRICULUM.md "Weeks 13 and 14. Capstone" and section 3 (2026-10-14)
---

# Capstone brief: End-to-End MLOps

## Goal

By Week 14 you own a working machine learning system. It is not a notebook. It is a project that another person can clone, run and trust.

Your system takes data in, checks it, trains a model, and records how the model was made. It serves predictions through an API in the cloud. It watches itself for problems. When something goes wrong, it stops the bad change or recovers from it.

On demo day you show it working. You also show it **failing safely**: a quality check stops something bad, and you recover.

**The evidence for the capstone:**
1. A reviewer runs your submission from a fresh clone with the commands in your README.
2. A live demo includes one failed quality check and one recovery action.
3. In a walkthrough, you explain your own code and make a small change on request.

## You already build most of it

Each week adds one part to the diamond project. The capstone joins those parts into one system and adds one feature of your own. You do not start from zero in Week 13.

| Required part | Tools | Week you learn it |
|---|---|---|
| 1. Validated and versioned data | pandera, DVC | 3 |
| 2. Tracked experiments and a registered `champion` | MLflow | 4 |
| 3. An orchestrated training pipeline | Prefect | 5 |
| 4. A tested API and a batch job | FastAPI, Pydantic | 6 |
| 5. A container | Docker | 7 |
| 6. CI with a quality gate, and CD | GitHub Actions | 9 |
| 7. Infrastructure in Terraform on AWS | Terraform, AWS Lambda, S3 | 10 |
| 8. Monitoring with a drift report and a dashboard | Evidently, Prometheus, Grafana | 11 |
| 9. A feedback loop with a champion vs challenger decision | MLflow, Prefect | 12 |
| 10. A rollback | MLflow aliases, CD | 12 |
| 11. `docs/architecture.md` with a diagram and a reason for each tool choice | Markdown, Mermaid | You write it yourself (see below) |

Kubernetes (Week 8) is optional in the capstone. It is a good choice for your own feature.

**Keep each week's practical working.** That is the best capstone plan. A student who finishes the 12 practicals has parts 1 to 10 ready to connect.

**Part 11 is not in any practical.** You create `docs/architecture.md` yourself. Start it from the lifecycle diagram in your Week 1 `docs/lifecycle.md`. Each week, add the new tool to the diagram and write one or two sentences on why you use it. Then the document is ready by Week 14.

## Choose a track

**Track A (the default): the diamond system, extended.** You use the diamond price data and your weekly work. You add **one feature of your own**. Examples:

- A shadow deployment: a second model gets the same requests, but its answers are only logged and compared
- A Feast feature store for the diamond features (Week 3 showed a demo)
- A Kubernetes deployment with a rolling update (Week 8)
- A small Streamlit front end that calls your API
- A cost dashboard for your AWS resources
- An idea of your own. Ask in your proposal

**Track B (approval needed): a dataset of your choice.** The rubric is the same. Your proposal must show 2 things:
1. You may legally use the dataset. Name its license or terms of use.
2. The model trains in under 5 minutes on your laptop.

Track B is more work. You rebuild every part for new data, new checks and a new model. Pick it only if your weekly practicals are on time. You still add one feature of your own.

## Timeline

| When | What you do | What you get back |
|---|---|---|
| Week 1 | Read this brief and the rubric. Ask questions | This brief |
| End of Week 5 | Submit the 1-page proposal (template below) | |
| Week 6 | Fix the scope if asked | Scope approved, or changes to make |
| Week 10 | 15-minute check-in, live or recorded | Feedback on progress and risks |
| Week 13 | Build week. Bring your questions to the live session | Office hours. The instructor runs the full answer key, including a failure and a recovery |
| Week 14, before the session | Your submission is frozen. A reviewer runs it from a fresh clone | |
| Week 14, in the session | Demo day: 10 minutes each | Your capstone grade |

## The proposal (end of Week 5)

One page. Save it as `docs/capstone-proposal.md` in your fork and submit the way your instructor asks. Use these 4 headings:

1. **Track.** A or B. For Track B: the dataset, its link, its license, its size, and your training time.
2. **Own feature.** What it does, why it is useful, and how you will show it in the demo. Two to four sentences.
3. **Architecture sketch.** A diagram of your system: the data, the training pipeline, the registry, the API, the cloud, and the monitoring. A Mermaid diagram or a photo of a drawing is fine.
4. **Risks.** The 3 things most likely to go wrong, and what you will do about each. Example: "Terraform is new to me. I will finish Practical 10 the same week."

The instructor approves the scope in Week 6, or asks for changes. A smaller system that works beats a bigger one that does not.

## The check-in (Week 10)

Fifteen minutes. Live, or a screen recording with notes. Bring:
- Your architecture diagram, updated
- Which required parts work now, and which do not
- Your own feature: what exists, what is left
- One question you want help with

The check-in is not graded. It is your best chance to fix a risk early.

## What to submit (Week 14)

1. **Your repository**, frozen with a Git tag named `capstone-submission` on the commit you want graded. Push the tag to your fork. The reviewer checks out that tag. Commits after the tag are not graded.
2. **`README.md`** that lets a stranger run your system. The required commands, in order, and what each one should show.
3. **`docs/architecture.md`**: one diagram of the whole system, and one or two sentences for each tool that say why you chose it.
4. **A demo plan**: the commands or script you will run on demo day, in order. It must include the failed quality check and the recovery.

Create the tag from the root of your fork, on your final commit:

```bash
git tag capstone-submission
git push origin capstone-submission
```

If you must fix something before the deadline, ask the instructor before you move the tag.

## Demo day (Week 14)

**Before the session.** The instructor, or a classmate, runs your submission from a fresh clone, using only your README. Write it for that person.

**In the session. 10 minutes each:**
- **6 minutes, demo.** Show the system working end to end. Then show **one failed quality check** (for example, CI blocks a worse model, or validation stops bad data). Then show **one recovery action**: a rollback to the previous `champion`. Also show the champion vs challenger decision your feedback loop recorded. The rubric needs both for full Monitoring and recovery points.
- **4 minutes, questions.** Answer trade-off questions about your design. Make **one small change on request**, for example a new threshold or a new log line, and run it.

Practise the demo with a timer. Have the cloud resources running before your turn. If the live system fails, show the recorded backup and explain what failed. That still earns points for explanation.

## Rules

**AI tools.** You may use AI tools. You are responsible for every line you submit. In the walkthrough you explain your code and change it. If you cannot explain a part, it does not earn points.

**AWS and cost.** Use your own AWS account and IAM user from Week 0. Keep the budget alert from Week 0 on. Run `terraform destroy` when you finish a work session, and again after demo day. Never put secrets, access keys or `.env` files in Git.

**Your own work.** You may discuss ideas with classmates. Your code, your documents and your demo are your own. Name any code you adapted from another source in `docs/architecture.md`.

## Common mistakes

| Mistake | What to do instead |
|---|---|
| Starting the capstone in Week 13 | Keep every weekly practical working. Connect the parts as you go |
| A README that works only on your laptop | Ask a classmate to run it from a fresh clone before Week 14 |
| A big own feature that is not done | Pick a small feature. Make it work. Explain it well |
| No failure in the demo | Plan the failed check and the recovery first. The rubric's largest area depends on them |
| Cloud resources left running | `terraform destroy` after each session. Check the AWS console |

## How you are graded

See `capstone/rubric.md`. The 7 areas add up to 100 points. Monitoring and recovery carry the most points (20), because a production system must find and fix its own problems.
