# Diamond Price Prediction

Week 0 starter for the InnovatiCS MLOps Specialization Bootcamp. This folder
contains the original working notebook and its full dataset. Each later module
adds one production practice to the same project.

Use Ubuntu in WSL2 on Windows, or a Linux/macOS terminal. Open this folder in
VS Code through Remote-WSL on Windows. Run the commands below inside Linux.

## Install the notebook environment

From the course repository, enter `diamond-mlops/`:

```bash
cd diamond-mlops
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m jupyterlab
```

Open `notebooks/01_diamond_exploration.ipynb` and select the Python 3 kernel.
Run every cell in order. The notebook reads `data/raw/diamonds.csv`, removes
duplicates and zero dimensions, compares models, and evaluates the winner on
10,755 held-out rows. Keep XGBoost out of this course environment: the notebook's
optional hook can change the winning model if you install it.

The numerical versions are fixed so the notebook and later modules agree.
`requirements.in` lists direct dependencies; `requirements.txt` locks all
resolved dependencies with hashes and platform markers for Python 3.12 on
Linux and macOS. Model files and executed
notebook outputs are generated locally and ignored by Git.

## Verify setup

Install Docker Desktop with WSL2 integration and AWS CLI v2, and configure your
student IAM user as described in the Week 0 practical. **Never create access
keys for the AWS root user.** Set `AWS_PROFILE` if you use a named profile.

From this folder:

```bash
bash scripts/verify_setup.sh
```

The script reports three checks, attempts all of them, and exits nonzero if any
fails:

1. AWS STS returns an IAM user identity. Root and role identities fail the Week 0
   requirement. The script prints the result without displaying account details.
2. Docker runs `hello-world`, pinned by its published image digest, and removes
   the container when it finishes.
3. The notebook executes every cell in this folder's Python 3.12 virtual
   environment. It saves an executed copy in `notebooks/executed/` and checks
   MAE `279.29262903257705`, RMSE `524.9243546483148`, and R2
   `0.982563973914643`, using an absolute tolerance of `1e-9` for floating-point
   differences. Seed 42, HistGradientBoosting, and 10,755 holdout rows must match.

AWS STS only reads identity information; this script creates no AWS resources.
For a notebook-only rerun:

```bash
.venv/bin/python scripts/run_notebook.py
```

If AWS fails, check the CLI installation, profile and credential configuration.
If Docker fails, start Docker Desktop and check WSL integration. If the notebook
fails, read its traceback and reinstall the locked requirements in Python 3.12.
Each notebook cell has a 10-minute timeout; CPU parallelism is limited to keep
laptop memory use predictable.

The local notebook kernel may print `Kernel is running over TCP without
encryption`. This warning is expected during verification; use the final
PASS/FAIL result to check whether the notebook succeeded.

## Project docs

- `docs/problem-framing.md`: who uses the prediction, the targets (metric,
  latency, cost), production risks, and the maturity level today (Week 1).
- `docs/lifecycle.md`: the project's ML lifecycle diagram and how each stage
  maps to a course week (Week 1).

## Course references and provenance

The reviewer publishes solution tag `m00` and starting branch `start-m00` after
this item merges. Both references contain this starter; Week 0 has no code
exercise stubs. Later `start-mXX` branches include that week's TODO files.
Do not publish references to an unreviewed solution commit.

Notebook and CSV copied from the course's read-only
`sources/diamond-mlops-reference/`. Notebook cell source is preserved; saved
outputs and execution counts are cleared. The dataset has 53,940 raw rows.
The original diamonds dataset is distributed with
[ggplot2](https://ggplot2.tidyverse.org/reference/diamonds.html).

API references checked for this implementation:
[AWS STS](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html),
[Docker run](https://docs.docker.com/reference/cli/docker/container/run/),
[nbclient](https://nbclient.readthedocs.io/en/latest/client.html), and
[uv dependency compilation](https://docs.astral.sh/uv/pip/compile/).
