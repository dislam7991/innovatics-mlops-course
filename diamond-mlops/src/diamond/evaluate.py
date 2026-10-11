"""Evaluation entry point -- metrics on the held-out test set.

Notebook equivalent: the evaluation cell, but fixed to evaluate on a TRUE holdout
(the notebook's original version leaked by scoring on training rows).

    python -m diamond.evaluate

Writes models/metrics.json. Three things this reports that a bare score does not,
and that Module 11 (monitoring) builds on:

  * which model produced the numbers -- read off the saved artifact itself, not
    from config, so metrics.json can never disagree with the shipped pipeline;
  * a LinearRegression baseline scored on the same split, so "R^2 = 0.98" is
    always readable next to what a trivial model gets;
  * the seed and test-set size, so a run is reproducible from the file alone.
"""

from __future__ import annotations

import json

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from .config import METRICS_PATH, MODEL_PATH, load_params
from .data import load_raw
from .preprocess import build_preprocessor, clean, split
from .train import candidate_models


def _score(y_true, preds) -> dict:
    return {
        "mae": float(mean_absolute_error(y_true, preds)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, preds))),
        "r2": float(r2_score(y_true, preds)),
    }


def _model_name(pipe: Pipeline) -> str:
    """Report what is actually in the artifact, using the same names as
    params.yaml and the bake-off roster.

    Deliberately a reverse lookup against candidate_models() rather than string
    surgery on the class name: sklearn's class names do not match our roster
    keys (KNN is KNeighborsRegressor, XGBoost is XGBRegressor), so stripping a
    'Regressor' suffix would silently emit a name params.yaml can never match.
    """
    estimator_type = type(pipe.named_steps["model"])
    for name, candidate in candidate_models(seed=0).items():
        if type(candidate) is estimator_type:
            return name
    return estimator_type.__name__  # unknown estimator: report it honestly


def evaluate() -> dict:
    params = load_params()
    pipe = joblib.load(MODEL_PATH)
    df = clean(load_raw())
    X_train, X_test, y_train, y_test = split(df)

    metrics = {"model": _model_name(pipe)}
    # TODO M02: score pipe on the holdout and update metrics, then remove this exception.
    raise NotImplementedError("TODO M02: add holdout scores to metrics")

    # Baseline: the simplest defensible model, same preprocessing, same split.
    baseline = Pipeline([("prep", build_preprocessor()), ("model", LinearRegression())])
    baseline.fit(X_train, y_train)
    metrics["baseline"] = {"model": "LinearRegression"}
    metrics["baseline"].update(_score(y_test, baseline.predict(X_test)))

    metrics["n_test"] = int(len(y_test))
    metrics["seed"] = params["seed"]

    # Week 1's problem framing asks us to expose errors on expensive stones.
    high_value = y_test > 10_000
    metrics["above_10000_usd"] = {"n_test": int(high_value.sum()), "mae": None}
    if high_value.any():
        metrics["above_10000_usd"]["mae"] = float(
            mean_absolute_error(y_test[high_value], pipe.predict(X_test.loc[high_value]))
        )

    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    print("Holdout metrics:", json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    evaluate()
