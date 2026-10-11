# Problem framing: Diamond Price Prediction

Instructor solution for Practical 1, Part B (tag `m01`). Your version can make
different choices. It must answer the same 4 questions with numbers you can
check.

The company in this document is fictional.

## 1. Who uses the prediction?

**Sparkle Exchange** is an online marketplace where independent sellers list
loose diamonds.

| User | What they do with the prediction | What they need |
|---|---|---|
| Seller | Gets a suggested listing price while filling in the listing form | An answer in under a second, and a price they find fair |
| Pricing analyst | Reviews listings whose asking price is far from the suggestion | A batch of suggestions for all new listings, once a day |
| Buyer | Sees a "fair price" badge on listings close to the suggestion | Trust that the badge is not wrong too often |

So the model is used 2 ways:
- **Online:** one diamond at a time, from the listing form (Week 6 API).
- **Batch:** all new listings, once a day (Week 6 batch job).

The model **suggests** a price. A person always sets the final price. This
limits the damage from a bad prediction.

## 2. What does "good" mean?

Measured on the fixed holdout set (10,755 rows, seed 42) unless stated.

| Criterion | Target | Today (notebook, `m00`) | Why this number |
|---|---|---|---|
| Mean absolute error (MAE) | 300 USD or less | 279.29 | The average diamond costs about 3,933 USD. An error of 300 USD is under 8% of that. Sellers accept a suggestion in that range |
| R2 | 0.98 or more | 0.9826 | Guards against a model that is good on average but misses the overall price pattern |
| Online latency, p95 | 500 ms or less per request | not measured | A seller waits for the answer while typing. Above half a second the form feels slow |
| Batch run time | 15 minutes or less for 50,000 rows | not measured | The daily batch must finish before analysts start work |
| Cloud cost | 10 USD a month or less at course traffic | 0 (runs locally) | A student project on AWS Lambda and S3 should stay inside this |

**Two kinds of targets**

The targets are checked at different times, because some can only be
measured once that part of the system exists.

- **Offline model gate** (Weeks 4, 5, 9, and 12). A new model can become
  `champion` only if, on the same holdout:
  - MAE is 300 USD or less,
  - R2 is 0.98 or more, and
  - MAE is not worse than the current `champion`'s MAE.
- **Release and operating targets** (from Week 6 on). Online p95 latency
  (Week 6, then Weeks 8 and 11), batch run time (Week 6), and cloud cost
  (Week 10) are measured when those stages exist. They are not part of the
  offline gate. Until a target is measured, it is "not measured". It never
  counts as passed.

MAE alone hides large errors on expensive stones. Every evaluation also
reports MAE for diamonds priced above 10,000 USD, with the number of rows in
that group. No target yet: we record it first, then set a target once we
have a baseline.

## 3. What can go wrong in production?

| Risk | Example | How we will catch it | Week |
|---|---|---|---|
| Bad input data | A listing with `x = 0` or `carat = -1` | Schema validation rejects it | 3, 6 |
| Training data changes without a record | Someone edits `diamonds.csv`. Nobody can say which data trained the model | Data versioning ties each model to a data hash | 3, 4 |
| Results cannot be reproduced | A newer scikit-learn changes MAE from 279.29 to 278.16 | Pinned, hash-locked dependencies | 0, 2 |
| A worse model is released | A retrain on bad data scores higher error | Quality gate in the pipeline and in CI | 5, 9 |
| The market moves (data drift) | Buyers shift to larger stones. Inputs no longer look like the training data | Drift report on recent inputs | 11 |
| The model gets worse (concept drift) | Prices change, so the same features now mean a different price | Live error once real sale prices arrive | 12 |
| Service is down or slow | The API times out while a seller fills in the form | Health check, latency and error metrics, alerts | 6, 8, 11 |
| Cost runs away | A loop calls the API 1 million times | AWS budget alert, rate limits | 0, 10 |

## 4. Where does the project sit on the maturity model today?

We use the 5-level maturity model (Level 0 to Level 4).

| Level | Name | Diamond project |
|---|---|---|
| 0 | No MLOps | **Today.** One notebook, run by hand. No model tests, no run tracking, no deployment |
| 1 | DevOps but no MLOps | After Weeks 2 and 3: Git workflow, tests, versioned data |
| 2 | Automated training | After Weeks 4 and 5: tracked runs, registry, a pipeline that trains by itself |
| 3 | Automated model deployment | After Weeks 6 to 10: API, container, CI/CD to AWS |
| 4 | Full MLOps automated operations | After Weeks 11 and 12: monitoring, retraining, and rollback |

**Why Level 0 today**
- The notebook is the only way to train. A person runs it cell by cell.
- The starter has some safeguards: pinned packages, committed data, and a
  setup check that the notebook still gives the expected numbers. Those
  check the environment. They do not test the model code.
- No per-run record of which data version or settings produced which model.
- No way for another program to get a prediction.
- Nobody would notice if the model got worse.

**Next 3 changes, in order**
1. Move the notebook code into a tested Python package with one config file
   (Week 2). Nothing else can be automated until the code runs outside a
   notebook.
2. Version the data and validate it before training (Week 3). Without this,
   no result can be traced to its data.
3. Track every training run and register the best model (Week 4). Without
   this, we cannot prove a new model is better.
