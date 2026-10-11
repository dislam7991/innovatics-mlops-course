PYTHON = .venv/bin/python
# Limit parallelism for predictable laptop memory use, as in Week 0.
export OMP_NUM_THREADS = 1
export OPENBLAS_NUM_THREADS = 1
export MKL_NUM_THREADS = 1
export LOKY_MAX_CPU_COUNT = 2

.PHONY: install train evaluate test lint format hooks predict
install:
	python3.12 -m venv .venv
	$(PYTHON) -m pip install --require-hashes -r requirements.txt
	$(PYTHON) -m pip install --no-deps --no-build-isolation -e .
	$(PYTHON) -m pip check

# A training run includes holdout evaluation so each run produces metrics.json.
train:
	$(PYTHON) -m diamond.train
	$(PYTHON) -m diamond.evaluate

evaluate:
	$(PYTHON) -m diamond.evaluate

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests
	$(PYTHON) -m black --check src tests

format:
	$(PYTHON) -m ruff check --fix src tests
	$(PYTHON) -m black src tests

hooks:
	cd .. && diamond-mlops/.venv/bin/pre-commit install --config diamond-mlops/.pre-commit-config.yaml

predict:
	$(PYTHON) -m diamond.predict '$(RECORD)'
