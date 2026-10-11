"""Guards against config/code/artifact drift.

These tests exist because of a real defect: params.yaml named one model,
models/metrics.json named another, and src/ could train neither -- because
train.py read the seed from params.yaml but took the model name from a
hardcoded default. The repo shipped the notebook's artifacts and could not
regenerate them.

Nothing here trains anything, so it runs in CI in under a second. The point
of Module 2 is that "the notebook and the repo agree" is an assertion, not
a promise.
"""

import json

import joblib
import pytest

from diamond.config import METRICS_PATH, MODEL_PATH, load_params
from diamond.train import build_model, candidate_models


def test_build_model_uses_configured_seed():
    params = load_params()
    model = build_model(params["model"]["name"], params["seed"], params["model"]["params"])
    assert model.random_state == params["seed"]


def test_unknown_model_and_invalid_hyperparameter_fail():
    with pytest.raises(KeyError, match="Unknown model"):
        build_model("DoesNotExist", 42)
    with pytest.raises(ValueError, match="Invalid parameter"):
        build_model("HistGradientBoosting", 42, {"n_estimators": 10})


def test_missing_config_fails_instead_of_silently_using_defaults(tmp_path, monkeypatch):
    from diamond import config

    monkeypatch.setattr(config, "PROJECT_ROOT", tmp_path)
    with pytest.raises(FileNotFoundError):
        config.load_params()


def test_configured_model_exists_in_roster():
    """params.yaml cannot name a model the code is unable to build."""
    name = load_params()["model"]["name"]
    assert name in candidate_models(
        seed=42
    ), f"params.yaml model.name={name!r} is not in candidate_models()"


def test_configured_hyperparameters_are_valid_for_that_model():
    """Catches the n_estimators-vs-max_iter class of error at test time
    rather than halfway through a training run."""
    cfg = load_params()["model"]
    model = build_model(cfg["name"], seed=42, hyperparams=cfg.get("params"))
    for key, value in (cfg.get("params") or {}).items():
        assert model.get_params()[key] == value


@pytest.mark.skipif(not MODEL_PATH.exists(), reason="no trained artifact present")
def test_saved_artifact_is_the_configured_model():
    """The shipped .joblib must be the model params.yaml describes."""
    from diamond.evaluate import _model_name

    configured = load_params()["model"]["name"]
    pipe = joblib.load(MODEL_PATH)
    assert _model_name(pipe) == configured
    params = load_params()
    assert pipe.named_steps["model"].random_state == params["seed"]
    for key, value in params["model"]["params"].items():
        assert pipe.named_steps["model"].get_params()[key] == value


@pytest.mark.skipif(not METRICS_PATH.exists(), reason="no metrics present")
def test_metrics_describe_the_configured_model():
    """metrics.json must not claim a model the repo does not train."""
    from diamond.data import load_raw
    from diamond.preprocess import clean, split

    metrics = json.loads(METRICS_PATH.read_text())
    assert metrics["model"] == load_params()["model"]["name"]
    assert metrics["seed"] == load_params()["seed"]
    assert metrics["n_test"] == len(split(clean(load_raw()))[3])
