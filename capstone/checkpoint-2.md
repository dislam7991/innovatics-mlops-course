---
item: P-07 (Capstone package)
title: "Checkpoint 2: Automated delivery to the cloud"
due: end of Week 10
covers: Weeks 6 to 10
solution_tag: m10
grading: 10% of the course grade (the 2 checkpoints are 20% together)
source: CURRICULUM.md section 3 and "Checkpoint 2" in Week 10 (2026-10-22); diamond-mlops/README.md, Makefile, infra/, scripts/ and .github/workflows/ at the M10-CODE merge commit 2d3b4e7 (tag m10)
---

# Checkpoint 2: Automated delivery to the cloud

## Goal

Weeks 6 to 10 took the trained model to users. Checkpoint 2 asks one question: **does a change reach production only when it is good, and can you undo it?**

You submit your diamond project as it stands after Week 10. A reviewer reads your pull requests, your GitHub Actions runs and your screenshots. Then, in a short live walkthrough, you call your live URL, explain the rollback, and destroy the infrastructure.

There is no new dataset and no new tool. This checkpoint checks that the Week 6 to 10 parts work **together**: CI, the gate, CD, ECR, Lambda and Terraform.

## What the reviewer must see

| # | The reviewer sees | Week |
|---|---|---|
| 1 | A pull request with a **bad code change** is blocked: `check` is red, and the ruleset disables the merge | 2, 9 |
| 2 | A pull request with a **worse model** is blocked: `check` is green, `model` is red at the `Quality gate` step, and the "Diamond quality gate: FAIL" comment names the reasons | 4, 9 |
| 3 | A **good merge** to `main` runs Diamond CI, then Diamond CD. CD builds the image, pushes it to ECR, deploys the release image to Lambda by digest, and checks `/health` | 7, 9, 10 |
| 4 | The infrastructure comes from `infra/`. `terraform plan` shows `No changes.` after the apply. Every resource carries the tag `project=diamond-mlops` | 10 |
| 5 | In the walkthrough, the live function URL answers `/health` and returns a price from `/predict` | 6, 10 |
| 6 | Screenshot (d): the previous image is restored once with `scripts/deploy_lambda.sh`, and then the latest image again | 10 |
| 7 | `terraform destroy` removes everything. The tag search lists nothing | 10 |
| 8 | Pass/fail, required: the Week 8 manifests are in `k8s/`, and `tests/test_k8s_manifests.py` passes in `check` | 8 |

These commands come from `diamond-mlops/Makefile`, `README.md` and `modules/m10-cloud-iac/walkthrough.md` at tag `m10`. Your project must still support them, or your README must name the commands that replace them:

| Command | What it does |
|---|---|
| `make test` | Runs the tests, including the Kubernetes manifest checks |
| `make gate` | Runs the CI quality gate locally. Exit 0 passes, exit 1 blocks |
| `make tf-check` | Terraform format, validate, and tests on a mocked provider. No AWS needed |
| `make image && make lambda-release` | Builds the API image, then the release image for Lambda |
| `make lambda-check` | Runs the release image under the Lambda emulator and calls it |
| `bash scripts/deploy_lambda.sh <function> <image>` | Points Lambda at one image by digest and checks `/health`. It prints the rollback command first |
| `terraform -chdir=infra plan` | Shows what Terraform would change. After an apply: `No changes.` |
| `terraform -chdir=infra destroy` | Removes every resource, the images and the bucket contents included |

## What to submit

Submit the way your instructor asks, before the end of Week 10:

1. **A Git tag named `checkpoint-2`** on the commit you want graded, pushed to your fork. Commits after the tag are not graded.
2. **Links to two blocked pull requests.** Leave both open, and do not merge them.
   - Bad code: a change that breaks a test or the lint, for example a wrong expected value in one test.
   - Worse model: in `params.yaml`, change `max_iter: 400` to `max_iter: 20`, as in Practical 9.
3. **A link to one green Diamond CD run** from a good merge. Its last step prints `Deployed ...@sha256:...` and the `/health` answer.
4. **A README section "Checkpoint 2: delivery and rollback".** The commands in order, as in M10 walkthrough sections 7 to 10: the first apply (no `image_uri`), the first release push, the second apply with that digest in `image_uri`, the GitHub variables and secrets by name (never their values), the deploy, the rollback, and the destroy.
5. **5 screenshots**:
   (a) the ruleset with the required checks `check`, `model` and `infra`;
   (b) the `production` approval on the CD run;
   (c) the terminal with `terraform plan` showing `No changes.`, and the `curl` of `/predict` returning a price;
   (d) the terminal with the two `deploy_lambda.sh` runs of the rollback and the return, each with its `Deployed` line;
   (e) the terminal with `terraform destroy` complete and an empty tag search.
   Take all five on one day, and run the destroy of (e) that same day. Your function URL is public while it exists, and nothing caps what its calls cost.

