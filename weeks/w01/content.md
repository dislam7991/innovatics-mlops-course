# M01 content: Foundations of MLOps (Week 1)

Topic-based teaching content for Week 1. This file is the source for the Week 1 deck, practical, quiz and instructor notes. Those are built only after Daniel approves this file (gate G5).

| Field | Value |
|---|---|
| Work item | M01-CONTENT (Week 1 content file) |
| Author | Claude, 2026-10-05 |
| Reviewer | Codex (G4), then Daniel (G5) |
| Scope authority | `CURRICULUM.md` Week 1 (Big question, 4 objectives, Concepts list, Practical 1, Quiz 1) |
| Evidence used | `modules/m01-foundations/source-map.md` (blob fb7ed973ca50), `evidence/notes.md` (blob 30397c94384c), `evidence/videos.md` (blob e02684246b42), all at main b22832b. Psitron page checks: `docs/sources/psitron-visual-check.md` (blob 5a59f564495b) |
| Code checkpoints | Tag `m00` = 58d83c0 (notebook). Tag `m01` = 7596237 (`docs/problem-framing.md`, `docs/lifecycle.md`). Tag `m02` = e057569 (named only as a preview) |
| Research gate | G3 passed: Codex round 2 on PR #22 at c50d816, comment 5993511662 |

## How to read this file

- Topics follow the teaching order of the Week 1 session plan. They are not slides.
- Each topic has the same 7 parts: objective, explanation, diamond example, limits and common mistakes, diagram spec, demo and practical link, sources.
- Every claim carries one of these labels:
  - **[source]** explained by a named source the evidence files record as read-full, visual-checked or doc-verified.
  - **[synthesis]** our own combination of named sources.
  - **[decision]** a course design choice, with the reason.
  - **[fictional]** an invented teaching example. Sparkle Exchange (the diamond marketplace) is fictional.
  - **[measured]** a number produced by running code, with the command and revision.
- Source labels in the "Sources" lines repeat the reading status from the evidence files. Psitron text pages are `read-full` in the P-10 catalog (text extract). Psitron PDF pages are `visual-checked` in `psitron-visual-check.md`. Transcripts are `transcript-reviewed: read-full` in `evidence/videos.md`.
- Slides carry InnovatiCS branding and no source credits. The citations here are internal.

