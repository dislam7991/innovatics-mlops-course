# Diamond Price Prediction: Week 2 starter

This starter provides the package, config, Makefile, pinned environment, hooks,
and CI. Three blocks remain unfinished: `train.train()`, `evaluate.evaluate()`,
and `test_clean_removes_duplicates_without_changing_input()`.

Each block has one `TODO M02` comment and raises `NotImplementedError`. Fill
those blocks before running the full training commands below. `make install`
and `make lint` work immediately. Before you finish, `make test` has one
intentional TODO failure, 10 passes, and two artifact skips. Training fails
before saving a model. The existing config guards must stay in place.

Use Ubuntu in WSL2 on Windows, or a Linux/macOS terminal. Open this folder in
VS Code through Remote-WSL on Windows. Run the commands below inside Linux.

## Install and run the reproducible project (Week 2)

Install Python 3.12 and GNU Make in your Linux environment first. From the course
repository, run:

```bash
cd diamond-mlops
make install
make train
make evaluate
make test
make lint
```

`make install` creates `.venv`, installs the hash-locked dependencies, then installs
this package in editable mode without downloading extra dependencies or build
tools. `pyproject.toml` declares exact direct pins and requires Python 3.12;
`requirements.txt` locks the notebook, package, development tools, and their
dependencies for Linux and macOS. Keep both files when you clone or export.

`make train` fits on the training rows, saves `models/diamond_pipeline.joblib`,
then evaluates the holdout and writes `models/metrics.json`. `make evaluate`
scores the saved pipeline again. It also trains a linear baseline on the same
training split and reports MAE on holdout diamonds above 10,000 USD with the
number of rows in that group. Those are context measurements; Week 9 adds
the release quality gate.

With the committed data and `params.yaml`, expect HistGradientBoosting, seed 42,
10,755 holdout rows, MAE `279.29262903257705`, RMSE `524.9243546483148`, and R2
`0.982563973914643`. A floating-point difference below `1e-9` is acceptable.
Show that two runs are repeatable:

```bash
make train
cp models/metrics.json /tmp/diamond-metrics-first.json
make train
cmp /tmp/diamond-metrics-first.json models/metrics.json
```

`cmp` prints nothing and returns zero when the files match. Models and metrics
are generated outputs ignored by Git. A fresh clone's fast `make test` skips
two artifact checks until you train. After training, those checks also verify
the saved model name, hyperparameters, seed, and metrics against config. The
tests do not require a model to exceed a quality threshold.

The package layout separates responsibilities:

| File | Responsibility |
|---|---|
| `params.yaml` | Seed, split fraction, model choice and hyperparameters |
| `src/diamond/config.py` | Fixed feature schema, paths, config loading |
| `src/diamond/data.py` | Read the local CSV |
| `src/diamond/preprocess.py` | Clean rows, encode quality order, scale, split |
| `src/diamond/train.py` | Build, fit, save the chosen model |
| `src/diamond/evaluate.py` | Score the holdout and linear baseline |
| `src/diamond/predict.py` | Load the saved pipeline and predict a record |
| `tests/test_config_matches_code.py` | Detect config, code and artifact drift |

Change experiments in `params.yaml`, then train and evaluate again. Config is
required; a missing config fails rather than silently using defaults. The
preprocessor is fitted only on training data. The holdout is recreated from
the same cleaned data, split fraction and seed, so keep them unchanged between
training and evaluation. Week 3 adds validation and data versioning.

To predict one record from the shell:

```bash
.venv/bin/python -m diamond.predict '{"carat":0.23,"cut":"Ideal","color":"E","clarity":"SI2","depth":61.5,"table":55.0,"x":3.95,"y":3.98,"z":2.43}'
```

The JSON output contains `prediction` in USD. This is a local helper; the HTTP
service comes in Week 6. Load only model files you trained or trust: joblib
deserialization can execute Python code.

## Code checks and Git hooks

From `diamond-mlops/`, run:

```bash
make format
make lint
make test
make hooks
```

Ruff checks code/imports, Black formats it, and pytest checks behavior. Hooks
use the same locked `.venv` executables as Make, so they do not download another
tool environment. `make hooks` installs the hooks into this Git checkout;
installation is an explicit local step, not a side effect of `make install`.
If a hook edits a file, inspect and stage the fix before committing again.

From the parent course repo, check all tracked files once:

```bash
diamond-mlops/.venv/bin/pre-commit run --all-files --config diamond-mlops/.pre-commit-config.yaml
```

The config's paths target this course repository layout. A future standalone
student export must adjust the hook paths and workflow working directory.
`.github/workflows/checks.yml` runs install, lint and fast tests on pushes and
pull requests with a pinned Python version and immutable action commits. CI
does not train on every push yet; Week 9 adds that pipeline.

## Open the original notebook

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

This revised starter is `start-m02-v2`, built from solution tag `m02`
(`e057569aad5f616359ceb33ac140b0ba1dab4e17`) with three targeted TODOs.
The original `start-m02` branch is at `84b7c2d`. Python 3.11 tags are kept as `archive/`.

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

Week 2 adapts the course's own `sources/diamond-mlops-reference/src/diamond/`,
`params.yaml`, and tests. The model, quality order and split match the notebook.
Extra tests cover duplicate cleaning, input preservation, quality order,
unknown categories, deterministic/disjoint splits, and invalid configuration.
Official [scikit-learn 1.7.2](https://scikit-learn.org/1.7/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html),
[Ruff](https://docs.astral.sh/ruff/configuration/),
[pre-commit](https://pre-commit.com/), and
[GitHub Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
documentation were checked for this stage.