Create the tag from the root of your fork, on your final commit:

```bash
git tag checkpoint-2
git push origin checkpoint-2
```

Never put AWS keys or `infra/terraform.tfvars` in a commit or a screenshot.

## The live walkthrough (10 minutes)

At a time your instructor gives you, in the week after Week 10. Build the stack again just before it, with the first three steps of your README section: apply, push the release image, apply with its digest. Destroy it at the end of the walkthrough.

- Open the worse-model pull request. Say which gate rule failed and why the merge button is disabled.
- Open the green CD run. Say what each step does, and where the model version comes from.
- Call your live URL: `/health`, then `/predict`.
- Show screenshot (d). Say where the rollback command comes from and what it changes in Lambda.
- Answer one question about a design choice. Example: "Why does CD deploy by digest, and not by tag?"
- Run `terraform -chdir=infra destroy`, then the tag search:

```bash
aws resourcegroupstaggingapi get-resources --tag-filters Key=project,Values=diamond-mlops --region us-east-1
```

The search should list nothing, or only resources that AWS is still deleting. Use your own region if it is not `us-east-1`.

The AI-use policy applies. You may use AI tools. You must explain and change your own code.

## Rubric

Total: 100 points. The weights come from CURRICULUM.md, Week 10.

| Criterion | Full points | Part points | 0 points |
|---|---|---|---|
| 1. CI blocks a bad change and a worse model (30) | Both pull requests are blocked by a red required check. The worse model fails at `Quality gate`, with the FAIL comment | 15: only one of the two is blocked, or the checks are red but the merge is not blocked by a ruleset | Nothing is blocked |
| 2. CD builds, pushes and deploys on merge (25) | One CD run, started by the merge, approved in `production` (a private fork: no approval needed), deploys by digest. `/health` reports the champion's model version | 13: the image reaches ECR, but the deploy is manual or fails | No CD run |
| 3. Infrastructure fully in Terraform and destroyable (20) | Every resource of the Week 10 stack is in `infra/`: the bucket, the ECR repository, the role, the log group, the function, its URL and the deploy policy. The Week 9 IAM user and the Week 0 budget alert are made outside the stack, and do not count. `plan` shows no changes after the apply. `destroy` and an empty tag search are shown | 10: a stack resource was made by hand, or the destroy is not shown | No Terraform |
| 4. Previous version restored (10) | Screenshot (d) shows the rollback and the return to the latest image. In the walkthrough, you explain the rollback command | 5: the rollback is shown, but the latest image is not restored, or you cannot explain it | No rollback |
| 5. Live walkthrough (15) | Clear explanation. Good answer to the design question. The rebuilt stack answers the live calls, and the destroy works | 8: clear explanation, but a live step fails | No walkthrough, or you cannot explain your code |
| Kubernetes manifests (pass/fail, required) | `k8s/` holds the Week 8 manifests, and `tests/test_k8s_manifests.py` passes in `check` | | Missing or failing: the checkpoint is not graded until it is fixed |

A private fork cannot set the ruleset or the `production` reviewer on GitHub Free. Then criterion 1 earns full points if the red checks and the FAIL comment are shown. Skip screenshots (a) and (b); criterion 2 earns full points without the approval. Note it in your submission.

## Common problems

| Problem | Likely cause | Fix |
|---|---|---|
| The CD run is skipped | The repository variable `ECR_REPOSITORY` is missing, or CI on `main` was not green | Set the variable. Merge again after a green CI run |
| CD stops after the API image | The repository variable `LAMBDA_FUNCTION` is missing | Set `AWS_REGION`, `MODEL_BUCKET` and `LAMBDA_FUNCTION` from `terraform output` |
| `fetch_release.sh` refuses the export | The export in S3 is from another tracking store than `models/champion.json` | Repeat walkthrough section 8 in order: train and register, bundle, upload, commit the record |
| `/health` reports the wrong model version | The release image was built from an older export | Fetch the export again, rebuild, and deploy |
| `terraform plan` wants to destroy the function | `infra/terraform.tfvars` with `image_uri` is missing | Restore the file. Keep it out of Git |
| The first `curl` takes about 10 seconds | A cold start | Call again. The next calls are fast |
| The merge button is enabled on a red pull request | The checks are not in the ruleset, or the fork is private | Add `check`, `model` and `infra` as required checks |
| The first `terraform apply` fails: the ECR repository already exists | The Week 7 repository was made by hand, outside Terraform | Delete it first, as in walkthrough section 7, then apply again |