**The diamond numbers used in this file** [measured]: HistGradientBoosting, seed 42, 10,755 holdout rows: MAE 279.29 USD, RMSE 524.92 USD, R2 0.9826. Reproduced from a clean install for P-02 (Oct 3, MAE 279.292629032577) and M00-CODE (PR #8, merged at 534b82c, now tag `archive/m00-py311`). Re-measured on Python 3.12.3 after the switch (2026-10-11, clean `m00`, MAE 279.292629032577). AGENTS.md section 10 holds the full-precision values.

---

## Topic 1. The production gap: a working notebook is a small part of a working system

**Objective.** Students can explain why a model that works in a notebook is still far from a model people can rely on, and can name what is missing around it. (Supports the Big question and objective 1.)

**Explanation.**
- A notebook answers one question: "Can a model predict this well on my data today?" A production system must answer more questions, every day: Which data trained this model? Can I retrain it the same way? How do other programs get a prediction? Who notices when it gets worse? [synthesis: notebook cells 0 and 27; Sculley et al. Figure 1]
- Sculley et al. (Google, 2015) drew this as one small "ML Code" box inside much larger boxes: configuration, data collection, feature extraction, data verification, machine resource management, analysis tools, process management tools, serving infrastructure and monitoring. Their point: only a small part of a real ML system is the learning code. [source: Sculley p. 4, Figure 1]
- The paper's only number is a hedge. A mature system "might" end up at most 5% ML code and at least 95% glue code (p. 5). It is an estimate. Do not present it as a measured statistic. [source: Sculley p. 5]
- What goes wrong after go-live, in the order the diamond project will meet it:
  1. **Data quality.** Models need large amounts of good data. Bad rows reach the model unless something checks them. [source: Psitron M01 p14]
  2. **Deployment and maintenance.** Getting a model to serve predictions needs planning and keeps costing effort after release. [source: Psitron M01 p14]
  3. **The world changes.** Accuracy falls when the data or the business changes. This is hard to see because nothing crashes. [source: Psitron M01 p14; Day 1 2:22:19 to 2:26:00]
  4. **Scale shows up late.** A model that works on the in-house test set can break with real traffic: new data patterns, more volume, more load. [source: Psitron M01 p17 to p18; Day 1 2:35:37 to 2:36:13]
  5. **Retraining at scale.** Someone must retrain, check and redeploy, again and again. [source: Psitron M01 p17]
- The story to tell (spoken by the Psitron instructor, no named source, so tell it as a scenario): a team built a ticket-sales forecaster for theatres in 2020. Theatres closed, streaming took over, some viewers never came back. The data scientist deployed it by hand and expected it to last three years. It failed within a couple of months. Monitoring would have shown the drift. A repeatable pipeline would have made the retrain cheap. [fictional/illustrative: Day 1 2:22:19 to 2:26:00 and 2:49:55 to 2:51:48]
- The Zoomcamp maturity video gives the hand-off risk in one line: at the lowest level, engineers re-implement the data scientist's notebook, which "sometimes ends up in a total disaster". Paraphrase it; the transcript is AI-cleaned, so do not quote it as speech. [source: Zoomcamp 1.5 P2, limits in videos.md]

**Diamond example.**
- The diamond notebook at tag `m00` trains a good model: MAE 279.29 USD on 10,755 holdout rows, R2 0.9826. [measured]
- Its own last cell lists what it is missing: it is monolithic and stateful (cells depend on run order), paths and parameters are hardcoded, it has no tests, and it cannot be reproduced with one command. In this course the Week 0 runner (`scripts/run_notebook.py`) re-runs the notebook and checks the model type, seed, holdout rows and metrics, so teach the gap precisely: no unit tests of the model code, and no reusable training step outside the notebook; the runner is an end-to-end regression check. [source: `notebooks/01_diamond_exploration.ipynb` cell 27, tag `m00`]
- Its first cell says it stops at the hand-off point, on purpose: "Operations do not belong in a notebook." [source: cell 0]
- Cell 24 makes the course's point in the notebook's own words: the lesson is making this result reproducible, testable and deployable; squeezing out more accuracy is not the goal. [source: cell 24]
- So Week 1's "before" picture: one strong model, zero of the boxes around it. Each later week fills one box.

**Limits and common mistakes.**
- Use one statistic: the often-quoted figure that about 87% of ML projects never reach production ("80 to 90%" is also fine). It dates from 2019 and is an industry estimate, not the result of a published study, so present it as a widely reported estimate and give the year. Do not use the Psitron numbers (53% of proofs of concept reach production, 9 months on average, "75% by end of 2024"): they come from a 2023 conference talk and an expired forecast. Let the notebook make the rest of the point. [decision: Daniel, M01-CHECK, 2026-10-19; earlier analysis in source-map section 1 and videos.md section 2.1]
- Do not say "the model is unimportant". The model is the reason the system exists. The point is that it is small next to everything needed to run it.
- Psitron M01 p16 ("may back propagate to the original state") is unclear even with the spoken explanation. Skip it. [decision: videos.md 2.1]

**Diagram spec: "The model is a small box".**
- Meaning: the trained model is a small part of a production ML system.
- Elements: a small dark box "Model: `train` + HistGradientBoosting" in the centre. Around it, larger empty boxes, each labelled with the week that builds it: Config and code structure (W2), Data validation and versioning (W3), Experiment tracking and registry (W4), Pipeline and scheduling (W5), Serving API and batch (W6), Container: build (W7) and run (W8), CI/CD (W9), Cloud resources (W10), Monitoring (W11), Retraining and rollback (W12).
- Relationships: no arrows. The size difference is the message.
- Source and adaptation: idea after Sculley et al. 2015 Figure 1 (9 boxes listed above). Our labels are course weeks, so it is an original drawing. Do not copy Google's adapted version (it adds "automation", "testing and debugging" and "metadata"). Use the box names only as listed here.

**Demo and practical link.**
- Demo: open the notebook at `m00`, scroll to cell 27, read the 4 bullets aloud, then ask "Which of these would hurt first if 50 sellers used this every day?"
- Practical 1 Part B question 4 asks where diamond sits today. This topic gives the answer: Level 0 (Topic 6).

**Expected outcome.** Students name at least 3 missing boxes (tests, data and model versioning, serving, monitoring) and agree the notebook is Level 0.

**If it goes wrong.** If the notebook will not open, show cells 0, 24 and 27 from the GitHub file view at tag `m00`; they are text cells, so no kernel or outputs are needed. If students say "it works, so it is ready", ask who would notice if prices moved next month.

**Sources.** Sculley et al. 2015 (read-full pp. 1 to 9; Figure 1 visual-checked; notes.md M01-R1). Psitron M01 p13, p14, p16 to p18 (read-full text; p13 visual-checked; p14 and p16 to p18 are text-only pages per the visual check). Psitron Day 1 1:43:08 to 2:56:08 (transcript read-full). Zoomcamp 1.5 P2 (AI-cleaned transcript, read-full, paraphrase only). Diamond notebook cells 0, 24, 27 at `m00` (read-full this run).

---

## Topic 2. What MLOps is, and why it starts before deployment

**Objective.** Students can define MLOps in one sentence and explain why it covers data collection, validation and evaluation, before any deployment. (Objective 1.)

**Explanation.**
- Definition for the course (our rewrite of Google Cloud's): **MLOps is the engineering practice and team culture that joins building ML systems with running them, and works step by step toward automating and monitoring every stage of the lifecycle.** A team does MLOps long before everything is automated; the maturity levels in Topic 6 describe how far it has got. [source: Google Cloud MLOps page, intro, read-full, last reviewed 2024-08-28]
- Google says MLOps advocates automation and monitoring at all steps of building an ML system, and lists them as integration, testing, releasing, deployment and infrastructure management. Its 8 data science steps start at data extraction and include evaluation on a holdout set and model validation (does it beat a baseline, is it fit to deploy) before serving. So MLOps work starts well before deployment. [source: Google, "Data science steps for ML"]
- The older Psitron definition (p12) says MLOps is collaboration between data scientists and operations, and that it "automates the deployment" of models. That is too narrow: it leaves out data and evaluation. The Psitron instructor also widens the people list himself: data engineers, ML engineers and MLOps engineers belong in it too. [source: Psitron M01 p12; Day 1 2:18:13 to 2:20:03]
- MLOps sits where three fields meet: machine learning, data engineering and DevOps. The model needs ML skills. The data needs pipelines and checks. Releasing and running it needs DevOps. [source: Psitron M01 p20, visual-checked]
- Three things MLOps versions that plain software does not: data, models, and the code that trains them. Code versioning carries over from DevOps. [source: Psitron M01 p22; Day 1 2:51:48 to 2:55:03]
- A good student question from the Psitron session: "Why not put the data in GitHub too?" Git is made for text files that change line by line. A 1 to 2 GB data file does not fit that model, so data gets its own tool (DVC, Week 3). [source: Day 1 2:51:48 to 2:55:03; Day 6 2:44:22 onward]

**Diamond example.**
- Three of the 8 risks in `problem-framing.md` happen before any deployment: bad input data, training data that changes without a record, and results that cannot be reproduced. MLOps handles all three in Weeks 0 to 3, long before the API in Week 6. [source: `docs/problem-framing.md` section 3, tag `m01`]
- The notebook's sanity check is an MLOps habit inside a data scientist's file: an R2 above about 0.95 is a red flag until checked for leakage and overfitting. The notebook checks holdout isolation, target-free features, train/test overlap, and the CV-vs-holdout gap. [source: cells 22 to 24, tag `m00`]

**Limits and common mistakes.**
- Mistake: "MLOps = deploying models." Deployment is one stage. Validation and evaluation come first, and monitoring and retraining come after.
- Mistake: "MLOps = a tool." No tool makes a team "do MLOps". The practices and the team habits come first; tools support them.
- The course starts from an existing model for convenience. Say this out loud in Week 1 so students do not conclude that MLOps begins after the model. [source: CURRICULUM Week 1 Concepts]

**Diagram spec: "Where MLOps sits".**
- Meaning: MLOps needs three skill areas at once.
- Elements: three overlapping circles labelled Machine learning, Data engineering, DevOps. The centre overlap is labelled MLOps.
- Source and adaptation: idea from Psitron M01 p20 (left Venn, visual-checked). Redraw in our style. Skip the second Venn on that page (people, process, technology); it is generic.

**Demo and practical link.**
- Ask students to point at the cells in the notebook that are already "MLOps-ish" (cells 22 to 24, the sanity checks) and the parts that are missing (no record of data version, no unit tests).

**Expected outcome.** Students point to cells 22 to 24 as checks that already exist, and name two things missing (no record of the data version, no unit tests).

**If it goes wrong.** If students call every exploration cell "MLOps", narrow it: MLOps is what makes a result trustworthy and repeatable. A chart that is only looked at once does not count.

**Sources.** Google Cloud MLOps page (read-full raw HTML, checked 2026-10-05; notes.md M01-R2b and R6a). Psitron M01 p12, p20, p22 (read-full text; p20 and p22 visual-checked). Psitron Day 1 (transcript read-full). Supporting only: Kreuzberger et al. 2023, Section 6 definition (read-part; it agrees that MLOps covers the end-to-end lifecycle; no claim here rests on it alone).

---

## Topic 3. DevOps, DataOps and MLOps

**Objective.** Students can say what each practice protects and how each notices a problem. (Objective 1.)

**Explanation.**
- **DevOps** gives shorter development cycles and dependable releases through continuous integration (CI: every change is built and tested automatically) and continuous delivery (CD: every tested change can be released automatically). Its loop: plan, code, build, test, deploy, operate, monitor, improve. [source: Google "DevOps versus MLOps"; Psitron M01 p28, visual-checked; Day 3 15:00 to 21:40]
- **DataOps** applies DevOps and lean ideas to data pipelines, so analytics data arrives on time, is tested and versioned, and its quality is watched continuously. Its manifesto says "analytics is code", version everything, orchestrate pipelines, treat pipelines like lean production lines, and check data quality automatically. It treats delivery as a team sport, shared across roles. [source: DataOps Manifesto, read-full, checked 2026-10-05]
- **MLOps** keeps everything from DevOps and adds what ML needs. Google lists five differences: [source: Google "DevOps versus MLOps"]
  1. Team skills: data scientists are often not software engineers.
  2. Development is experimental: many runs, most thrown away.
  3. Testing covers data, schemas and model quality, on top of unit and integration tests.
  4. Deployment often means shipping a training pipeline that produces models, and that pipeline then ships the prediction service.
  5. Production models decay as data changes, even when the code has no bug.
- From these, Google names three practices: CI also tests data and models; CD ships a pipeline; **CT (continuous training)** is new and unique to ML. Google also says to track summary statistics of live data and model performance so you can alert or roll back. [source: Google]
- The one-line contrast for students: **a model can go wrong with no bug at all.** Software bugs can be loud (a crash, a failed test) or quiet (a wrong calculation that still returns a plausible number). A model adds a third kind of failure: the code is correct and runs fine, but the world changed, so the predictions slowly get worse. No error is raised. Only measuring predictions against reality shows it. [synthesis: Google point 5; problem-framing risk table]

| | DevOps | DataOps | MLOps |
|---|---|---|---|
| Main product | Application code | Analytics data and reports | Models and the pipelines that make them |
| What gets versioned | Code, config | Code, config, data, environments | Code, config, data, models |
| Typical failure | A bug, a failed build, a crash | Late, missing or wrong data | Accuracy falls as the world changes; train and serve disagree |
| How you notice | Tests fail, errors, alerts | Data tests, pipeline monitoring | Data checks, drift reports, live error vs actual outcomes |

[synthesis: Google; DataOps Manifesto; Psitron M01 p22]

- Zoomcamp's cleanest contrast: a team with unit and integration tests, CI/CD and request metrics, but no experiment tracking and no way to reproduce the model, has DevOps and is "not ML-aware". That is Level 1 in Topic 6. [source: Zoomcamp 1.5 P3, paraphrase only]

**Other "Ops" names (one slide, or one quiz matching item).**
- AIOps: AI applied to IT operations, for example predicting server failures from logs. Different goal from MLOps. [source: Day 3 30:35 to 40:25, his correct examples only]
- ModelOps: the release, monitoring and retirement half of the model lifecycle. [source: Psitron M01 p34 to p35, p35 visual-checked]
- GitOps: Git is the source of truth for infrastructure and deployments, and a controller or pipeline applies the changes. [synthesis: Psitron M01 p36 to p38, corrected; see limits]
- LLMOps: MLOps practices for large language model applications. Optional session after the capstone. [source: Psitron M01 p39 to p41; CURRICULUM section 8]

**Diamond example.**
- Two `problem-framing.md` risks show "breaks quietly". **Data drift:** buyers shift to larger stones, so inputs stop looking like the training data. **Concept drift:** prices change, so the same features now mean a different price. Neither raises an error. Only the numbers move. Week 11 catches the first with a drift report, Week 12 the second with live error once real sale prices arrive. [source: `problem-framing.md` section 3, tag `m01`]
- Keep these two definitions apart from Week 1 on. Some sources blur them (Google's level 1 trigger list calls a change in data distribution "concept drift"; the Psitron Level 4 example calls customer behavior change "data drift"). [source: notes.md M01-R2b teaching flag; videos.md section 7]

**Limits and common mistakes.**
- The Psitron AIOps example (a chatbot explaining loan terms) is a business AI application. AIOps means AI used to run IT systems. The MTTR explanation in the same segment is wrong: MTTR is the mean time to restore service after a failure. Do not reuse either. [source: videos.md section 3]
- The Psitron GitOps explanation says "AWS automatically fetches the changes" from GitHub. AWS does not pull from GitHub by itself; a controller such as Argo CD or Flux, or a pipeline, applies the change. It also mixes GitOps with infrastructure as code. [source: videos.md section 3]
- Psitron's DevOps tool list (Ansible, Chef, Puppet, Travis CI) is dated for this course. Name GitHub Actions and Terraform, which students use. [decision: source-map section 3]
- Psitron interview Q5 narrows DataOps to "alarms on data change". The manifesto is broader: delivery, orchestration, versioning, testing and monitoring of analytics pipelines. [source: notes.md item 16]
- The DataOps Manifesto is stewarded by a tool vendor (DataKitchen). Use it for one line. Do not teach its "+1 Start With Data Testing" item; it advertises the vendor's tool. [source: notes.md M01-R6c]
- None of the four videos mention DataOps. [source: videos.md section 3]

**Diagram spec: "Three practices" table.**
- The 4-row table above, as one slide. Optional second picture: a DevOps loop (plan to improve) with three extra boxes attached for MLOps: data, model, continuous training. Redraw from the idea of Psitron M01 p22 (three linked loops, visual-checked); do not copy its infinity-loop artwork.

**Demo and practical link.**
- Quiz 1 topic "MLOps vs DevOps" draws from the table and the five Google differences.

**Expected outcome.** Students can fill the "how you notice" column for one example per practice, and explain why a model can fail with no error.

**If it goes wrong.** If students treat DataOps as a job title for data engineers, go back to the manifesto line: delivery of analytics data with tests, versioning and monitoring, shared across roles.

**Sources.** Google Cloud MLOps page (read-full). DataOps Manifesto (read-full, no page date, checked 2026-10-05). Psitron M01 p22, p28, p34 to p41 (read-full text; p22, p28, p31, p35, p42 visual-checked). Psitron Day 1 and Day 3 (transcripts read-full). Zoomcamp 1.5 P3 (AI-cleaned, paraphrase). `problem-framing.md` at `m01`.

---

## Topic 4. The ML lifecycle: scope, data, model, deploy, monitor, decide, loop back

**Objective.** Students can draw the lifecycle from problem framing to monitoring, with the loops back, and say what question each stage answers. (Objective 2.)

**Explanation.**
- The course uses 6 stages. Each stage answers one question: [source: `docs/lifecycle.md`, tag `m01`]

| Stage | Question it answers | Diamond output | Week |
|---|---|---|---|
| 1. Scope | Who uses the prediction, and what is "good"? | `docs/problem-framing.md` | 1 |
| 2. Data | Is the data valid, and which version trained the model? | Validated `diamonds.csv`, tracked by DVC | 3 |
| 3. Model | Is this model better than the current one? | Tracked runs; best model gets the `champion` alias | 2, 4, 5 |
| 4. Deploy | Can other programs use the model, safely and repeatably? | Batch job, API, container, CI/CD, AWS Lambda | 6 to 10 |
| 5. Monitor | Is the service healthy, and is the model still right? | Service dashboards and drift report (W11); live error once actual sale prices arrive (W12) | 11 to 12 |
| 6. Decide | The model got worse. What now? | Retrain, roll back, or wait | 12 |

- The loops matter as much as the stages: [source: `docs/lifecycle.md`]
  - Model misses targets: go back to **Data**. Most model problems are data problems. Check the data before tuning.
  - Retrain: new data goes back through **Data** validation first.
  - Roll back: move `champion` back to the previous version (**Deploy**). No retraining needed.
  - Targets wrong: go back to **Scope** (for example, sellers need a faster answer).
- Why our version and not a textbook circle: many lifecycle pictures stop at deployment. Psitron's lifecycle circle (M01 p26) goes from gathering data to deployment with no monitoring and no loop back. Its spoken walk also ends at "move to production". Use it as a "what is missing?" prompt. [source: Psitron M01 p26, visual-checked; Day 3 8:09 to 13:40]
- Google's 8 steps (extraction, analysis, preparation, training, evaluation, validation, serving, monitoring) are a finer version of stages 2 to 5. Its step 6, model validation, is our quality gate: the model must beat the baseline and the current champion before release. [source: Google "Data science steps for ML"]
- The only spoken closed-loop lifecycle in our videos: the Psitron Level 4 whiteboard. Prep, train, evaluate, deploy, monitor, then back to data. Three retraining triggers: a monitoring alert, a schedule, a code change. [source: Day 6 2:36:29 to 2:41:56; drawing not seen, transcript only]
- Psitron's components view (M01 p23 to p25) adds a useful point: production monitoring covers the models and the infrastructure, including failed CI/CD jobs. [source: Day 3 3:53 to 8:09; p23 visual-checked]

**Diamond example.** Today (`m00`) only stage 3 exists, and only inside a notebook. Every other stage is built during the course. [source: `docs/lifecycle.md` "Today"]

**Limits and common mistakes.**
- Mistake: drawing a straight line that ends at "Deploy". Every lifecycle in this course has a loop back from monitoring.
- Mistake: putting Scope outside the lifecycle. Framing decides the metric and threshold that every later stage checks.
- The Day 6 whiteboard example ("drift above 30% means retrain") uses an invented threshold. If used, label it as an example. [source: videos.md section 7]
- The Psitron Day 3 walk calls TensorFlow and scikit-learn "algorithms" (they are libraries) and says Apache MXNet is from Microsoft (it is an Apache project). Do not reuse. [source: videos.md section 4]

**Diagram spec: "Diamond lifecycle".**
- Use the Mermaid diagram in `docs/lifecycle.md` at tag `m01` exactly: 6 boxes left to right (Decide is a diamond shape), with 4 labelled back arrows: retrain (Decide to Data), roll back (Decide to Deploy), targets wrong (Decide to Scope), misses targets (Model to Data). Render it as a slide; light up only stage 3 for "today".

**Demo and practical link.**
- Live demo: build the lifecycle diagram in Mermaid on screen (paste into mermaid.live), stage by stage, then add the loops one at a time while saying why each exists.
- Practical 1 Part C: students draw their own diamond lifecycle (Mermaid recommended). Done when all lifecycle stages are present. Answer key: `docs/lifecycle.md` at `m01`. Students start from the stub on `start-m01`.

**Expected outcome.** The Mermaid diagram renders 6 stages and the 4 labelled back arrows, matching `docs/lifecycle.md` at `m01`.

**If it goes wrong.** If mermaid.live shows a syntax error, check the first line is `flowchart LR`, that labels with `<br/>` or brackets are inside double quotes, and that each arrow uses `-->`. If it still fails or there is no internet, show the pre-rendered picture (a deck item) and paste the `m01` source after class.

**Sources.** `diamond-mlops/docs/lifecycle.md` at `m01` (read-full this run). Google Cloud MLOps page (read-full). Psitron M01 p23 to p26 (read-full text; p23, p26 visual-checked). Psitron Day 3 and Day 6 (transcripts read-full).

---

## Topic 5. Problem framing with measurable success criteria

**Objective.** Students can turn a vague goal into measurable criteria: who uses the prediction, a metric with a threshold, latency and cost limits, and the main failure risks. (Week 1 Evidence; Practical 1 Part B.)

**Explanation.**
- Framing comes first because every later check needs a target. The model gates (Week 4 registration, Week 5 pipeline, Week 9 CI, Week 12 retraining) compare a new model against the MAE and R2 targets set here. Release and operating targets (latency, batch time, cost) are also set here and checked once those parts exist. Operational alert thresholds, such as the Week 11 drift alert, are calibrated later, when there is live data to set them against. [synthesis: `problem-framing.md` section 2; `lifecycle.md` stage 1]
- Psitron's components view starts the same way: the business team and the data scientist turn a business problem into a "viable problem statement" with KPIs, and production monitoring later checks the models still meet those KPIs. Neither source gives thresholds. [source: Day 3 4:42 to 5:35 and 7:51 to 8:09; Psitron M01 p24]
- A complete framing answers 4 questions:
  1. **Who uses the prediction, and how?** Online one at a time, or in a batch?
  2. **What does "good" mean?** A metric and a threshold, plus latency and cost limits.
  3. **What can go wrong in production?** Each risk with how it will be caught.
  4. **Where is the project on the maturity model today?** (Topic 6.)
- Two kinds of targets, checked at different times: [source: `problem-framing.md` section 2]
  - **Offline model gate.** Checked on the fixed holdout before a model can become `champion`.
  - **Release and operating targets.** Latency, batch run time, cost. Measured only once that part of the system exists. Until measured, a target is "not measured". It never counts as passed.

**Diamond example** [fictional company, real numbers]. Sparkle Exchange, an online marketplace where sellers list loose diamonds. [source: `problem-framing.md`, tag `m01`]

| Vague | Measurable |
|---|---|
| "The price should be accurate" | MAE 300 USD or less on the 10,755-row holdout. Today: 279.29. (Average diamond is about 3,933 USD, so 300 USD is under 8%.) |
| "It should follow the price pattern" | R2 0.98 or more. Today: 0.9826 |
| "It should be fast" | Online p95 latency 500 ms or less: across a measured set of requests (for example one load-test run), 95% finish within 500 ms and up to 5% may be slower. Today: not measured |
| "The daily batch should be quick" | 15 minutes or less for 50,000 rows. Today: not measured |
| "It should be cheap" | 10 USD a month or less on AWS at course traffic |
| "It should not miss expensive stones" | Report MAE for diamonds above 10,000 USD, with the row count. No target yet: record a baseline first |

- Users: seller (suggested price while filling in the form, under a second), pricing analyst (daily batch for all new listings), buyer ("fair price" badge). A person always sets the final price, which limits the damage from a bad prediction.
- The offline gate: MAE 300 or less, R2 0.98 or more, and MAE not worse than the current `champion`.
- Code link: the "above 10,000 USD" slice from this framing became a real block in `src/diamond/evaluate.py` at tag `m02`. [source: `evaluate.py` lines 77 to 80 at `m02`]

**Limits and common mistakes.**
- Mistake: a metric with no threshold ("we will track MAE"). A metric only becomes a target once it has a number and a reason.
- Mistake: only model metrics. Latency and cost are success criteria too. A model that is accurate and takes 5 seconds fails the seller.
- Mistake: marking a target "passed" before it can be measured.
- MAE alone hides large errors on expensive stones. That is why the slice exists.
- A fixed threshold can go stale. If diamond prices inflate, 300 USD becomes a stricter target. Sculley et al. call this "fixed thresholds in dynamic systems". Revisit thresholds when the world changes. [source: Sculley p. 7; notes.md item 15]
- The general promotion rule in CURRICULUM and the diamond targets here both stand. Diamond code and practicals use the project targets. [decision: PROJECT_STATE decision 2026-10-04]

**Diagram spec: "Vague vs measurable".** The two-column table above, as one slide. No other drawing.

**Demo and practical link.**
- Practical 1 Part B: students write `docs/problem-framing.md` answering the 4 questions with numbers they can check. Their choices may differ from ours. Answer key: `problem-framing.md` at `m01`.
- Optional cost framing example for speaker notes: the Psitron edge example (a factory camera inspecting 10,000 products a day: cloud calls cost money per prediction, and a network outage stops the line) shows why latency and cost belong in the framing. Its numbers are invented and in rupees. If used, rebuild it in USD and label it as invented. [source: Day 6 3:49:36 to 3:53:19]

**Expected outcome.** Each student's framing has a metric with a threshold, a latency target, a cost limit, and at least 3 risks with how each is caught.

**If it goes wrong.** The most common gap is a metric with no number ("accurate"). Ask "what number would make you reject this model?" Second most common: marking latency as passed before anything can measure it.

**Sources.** `diamond-mlops/docs/problem-framing.md` at `m01` (read-full this run). `src/diamond/evaluate.py` at `m02` (read this run, lines 77 to 80). Psitron Day 3, Day 6 (transcripts read-full). Psitron M01 p24 (read-full text). Sculley p. 7 (read-full).

---

## Topic 6. The MLOps maturity model, Levels 0 to 4

**Objective.** Students can place a team on Levels 0 to 4, give the evidence for the score, and say what the next level needs. (Objective 3.)

**Explanation.**
- The course uses Microsoft's five-level model (Azure Architecture Center, "MLOps maturity model", last updated 2026-06-03). Both teaching programs we draw on teach a five-level model with the same structure: the Zoomcamp speaker says his is borrowed from Microsoft, and Psitron uses the same level names except Level 4, which Psitron calls "Full MLOps Automated retraining" and Microsoft calls "Full MLOps automated operations". [source: Microsoft page, read-full; Zoomcamp 1.5 P1; Psitron M02 p3, visual-checked]
- What it is for: a team judges where it is and plans small steps forward, instead of trying to automate everything at once. It is qualitative. Levels are cumulative: each level keeps what the lower levels have. [source: Microsoft overview; Day 6 2:25:00 to 2:27:11 and 2:33:14 to 2:33:21]
- Real teams are mixed. Microsoft says an organization often shows traits of more than one level, and the levels overlap like a continuum. So "mostly Level 1, some Level 2" is a valid score. [source: Microsoft, paragraph after the summary table]

**The course scale.** [decision: Daniel, 2026-10-05. Keep Microsoft's level names. Describe each level the way the two teaching programs (Psitron's spoken Day 6 walk and Zoomcamp 1.5) teach it. Where they disagree with Microsoft, the course follows the teaching programs and says so.]

| Level | Name | What is true at this level | Who works together |
|---|---|---|---|
| 0 | No MLOps | Everything manual, usually in notebooks. Data gathered by hand. No experiment tracking, and no automated or repeatable model tests or quality gate. The data scientist evaluates the model by hand (for example RMSE) and decides alone whether it is good enough and hands over a model file | The data scientist works alone; engineers re-implement the notebook |
| 1 | DevOps but no MLOps | The **code** is engineered: it lives in Git, has unit and integration tests, and CI runs them on every push. CI covers code only. Training, evaluation and hand-off of the model are still manual, and runs are not tracked, so models are hard to reproduce | Experienced developers help the data scientist |
| 2 | Automated training | Training is a repeatable pipeline (even a parameterized `python train.py`). Data and models are versioned. Every run is tracked and a registry says which model is live. Release is still manual, but easy | Data scientists and engineers on one team |
| 3 | Automated model deployment | Deployment goes through a CD pipeline with little or no human action. Models and the serving infrastructure are monitored. Teams often compare old and new models with A/B tests | Data, ML and software engineers together |
| 4 | Full MLOps automated operations | Monitoring closes the loop: a drift or performance alert (or a schedule, or a code change) triggers retraining, evaluation and release of a new model, with little or no human action | As Level 3, plus metrics from production feed back into the pipeline |

[source: Psitron Day 6 2:27:11 to 2:41:56 (Level 0 to 4 walk, three retraining triggers); Zoomcamp 1.5 P2 to P6 (paraphrase); Microsoft per-level tables for names, people and Level 4 wording]

- **Where the course scale differs from Microsoft: Level 1.** Psitron's Level 1 is GitHub plus CI with automated unit and integration tests, where CI covers code only. Microsoft (and the Zoomcamp video) also expect automated **application releases** at Level 1. The course uses Psitron's version, so a project can earn Level 1 by engineering its code before any application exists. Tell students that some teams (and Microsoft's article) count automated releases as part of Level 1, so they recognise that version at work. [source: Day 6 2:29:45 to 2:31:59; Microsoft Level 1 table; Zoomcamp 1.5 P3]
- Smaller differences, all handled the same way:
  - Level 2: Psitron stresses versioned data and models and automated training; Zoomcamp stresses experiment tracking and a registry. The course scale includes both. Microsoft agrees: tracked experiments, version-controlled training code and models, manual release. [source: Day 6 2:31:59 to 2:33:47; Zoomcamp 1.5 P4; Microsoft Level 2]
  - Level 3: Microsoft and Zoomcamp put A/B testing here; Psitron does not. The course scale says "often", because the diamond project does not build A/B testing. [source: Microsoft Level 3; Zoomcamp 1.5 P5; videos.md section 7]
  - Level 4 name: Psitron's slides say "Full MLOps Automated retraining". The course uses Microsoft's "Full MLOps automated operations" and says it includes retraining. [source: notes.md item 1]
- What moves a team up, one line each: [synthesis: course scale above]
  - 0 to 1: the **code** gets engineered: Git, tests, CI on every push.
  - 1 to 2: **training** becomes a tracked, versioned, repeatable pipeline.
  - 2 to 3: **deployment** becomes automatic, and the model and service are monitored.
  - 3 to 4: **monitoring** triggers retraining and release.
- **Not every model needs Level 4.** A proof of concept can stay at Level 0. Production needs at least Level 1. Several models make Level 2 worth it. Level 2 or 3 with monitoring is often enough, especially where a human must sign off. Choosing the target level is part of framing. [source: Zoomcamp 1.5 P7, paraphrase; Psitron has no equivalent]
- Google uses 3 levels: 0 manual process, 1 ML pipeline automation (continuous training), 2 CI/CD pipeline automation. Rough mapping (ours, stated by neither source): Google 0 = course Levels 0 and 1; Google 1 = course Level 2 plus automatic retraining triggers; Google 2 = course Levels 3 and 4. Say "roughly": Google puts performance-triggered retraining at its level 1. [synthesis: notes.md mapping section; Google page]
- Translate Azure terms from Microsoft's article to our stack: Azure ML registries become the MLflow registry with aliases; Event Grid triggers become Prefect triggers or AWS events; "managed feature store" becomes a Feast demo only. [decision: notes.md teaching notes]

**Diamond example: where the project climbs.** [source: `problem-framing.md` section 4, tag `m01`; scored on the course scale]

| Weeks | What the diamond project gains | Course-scale score |
|---|---|---|
| 0 to 1 | **Today.** One notebook run by hand. The model is evaluated by hand inside the notebook, with no unit tests of the model code and no quality gate (the Week 0 setup check reruns the notebook end to end, by hand), no run tracking, no deployment | Level 0 |
| 2 to 3 | Code in a tested package in Git, a CI check (lint and tests) on every push (W2); versioned and validated data (W3) | Level 1, with a first Level 2 trait (versioned data) |
| 4 to 5 | Tracked runs, registry with `champion`, a pipeline that trains by itself | Level 2 |
| 6 to 10 | API, container, CI/CD release to AWS | Level 3 for deployment; model monitoring arrives in Week 11 |
| 11 to 12 | Monitoring, retraining, rollback | Level 3 complete (W11), Level 4 traits (W12) |

- Why Level 0 today: the notebook is the only way to train; nobody records which data or settings made which model; no other program can get a prediction; nobody would notice if the model got worse. The starter's pinned packages and setup check confirm the environment, and the setup check also reruns the notebook end to end and checks its numbers. There are still no unit tests of the model code, nothing runs on every push, and nothing judges a new model. [source: `problem-framing.md` "Why Level 0 today"; `scripts/run_notebook.py` lines 39 to 52, tag `m00`. The `m01` file says these safeguards only "check the environment"; this file corrects that]
- Next 3 changes, in order: (1) tested package with experiment settings moved out of the code into `params.yaml` (Week 2; paths and feature lists stay in `src/diamond/config.py`), because nothing can be automated until code runs outside a notebook; (2) version and validate the data (Week 3), because no result can be traced to its data otherwise; (3) track every run and register the best model (Week 4), because otherwise nobody can prove a new model is better. [source: `problem-framing.md`]
- Notes against the `m01` answer key (the tag cannot move, so the practical answer key follows this file):
  - `problem-framing.md` lists "versioned data" at Level 1. On the course scale, versioned data is a Level 2 trait that arrives early, in Week 3. [source: Day 6 2:31:59 to 2:33:47; notes.md item 14]
  - `problem-framing.md` puts rollback at Level 4. The maturity sources do not name rollback; Google does (monitor live performance so you can roll back; metadata keeps a pointer to the previous model). Cite Google for rollback. [source: notes.md item 12]
  - The diamond project does not build A/B testing. Call it "Level 3 without A/B testing". [source: notes.md teaching notes]

**How to score a team per pillar (for Practical 1 Part A).** [decision: our adaptation. Microsoft scores along people, model creation, model release and application integration. CURRICULUM asks for a score per pillar, so we map each pillar to the course-scale level where it first appears.]

| Pillar | Level 0 looks like | Evidence for Level 1 or 2 | Evidence for Level 3 or 4 |
|---|---|---|---|
| Version everything | Files on laptops, `final_v2.csv` | Code in Git (L1); data and models versioned and tied to each run (L2) | Every deployed model traces to its data, code and config |
| Track experiments | Results in a spreadsheet or not at all | Every run tracked centrally; a registry says which model is live (L2) | Promotion follows a written rule, applied automatically (L4) |
| Orchestrate | Cells run by hand | Training is a repeatable, scheduled or triggered pipeline (L2) | Monitoring alerts trigger the pipeline (L4) |
| Serve | Model file emailed to an engineer | Scoring code version controlled and tested (L1) | Deployment automated through CD (L3) |
| Containerize | "Works on my machine" | Defined, pinned environments for training (L2) | The same image runs in test and production (L3) |
| CI/CD | Manual builds | CI runs tests on every push (L1) | Model release through CD with tests (L3) |
| Monitor | Nobody would notice | Training performance tracked (L2) | Live model and service metrics (L3); drift triggers retraining (L4) |
| Infrastructure as code | Clicked together in a console | Environment definitions in files (L2) | Whole environment (train, test, prod) managed as code (L3) |

- Score each pillar on its own, then give one overall score with "mostly X, some Y". Recommend the next 3 changes in order, each with a reason (the diamond list above is the model answer).

**Limits and common mistakes.**
- The Psitron level **slides** (M02 p4 to p8) are muddled: "a dummy-like model" (L0), "pipelines will have ability to generate data automatically" (L1), "monitored through unit tests" (L4). Do not use the slide text. The course scale above follows the instructor's spoken walk, which is clear. [source: notes.md item 2; videos.md section 7]
- Mistake: "Level 1 means the model is automated." At Level 1 only the code is engineered. Training and hand-off are still manual. [source: Day 6 2:29:45 to 2:31:59]
- Mistake: "Level 2 means CI/CD for models." Level 2 release is still manual. Automated deployment starts at Level 3. The old course quiz (Q4) got this wrong. [source: notes.md item 3; Day 6 2:31:59 to 2:33:47]
- Mistake: "Higher is always better." See Zoomcamp P7 above.
- Mistake: quoting a level definition as "the" standard. Sources differ at the edges (Level 1 is the clearest case). Score from evidence and name the scale you used.

**Diagram spec.**
- (a) **Maturity ladder**: 5 stairs, Level 0 at the bottom. On each stair: the level name, the one-line "what moves you up", and the diamond weeks from the table above. A "you are here" marker on Level 0. Idea from the Psitron M02 p3 pyramid (visual-checked); redraw as stairs in our style.
- (b) **Scoring grid** for Practical 1 Part A: rows = 8 pillars, columns = Levels 0 to 4, one tick per row. Original.
- (c) Optional **Google mapping line**: Google 0 / 1 / 2 under course Levels 0 to 1 / 2 / 3 to 4, with "roughly" on the slide.

**Demo and practical link.**
- Demo: score the diamond notebook live with the grid. Most pillars land at Level 0. Ask: "What is the smallest change that moves one pillar up?" (Answer: put the code in a tested package with CI, Week 2.)
- Practical 1 Part A: score a one-page company scenario per pillar and recommend the next 3 changes in order. The scenario is fictional and written in M01-PRAC (after this content is approved). It must be labelled fictional.
- Quiz 1 topic "maturity levels" comes from the course-scale table and the mistakes list.

**Expected outcome.** Scoring the notebook live gives Level 0 on almost every pillar. The code is in Git with pinned packages, but there are no unit tests and no CI (the Week 0 runner is an end-to-end metric check, not CI), so even "version everything" stays at Level 0 with one Level 1 trait.

**If it goes wrong.** If students score Level 2 because the notebook uses a scikit-learn `Pipeline`, separate the two ideas: a scikit-learn pipeline bundles preprocessing and model; an automated training pipeline runs without a person. If a student quotes Microsoft's stricter Level 1 (automated releases), agree that it is a valid reading and point to the course-scale note above. If the class disagrees on a pillar, ask for the evidence line from the table.

**Sources.** Psitron Day 6 2:24:38 to 2:42:11 (transcript read-full). Zoomcamp 1.5 (AI-cleaned transcript, read-full, paraphrase only). Microsoft "MLOps maturity model" (read-full raw HTML, last updated 2026-06-03, checked 2026-10-05; notes.md M01-R2a). Google Cloud MLOps page (read-full, last reviewed 2024-08-28). Psitron M02 p3 to p8 (read-full text; p3 visual-checked). `problem-framing.md` section 4 at `m01`.

---

## Topic 7. Hidden technical debt in ML systems

**Objective.** Students can name the main kinds of ML technical debt, spot each one in the diamond project, and say which week pays it off. (Objective 4.)

**Explanation.**
- Technical debt is Ward Cunningham's 1992 metaphor: shortcuts that speed you up now and cost you later. Sculley et al. (Google, NIPS 2015, "Hidden Technical Debt in Machine Learning Systems") applied it to ML. They did not coin the term. [source: Sculley p. 1]
- Their main claim: ML lets you build a working system fast, but real ML systems often build up large ongoing maintenance costs. ML has all the normal code debt plus extra debt at the **system** level. So normal fixes (refactoring, more unit tests, deleting dead code) are not enough on their own. The root cause: data shapes the system's behavior, so normal module boundaries do not hold. [source: Sculley pp. 1 to 2]
- The four debt types CURRICULUM names, plus two the diamond project meets early:

| Debt | What it is (our words) | Diamond example | Paid off in |
|---|---|---|---|
| **Glue code** (p. 5) | Lots of code written only to move data into and out of an ML package. It locks you to that package | [fictional] Ad hoc reshaping in the notebook, then different reshaping written again for an API | W2: one saved pipeline (`preprocess.py` plus the model, saved as `diamond_pipeline.joblib` by `train.py`) that `predict.py` loads to score new records. The API (W6) loads the same file |
| **Pipeline jungles** (p. 5) | Data preparation that grew one step at a time (scrapes, joins, temp files) into a tangle that is hard to test or recover | [fictional] `clean_v2_final.csv`, `diamonds_filtered.csv`, cells run by hand in a remembered order | W3 and W5: declared DVC stages and a Prefect flow |
| **Data dependencies** (pp. 3 to 4) | Inputs produced by someone else that change without warning (unstable), or inputs that add little but break the model when they vanish (underutilized). Data has no compiler that lists dependencies | A supplier renames the `cut` grade "Very Good" to "Very-Good". The encoder breaks or maps it wrong | W3: DVC-versioned data and a pandera schema listing allowed `cut` values |
| **Feedback loops** (p. 4) | A live model changes the data it will later learn from (direct), or two systems affect each other through the world (hidden) | Sellers accept the suggested price, so future "sale prices" are partly the model's own output | W12 **measures** it: live error per model version against actual sale prices. It does not remove it, because those prices are still influenced by the suggestions. Removing it needs a control group (for example some listings shown no suggestion), which the course does not build |
| **Configuration debt** (p. 6) | Settings (features, data selection, hyperparameters, thresholds) treated as an afterthought and never tested | Paths and parameters hardcoded in notebook cells (cell 27) | W2 (tag `m02`): `params.yaml` holds the seed, split size, model name and hyperparameters; `tests/test_config_matches_code.py` checks the seed, model and hyperparameters match the code and the saved model. The feature lists live in `src/diamond/config.py` and are not checked by that test, so this debt is only partly paid |
| **Changes in the external world** (p. 7) | The world moves, so fixed thresholds go stale and tests alone are not enough. You need live monitoring | The "MAE 300 USD" gate and a "fair price within 10%" badge rule stop fitting if prices inflate | W11 to W12: monitoring with alerts; revisit thresholds |

[source: Sculley sections cited by page; diamond examples are fictional illustrations, notes.md items 4 to 16]

- The diamond examples for glue code, data dependencies, feedback loops and the external world describe events that have not happened (the supplier rename, sellers accepting prices, the badge rule). Teach them as [fictional] illustrations. The configuration example is real: the notebook hardcodes paths and parameters (cell 27). [source: notebook cell 27]
- The Sculley remedies, in one line each: wrap ML packages behind common APIs (glue code); redesign data collection as a whole (jungles); version and freeze input signals, and run leave-one-feature-out checks (data dependencies); keep some data free of the model's influence (feedback loops); keep configs small, reviewed, diffable and checked automatically (configuration); monitor prediction bias, set action limits, watch upstream producers (external world). [source: Sculley pp. 3 to 7]
- One more idea for the "roles" link: Sculley says glue code and pipeline jungles often come from research and engineering being split into separate teams. Mixed teams help. Cultural debt is the same idea at team level: reward deleting features and better reproducibility as much as accuracy gains. [source: Sculley pp. 5 and 8]
- Five questions to judge debt (Sculley p. 8, paraphrased), good for a discussion or a self-check:
  1. How easily can a completely new approach be tested at full scale?
  2. What is the full chain of data dependencies?
  3. How precisely can you measure the impact of a change?
  4. Does improving one model or signal hurt others?
  5. How fast can a new team member become productive?

**For the curious (instructor notes or deeper reading, one line each).** Entanglement, "Changing Anything Changes Everything" (p. 2); correction cascades (p. 2); undeclared consumers (pp. 2 to 3); dead experimental codepaths, with the Knight Capital example the paper cites (p. 5); reproducibility debt (p. 8). The reproducibility example is real in our project: with scikit-learn 1.9.1 unpinned, the same code and data gave MAE 278.16 (278.15552478509267); pinning scikit-learn 1.7.2 restored 279.29. That is why every package is pinned and hash-locked. [measured before the Python 3.12 switch: Codex P-02 run, 2026-10-03 15:00 ET, WSL2 Ubuntu 22.04, Python 3.11.15, `make install && make train && make evaluate` on the reference project in `sources/diamond-mlops-reference`, logged in `handoffs/runs/2026-10-03-codex.md`. Sculley p. 8 for the debt type]

**Limits and common mistakes.**
- Do not say "95% of ML code is glue" as a fact. The paper says a mature system "might" be at most 5% ML code. [source: notes.md item 7]
- The paper's Figure 1 has 9 boxes around "ML Code" (listed in Topic 1). "Testing", "automation" and "metadata" come from Google's adapted figure, and "people" from neither. Match the original boxes. [source: notes.md item 6]
- The 2014 workshop paper "Machine Learning: The High-Interest Credit Card of Technical Debt" is a different, earlier paper. Do not mix up the titles. [source: notes.md M01-R1 note]
- None of the videos cover this topic, and nothing in `sources/` covers it. The paper is the only source. Daniel should read Sections 1 to 5 before teaching (about 5 pages). [source: videos.md section 8; source-map section 8]

**Diagram spec.**
- Reuse the "model is a small box" figure from Topic 1 as the opener.
- Then the 6-row debt table above as one slide, with the "Paid off in" column highlighted, so each debt points to a later week.

**Demo and practical link.**
- Demo: in the notebook, point at one example of each: hardcoded parameters (configuration), the manual cell order (pipeline jungle), the CSV read with no schema (data dependency).
- Quiz 1 topic "types of ML technical debt" uses the table.

**Expected outcome.** Students find 3 debts in the notebook: hardcoded settings (configuration), a manual cell order (pipeline jungle), and a CSV read with no schema (data dependency), and name the week that pays each off.

**If it goes wrong.** If students cannot see a pipeline jungle in one notebook, point at the cleaning steps that must run in a remembered order before training. If they ask for the paper's numbers, repeat the hedge: "might", at most 5% ML code.

**Sources.** Sculley et al. 2015, NIPS 28 (read-full pp. 1 to 9 from the publisher PDF, Figure 1 visual-checked, checked 2026-10-05; notes.md M01-R1). Diamond notebook cell 27 at `m00`. `problem-framing.md` risk table at `m01`.

---

## Topic 8. The 8 production pillars and the course map

**Objective.** Students can name the 8 pillars and say which week builds each one, so every later week has a place on the map. (Supports objectives 2 and 3.)

**Explanation.**
- The course is built on 8 production pillars: version everything (code, data, model), track experiments and register models, orchestrate pipelines, serve (batch and real time), containerize, CI/CD with automated checks, monitor for drift and performance, and infrastructure as code. [source: `sources/planning/MLOps-Target-Module-List.md` line 12, read-full in P-10]

| Pillar | Week | Tool students use |
|---|---|---|
| Version everything | W2 (code), W3 (data), W4 (models) | Git and GitHub, DVC, MLflow registry |
| Track experiments, register models | W4 | MLflow (alias `champion`) |
| Orchestrate | W5 | Prefect |
| Serve | W6 | FastAPI, batch script |
| Containerize, then run containers | W7 (build and store images), W8 (run and scale them) | Docker and Amazon ECR (W7); Kubernetes on a local Minikube cluster (W8) |
| CI/CD | W2 (first check), W9 | GitHub Actions |
| Infrastructure as code | W10 | Terraform on AWS |
| Monitor | W11 (W12 retrain and roll back) | Evidently, Prometheus, Grafana |

[source: CURRICULUM sections 4 and 5]

- The pillars line up with the "what moves you up" steps in Topic 6: versioning, tests and CI give Level 1, tracking and orchestration give Level 2, serving through CI/CD and cloud gives Level 3 deployment, monitoring completes Level 3, and retraining gives Level 4 traits (course scale). [synthesis: Topic 6; `problem-framing.md` section 4]
- Psitron's best overview picture (M02 p44) shows the same shift. "Moving from" a 4-box workflow (data, processing, training, deployment) "to" a full flow: project identified, data, processing, model building, training, model artifact, deploy, integrate, operate. Supporting boxes: data version control, code repository, feature store, model registry. Two automated quality gates, a feedback arrow from operate back to the start, and a traceability bar under everything. [source: Psitron M02 p44, visual-checked]

**roadmap.sh MLOps components (coverage check).** roadmap.sh names these MLOps components: version control; CI/CD; orchestration; experiment tracking and model registry; data lineage and feature stores; model training and serving; monitoring and observability. It also lists infrastructure as code under MLOps principles. [source: `sources/roadmap/roadmap-sh-mlops.md`, read-full in P-10]

| roadmap.sh component | Our week |
|---|---|
| Version control | W2, W3 |
| CI/CD | W9 |
| Orchestration | W5 |
| Experiment tracking and model registry | W4 |
| Data lineage and feature stores | Partly: DVC and MLflow record lineage (W3, W4); Feast is a demo (W3) |
| Model training and serving | W4, W6 |
| Monitoring and observability | W11 |

[source: `sources/planning/roadmap-sh_MLOps_Comparison.md` section 1]

**Diamond example.** The section 1 course map in CURRICULUM is the pillar map drawn as a flow: notebook, clean repo (W2), validated and versioned data (W3), tracked models (W4), pipeline (W5), API and batch (W6), container (W7), Kubernetes (W8), CI/CD (W9), AWS and Terraform (W10), monitoring (W11), investigate, retrain or roll back (W12), back to the pipeline. [source: CURRICULUM section 1]

**Limits and common mistakes.**
- roadmap.sh text and layout must not be copied into student materials. Use the component names and a link to https://roadmap.sh/mlops only. [decision: AGENTS.md licensing]
- Psitron M02 p44 shows "feature store" as a core box. In this course Feast is a demo only (W3). Mark it "demo" on our redraw. [source: source-map section 5]
- The pillar list is our course's framing. Other courses group the same practices differently (for example Psitron's six "stages" on M02 p9: versioning, testing, automation, reproducibility, deployment, monitoring). Present ours as "how this course is organized". [source: Psitron M02 p9]

**Diagram spec.**
- (a) **Course map**: the CURRICULUM section 1 flowchart, with Week 1 lit up. This is the "where we are" picture reused in every deck.
- (b) **From workflow to system**: redraw Psitron M02 p44 with our tool names under each support box: DVC (data version control), Git and GitHub (code repository), MLflow registry (model registry), Feast (demo) (feature store), and "quality gate in GitHub Actions" on the two gates.
- (c) **Pillar map**: the 8-row table above as a grid of 8 tiles, each with week and tool.

**Demo and practical link.** Students keep the pillar map: Practical 1 Part A scores the scenario against these 8 pillars.

**Expected outcome.** Students place every week on the pillar map and see that each roadmap.sh component has a week (data lineage only partly).

**If it goes wrong.** If students ask where Kubernetes fits: Docker builds the container (Week 7); Kubernetes runs and scales containers that already exist (Week 8). Minikube is a small Kubernetes cluster on your own laptop. If they ask why Feast is only a demo, the answer is time: one 3.5-hour session per week.

**Sources.** `MLOps-Target-Module-List.md` (read-full in P-10; line 12 rechecked this run). CURRICULUM sections 1, 4, 5. `roadmap-sh-mlops.md` and `roadmap-sh_MLOps_Comparison.md` (read-full in P-10; rechecked this run). Psitron M02 p9, p44 (p44 visual-checked).

---

## Topic 9. Roles and hand-offs

**Objective.** Students can name the roles in an ML team, say what each hands to the next, and point to where hand-offs fail. (Objective 4.)

**Explanation.**
- Role lines for the course (one line each). Titles vary between companies and the boundaries blur, so teach what each role is responsible for. [source: Day 1 2:11:50 to 2:12:07, he says "a data engineer or a data scientist" does data prep]
  - **Data engineer:** builds pipelines that bring scattered data (CRM, in-house databases) into one place, and keeps it flowing. Kreuzberger et al. list "DataOps engineer" as a similar role, which links this role to Topic 3. [source: Day 1 2:18:45 to 2:20:03; M02 p70 visual-checked; Kreuzberger R4]
  - **Data scientist:** turns the business problem into an ML problem, then builds, trains and evaluates models. [source: Day 1 2:18:45 to 2:20:03; Kreuzberger R3]
  - **ML engineer:** turns the model into production code and gets it deployed. [source: Day 1 2:18:45 to 2:20:03]
  - **MLOps engineer:** builds and runs the ML infrastructure, manages the automated training pipelines and model deployment, and monitors both the model and the infrastructure. [source: Day 1 2:18:45 to 2:20:03; Kreuzberger R7]
  - **Platform engineer:** builds and runs the shared platform (cloud accounts, clusters, CI runners, registries) that many teams use. [decision: our course term. The closest published role is Kreuzberger's "backend engineer (ML infrastructure management)" in Figure 3; "platform engineer" itself is not defined in our evidence]
  - Kreuzberger et al. also name a **business stakeholder** (sets the goal, reports the return on investment), a **solution architect** (designs the architecture, picks technologies), a **software engineer** (design patterns and coding guidelines) and a **DevOps engineer** (CI/CD, workflow orchestration, deployment, monitoring). [source: Kreuzberger Section 4.3 R1, R2, R5, R6]
  - Also in the picture: business or pricing analysts who evaluate results, app developers who use the model, and DevOps who deploy and monitor. [source: Psitron M02 p70, visual-checked]
- Kreuzberger et al. treat ML engineer and MLOps engineer as **one** cross-domain role (R7) that combines data science, data engineering, software engineering, DevOps and backend skills. The Psitron instructor splits them (ML engineer deploys; MLOps engineer builds pipelines and infrastructure). Teach the published view, and mention that some companies split the title. [source: Kreuzberger R7 and Figure 3; videos.md section 9]
- **How the team changes with maturity** is the strongest teaching point. Microsoft's "People" column: at Levels 0 and 1 everyone works alone and software engineers receive models "remotely"; at Level 2 data scientists and data engineers turn experiments into repeatable jobs together; at Level 3 software engineers join to automate model integration; at Level 4 software engineers add post-deployment metrics. Zoomcamp says the same in plain words: the data scientist works alone (L0), experienced developers help (L1), one team (L2). [source: Microsoft per-level tables; Zoomcamp 1.5 P2 to P4]
- An MLOps engineer must understand what the data scientist builds, the same way a DevOps engineer must know whether the app is Java or Node. [source: Day 3 1:13:49 to 1:15:37]
- Role boundaries are also enforced by access. Example: data engineers do not get access to model infrastructure. This connects to the IAM users students set up in Week 0. [source: Day 3 29:54 to 30:27]

**Where hand-offs fail** [synthesis]:

| Hand-off | What goes wrong | Course fix |
|---|---|---|
| Data engineer to data scientist | The data changes and nobody tells the model owner (Sculley's unstable data dependency) | W3: versioned data and a schema check |
| Data scientist to engineer | The notebook is re-implemented by someone else, so training and serving disagree (training-serving skew) | W2: one package used by both training and serving |
| Engineer to operations | Nobody owns "is the model still right?" after release | W11: monitoring with alerts; W12: a runbook |
| Model to its consumers | Other teams quietly use the predictions; a model update breaks them (Sculley's undeclared consumers) | W6: a documented API contract; W10: access control |

[source: Sculley pp. 2 to 3; Google level 0 (engineers rebuild features, causing training-serving skew); Zoomcamp 1.5 P2]

**Diamond example** [fictional]. At Sparkle Exchange: a data engineer loads new listings nightly; a data scientist owns the price model; an ML engineer owns the API; a platform engineer owns the AWS account. The seller, the pricing analyst and the buyer consume the output. [source for the users: `problem-framing.md` section 1]

**Limits and common mistakes.**
- Kreuzberger et al. is a 2022 to 2023 study (literature review, tool review and interviews). Role titles in job adverts keep changing, so keep to one line each and make no salary or job-market claims. [decision: source-map section 9]
- Psitron M02 p70 has no MLOps engineer and no platform engineer. Add both on our redraw. [source: source-map section 9]
- Mistake: "MLOps is the MLOps engineer's job." Every role in the table does part of it.

**Diagram spec: "Who hands what to whom".** A left-to-right strip of the 6 lifecycle stages (Topic 4). A role icon above each stage: data engineer (Data), data scientist (Model), ML engineer (Deploy), MLOps engineer (pipeline arrows spanning Data to Deploy), platform engineer (a base bar under everything), analyst and app developer (consumers at the right). Red marks on the 4 hand-off points from the table. Idea from Psitron M02 p70 (visual-checked); original drawing.

**Demo and practical link.** Session plan 2:15 to 2:45. Short pair discussion: "In your current job, where does a hand-off like this break?" Quiz 1 topic "roles".

**Expected outcome.** Each pair names one real hand-off failure and the course week that fixes it.

**If it goes wrong.** If a student has no work experience to draw on, use the Sparkle Exchange cast in the diamond example instead.

**Sources.** Kreuzberger, Kühl and Hirschl, arXiv 2205.02302 v3, Section 4.3 "Roles" (PDF pp. 4 to 5, read-full for that section) and Figure 3 (visual-checked), checked 2026-10-05; `evidence/notes.md` Part C. Psitron Day 1, Day 3 (transcripts read-full). Psitron M02 p70 (read-full text, visual-checked). Microsoft maturity page (read-full). Zoomcamp 1.5 (AI-cleaned, paraphrase). Sculley pp. 2 to 3 (read-full). Google level 0 (read-full).

---

## Topic 10. The tool landscape, grouped by pillar

**Objective.** Students can place a tool they hear about into a pillar, and know which tool this course uses there. (CURRICULUM Concepts: tool landscape; this is the week's "alternatives" slot.)

**Explanation.**
- Hundreds of MLOps tools exist, and most do one pillar's job. The useful skill is to ask "which pillar does this tool serve?" and compare it with the course tool. [synthesis]
- Psitron's view: general CI/CD tools are not built for ML, so teams stitch purpose-built tools together, and there is "no golden pipeline": each organization combines different tools. [source: Day 1 2:47:18 to 2:49:44]

| Pillar | Course tool | Other tools students will hear about (named only) |
|---|---|---|
| Version code | Git, GitHub | (none on the course slides; GitLab appears under CI/CD) |
| Version data | DVC | Git LFS, lakeFS (1 slide in W3) |
| Track and register | MLflow | Weights & Biases |
| Orchestrate | Prefect | Apache Airflow (optional session), Kubeflow Pipelines |
| Serve | FastAPI | Flask |
| Containerize | Docker, Amazon ECR | Docker Hub (a public image registry) |
| Run and scale containers | Kubernetes on Minikube (a local cluster) | Amazon EKS (managed Kubernetes on AWS) |
| CI/CD | GitHub Actions | GitLab CI/CD, Jenkins, AWS CodePipeline |
| Infrastructure as code | Terraform | AWS CloudFormation |
| Monitor | Evidently, Prometheus, Grafana | Amazon CloudWatch |
| End-to-end platforms | none (we build from parts) | Amazon SageMaker AI (optional W10 session), Databricks (shown once) |

[source: course tools from CURRICULUM section 5. Every alternative is named on that week's CURRICULUM alternatives slide and was doc-verified as a current product on its official page on 2026-10-05 (`evidence/notes.md` Part C). Names only; no claims about features.]

- Two names changed recently, so use the current ones: AWS now calls SageMaker "Amazon SageMaker AI", and the Weights & Biases documentation now sits on CoreWeave's documentation site, where W&B Models is still offered for experiment tracking. [source: notes.md Part C, checked 2026-10-05]

**Limits and common mistakes.**
- Neptune appears in several Psitron tool lists. Its hosted product shut down on March 6, 2026. Do not list it. [source: notes.md, Daniel's note, Oct 5]
- Drop doubtful Psitron entries: "Hugging Face feature store", DataRobot and "DataKit" as data versioning tools. [source: source-map section 9]
- AWS CodeCommit and Google Cloud Source Repositories appear in Psitron lists. Do not list them. The course uses GitHub. [source: source-map section 9]
- Psitron says the MLflow registry moves models "between stages". The course uses aliases (`champion`). [source: source-map section 9; AGENTS.md section 10]
- Psitron calls Kubeflow "de facto" and says "Spotify uses Kubeflow". Both are unsourced and dated. Do not repeat. [source: videos.md section 9]
- The Psitron claim "security is available by default on cloud" is wrong for this course. Under the AWS shared responsibility model, the customer configures IAM, encryption and network access. Week 0 IAM practice depends on this. [source: videos.md section 9]
- Tool lists date fast. The alternatives above were checked on 2026-10-05. Each later week re-checks its own alternatives slide when its research is done. [decision]

**Diagram spec: "Tool landscape grid".** One tile per pillar. In each tile: the course tool large, 1 or 2 alternatives small. Layout idea only (a tools-by-category table) from Psitron M01 p58 (visual-checked). That page is the excluded GreenSteam stack, so reuse none of its content. No logos needed.

**Demo and practical link.** None. Quiz 1 can ask "which pillar does this tool serve?" for 2 or 3 tools.

**Expected outcome.** Students place 3 named tools into the right pillar and name the course tool beside each.

**If it goes wrong.** Platforms such as SageMaker AI and Databricks span several pillars; put them in the "platforms" row and say the course builds the same pieces separately so students see each one.

**Sources.** CURRICULUM section 5. Psitron M02 p12 to p63 (read-full text). Psitron Day 1, Day 3, Day 6 (transcripts read-full). Notes on Neptune (notes.md header, Daniel, Oct 5).

---

## Topic 11. A real case: from notebooks to production at Aramex

**Objective.** Students see a real company make the notebook-to-production move, and practise scoring maturity only from the evidence a write-up gives. (Supports objectives 1 and 3; discussion before Practical 1 Part A.)

**What the case says** (paraphrased from one article; all figures are vendor-reported, not independently audited): [source: Sancricca (AWS) and Basford (Inawisdom), "How to Predict Shipments' Time of Delivery with Cloud-based Machine Learning Models", AWS for Industries blog, 2021-03-23, read-full raw HTML, checked 2026-10-05]
- Company: Aramex, a global logistics company based in the Middle East. Use case: predict how long a shipment will take to arrive.
- The models existed in Jupyter notebooks. A partner team (Inawisdom) took them to a production system in 8 weeks, in 2019, and runs it 24/7.
- Model: XGBoost on SageMaker, more than 12 features, trained on 6.3 million rows.
- Serving: real-time predictions through API Gateway and Lambda, target response under 200 ms, up to 4 million predictions a day at peaks such as Eid and Black Friday.
- Operations: the models are retrained regularly, and adapted to behavior changes such as COVID-19.
- Reported results: delivery-prediction accuracy up 74%, call-centre volume down 40%. The work later grew to more than 15 ML use cases.

**Teaching points.**
- It is the production gap in a real company: working notebooks first, then a separate effort to serve, scale and retrain. [synthesis: Topic 1]
- The framing has real numbers: a latency target (under 200 ms) and a volume (4 million a day at peaks). Compare with the diamond targets (p95 500 ms). [synthesis: Topic 5]
- The serving shape (API Gateway in front of Lambda) is close to what students deploy in Week 10. [synthesis: CURRICULUM Week 10]
- **Scoring exercise.** "What maturity level is this team?" Real-time serving and regular retraining are stated. How releases happen, whether runs are tracked, and whether retraining is automatic are **not** stated. So the honest answer is "at least serving in production with regular retraining; the article does not show enough to score CI/CD or automation". This is the habit Practical 1 Part A needs: score from evidence, and say what is unknown. [decision]

**Limits and common mistakes.**
- Do not show the Psitron CodePipeline and Step Functions diagram (M01 p61) as Aramex's system. That diagram belongs to a separate, generic AWS sample (Doshi, AWS Machine Learning Blog, 2021-04-02). No first-hand source documents Aramex's CI/CD. [source: notes.md Part B, case 3 verdict]
- Do not add the address-to-coordinates model from the Psitron summary. It is not in the Aramex article. [source: same]
- Say "the companies reported" for the 74% and 40% figures.
- The other two Psitron cases (an Azure DevOps ticket classifier and GreenSteam) are **excluded**. Their only sources are neptune.ai pages we could not read; the GreenSteam page now shows only an acquisition notice. They return only if Daniel saves archived copies into `sources/`. [source: notes.md Part B header and verdicts]

**Diagram spec.** None needed. Optional: a 3-box strip "notebooks, 8 weeks, real-time API plus regular retraining" with the two reported results as small labels.

**Demo and practical link.** 5-minute pair discussion right before Practical 1 Part A.

**Expected outcome.** Pairs list 2 things the article shows and 2 things it does not show.

**If it goes wrong.** If students claim CI/CD from "API Gateway and Lambda", ask where the article says how releases happen. It does not.

**Sources.** Aramex article (read-full, checked 2026-10-05; notes.md Part B case 3). Doshi AWS blog (read-full, used only to explain why the p61 diagram is excluded).

---

## How the topics fit the Week 1 session

Planned against CURRICULUM's Week 1 session plan (3.5 hours). [decision]

| Time | Topics |
|---|---|
| 0:00 to 0:15 | Intros and course map (Topic 8 diagram a only: "where we are") |
| 0:15 to 1:15 | Topic 1 production gap (12 min), Topic 2 what MLOps is (8), Topic 3 DevOps / DataOps / MLOps (12), Topic 4 lifecycle with the live Mermaid build (15), Topic 5 problem framing (13) |
| 1:15 to 1:25 | Break |
| 1:25 to 2:15 | Topic 6 maturity model with live scoring (30), Topic 7 technical debt (20) |
| 2:15 to 2:45 | Topic 8 pillar map, roadmap.sh components and "from workflow to system" (10), Topic 9 roles (12), Topic 10 tool landscape (8) |
| 2:45 to 3:05 | Topic 11 Aramex discussion (5), then Practical 1 start in pairs (15) |
| 3:05 to 3:25 | Capstone brief (from P-07, not this file) |
| 3:25 to 3:30 | Wrap, Quiz 1 opens |

- Topic 5 (framing) is missing from the CURRICULUM Concepts list. It is the week's Evidence and Practical Part B. It fits in the first concept block because the lifecycle starts with Scope. [decision: source-map section 11]
- The first block is the tightest (5 topics in 60 minutes). If it runs long, move the "other Ops names" slide (Topic 3) to deeper reading.

## Slide candidates (not a deck design)

Indispensable messages and figures:
1. Course map with Week 1 lit (Topic 8a).
2. "The model is a small box" with weeks around it (Topic 1).
3. The notebook's own "what this is not" list (Topic 1).
4. One-line MLOps definition and the 3-circle picture (Topic 2).
5. DevOps / DataOps / MLOps table, plus "a model can go wrong with no bug at all" (Topic 3).
6. Diamond lifecycle with 4 loops (Topic 4).
7. Vague vs measurable, and the two kinds of targets (Topic 5).
8. Maturity ladder with "what moves you up" and "you are here" (Topic 6a).
9. Per-pillar scoring grid (Topic 6b).
10. "Not every model needs Level 4" (Topic 6).
11. Technical debt table with "paid off in" (Topic 7).
12. From workflow to system, our redraw of M02 p44 (Topic 8b).
13. Pillar map and roadmap.sh components (Topic 8).
14. Roles strip with the 4 hand-off failure points (Topic 9).
15. Tool landscape grid (Topic 10).
16. Aramex: what the article shows and what it does not (Topic 11).

Speaker notes only: the theatre forecaster story; the Google 3-level mapping; Sculley's remedies; the "why not GitHub for data" question; the Psitron edge cost example (if rebuilt in USD).

Deeper reading (one required resource, plus optional):
- Required: Sculley et al. 2015, Sections 1 to 5 (about 5 pages).
- Optional: Microsoft "MLOps maturity model"; Google Cloud "MLOps: Continuous delivery and automation pipelines in machine learning"; the Aramex article.
- For the curious: the rest of Sculley (entanglement, correction cascades, undeclared consumers, dead codepaths).
