---
module: m01
title: "Quiz 1: Foundations of MLOps"
questions: 10
time: 15 minutes, open notes
grading: part of the 10% quizzes grade (one point per question)
source: modules/m01-foundations/content.md, approved blob a26932975cb0 (Daniel, Oct 6, PR #26)
---

# Quiz 1: Foundations of MLOps

Opens at the end of the Week 1 session. 10 questions, 15 minutes, open notes. Each question has one correct answer. Questions 7 and 8 use the diamond project and the Sparkle Exchange marketplace. Sparkle Exchange is a fictional company.

Use the course scale for maturity levels (Levels 0 to 4, as taught in Week 1).

---

## Questions

**1. Which sentence describes MLOps best?**

- A. The practice of deploying a trained model to a server.
- B. The engineering practice and team culture that joins building ML systems with running them, and works step by step toward automating and monitoring every stage.
- C. A set of tools (such as MLflow and Prefect) that a team installs to become "an MLOps team".
- D. The work that starts after a data scientist hands over a finished model.

**2. A team's prediction service has no bugs. The code has not changed in 3 months and all tests pass. Yet the model's error on new data keeps growing. What is the most likely cause?**

- A. A hidden bug that the unit tests do not cover.
- B. The service needs more servers.
- C. The team stopped using continuous integration.
- D. The world changed: the incoming data or the real price pattern moved away from what the model learned.

**3. The diamond model gets worse in production, and monitoring shows the cause is the newest model version. The old version was fine. Which lifecycle loop is the fastest fix?**

- A. Roll back: move the `champion` alias to the previous model version (back to Deploy). No retraining is needed.
- B. Retrain: send new data through Data validation first, then train again.
- C. Targets wrong: go back to Scope and rewrite the success criteria.
- D. Wait: do nothing until the next scheduled retrain.

**4. Match each stage of the course lifecycle to the question it answers.**

| Stage | Question |
|---|---|
| 1. Scope | (a) Is the service healthy, and is the model still right? |
| 2. Model | (b) Who uses the prediction, and what is "good"? |
| 3. Monitor | (c) Is this model better than the current one? |
| 4. Decide | (d) The model got worse. What now? |

Which row set is correct?

- A. 1-a, 2-b, 3-c, 4-d
- B. 1-b, 2-a, 3-d, 4-c
- C. 1-b, 2-c, 3-a, 4-d
- D. 1-c, 2-b, 3-d, 4-a

**5. On the course scale, what is true at Level 1 ("DevOps but no MLOps")?**

- A. The code is engineered (Git, unit tests, CI on every push). Training and hand-off of the model are still manual, and runs are not tracked.
- B. Training runs as a repeatable pipeline, and a registry says which model is live.
- C. Deployment goes through a CD pipeline with little or no human action.
- D. A monitoring alert triggers retraining and release.

**6. A team has these traits. Every training run is tracked. Data and models are versioned. Training is a repeatable pipeline. A registry says which model is live. An engineer still releases each new model by hand. Which level is this?**

- A. Level 1
- B. Level 2
- C. Level 3
- D. Level 4

**7. The diamond notebook (tag `m00`) trains a model with MAE 279.29 USD. Where does the project sit on the maturity model today, and why?**

- A. Level 2, because it uses a scikit-learn `Pipeline` that bundles preprocessing and the model.
- B. Level 1, because the code is in Git and the packages are pinned.
- C. Level 3, because the model is accurate enough to deploy.
- D. Level 0. It is one notebook run by hand: no unit tests of the model code, no tracked runs, no quality gate, no deployment, and nobody would notice if the model got worse.

**8. At Sparkle Exchange, a supplier renames the `cut` grade "Very Good" to "Very-Good" in a data feed. The price model's encoder breaks and nobody is warned. Which kind of ML technical debt is this, and which week pays it off?**

- A. Data dependency (an unstable input made by someone else). Week 3 pays it off with versioned data and a pandera schema that lists the allowed `cut` values.
- B. Glue code. Week 2 pays it off with `params.yaml`.
- C. Feedback loop. Week 12 pays it off with a retraining flow.
- D. Configuration debt. Week 9 pays it off with CI.

**9. At Sparkle Exchange, sellers usually accept the price the model suggests. The team plans to retrain next quarter on "sale prices" from the site. What is the risk?**

- A. Pipeline jungle: the data preparation has too many steps.
- B. Glue code: too much code moves data in and out of the ML package.
- C. Feedback loop: those sale prices are partly the model's own output, so the model learns from itself.
- D. There is no risk. More data always makes the model better.

**10. A data scientist builds a model in a notebook. An engineer rewrites the preparation steps for the API. Predictions from the API now differ from the notebook's for the same diamond. Which hand-off failed, and what does the course use to fix it?**

- A. Engineer to operations. The fix is a monitoring alert in Week 11.
- B. Data scientist to engineer (training-serving skew). The fix is one package used by both training and serving (Week 2).
- C. Data engineer to data scientist. The fix is a pricing analyst reviewing every prediction.
- D. Model to its consumers. The fix is an access-control rule in Week 10.
