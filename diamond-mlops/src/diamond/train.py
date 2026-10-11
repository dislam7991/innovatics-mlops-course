"""Training entry point.

Notebook equivalent: the model bake-off + tuning + finalize cells. Here it is a
parameterized, rerunnable script with a CLI:

    python -m diamond.train              # train the model configured in params.yaml
    python -m diamond.train --bakeoff    # cross-validated model comparison
    python -m diamond.train --model Ridge   # override params.yaml for one run

The bake-off mirrors the notebook's exploration; the default path trains the
single chosen model for production.

Two rules this module follows, and that Module 2 teaches:
  1. No model name or hyperparameter is hardcoded here. params.yaml is the
     single source of truth; the CLI can override it for a one-off run.
  2. The estimator that ships is the one the notebook selected -- currently
     HistGradientBoosting (max_iter=400, learning_rate=0.05, max_depth=None).
     Running this script reproduces models/metrics.json exactly.
"""

from __future__ import annotations

import argparse

import joblib
from sklearn.ensemble import (
    GradientBoostingRegressor,
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor

from .config import MODEL_DIR, MODEL_PATH, load_params
from .data import load_raw
from .preprocess import build_preprocessor, clean, split


def candidate_models(seed: int) -> dict:
    """Notebook comparison roster. build_model applies configured hyperparameters."""
    models = {
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(random_state=seed),
        "DecisionTree": DecisionTreeRegressor(random_state=seed),
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=seed, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(random_state=seed),
        # Histogram-based GBM: fast on 50k+ rows, and serializes to <1 MB where
        # an equivalent RandomForest hit 684 MB. This is the notebook's winner.
        "HistGradientBoosting": HistGradientBoostingRegressor(random_state=seed),
        "KNN": KNeighborsRegressor(),
    }
    try:  # XGBoost is optional; include it if installed
        from xgboost import XGBRegressor

        models["XGBoost"] = XGBRegressor(random_state=seed, n_jobs=-1, verbosity=0)
    except ImportError:
        pass
    return models


def build_model(name: str, seed: int, hyperparams: dict | None = None):
    """Instantiate one candidate and apply its configured hyperparameters."""
    roster = candidate_models(seed)
    if name not in roster:
        raise KeyError(
            f"Unknown model {name!r}. params.yaml model.name must be one of: "
            + ", ".join(sorted(roster))
        )
    model = roster[name]
    if hyperparams:
        model.set_params(**hyperparams)
    return model


def make_pipeline(model) -> Pipeline:
    return Pipeline([("prep", build_preprocessor()), ("model", model)])


def bakeoff(X, y, seed: int) -> None:
    print("Cross-validated bake-off (neg RMSE, 3-fold):")
    for name, model in candidate_models(seed).items():
        pipe = make_pipeline(model)
        scores = cross_val_score(pipe, X, y, cv=3, scoring="neg_root_mean_squared_error", n_jobs=-1)
        print(f"  {name:22s} RMSE = {-scores.mean():8.2f}  (+/- {scores.std():.2f})")


def train(model_name: str | None = None) -> Pipeline:
    """Train the configured model on the training split and save the pipeline.

    model_name=None means 'use params.yaml' -- the normal path.
    """
    params = load_params()
    seed = params["seed"]
    model_cfg = params.get("model", {}) or {}
    name = model_name or model_cfg.get("name")
    if not name:
        raise KeyError("No model configured: set model.name in params.yaml or pass --model.")
    # Hyperparameters only apply when training the model params.yaml describes.
    hyperparams = model_cfg.get("params") if name == model_cfg.get("name") else None

    df = clean(load_raw())
    # Training never touches the holdout; evaluate.py re-derives it from the same seed.
    X_train, _, y_train, _ = split(df)
    pipe = make_pipeline(build_model(name, seed, hyperparams))
    # TODO M02: fit pipe on X_train and y_train, then remove this exception.
    raise NotImplementedError("TODO M02: fit the training pipeline")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    shown = hyperparams or "library defaults"
    print(f"Trained {name} ({shown}) on {len(X_train):,} rows -> {MODEL_PATH}")
    return pipe


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bakeoff", action="store_true", help="run cross-validated model comparison")
    ap.add_argument("--model", default=None, help="override params.yaml model.name for this run")
    args = ap.parse_args()
    if args.bakeoff:
        p = load_params()
        d = clean(load_raw())
        Xtr, Xte, ytr, yte = split(d)
        bakeoff(Xtr, ytr, p["seed"])
    else:
        train(args.model)
