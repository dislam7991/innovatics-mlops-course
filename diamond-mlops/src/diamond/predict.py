"""Prediction helper — load the trained pipeline and score new records.

Notebook equivalent: the 'load model and predict' cell. Used by the API layer.
"""

from __future__ import annotations

import argparse
import json

import joblib
import pandas as pd

from .config import MODEL_PATH

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_one(record: dict) -> float:
    """Predict the price for a single diamond given a feature dict."""
    df = pd.DataFrame([record])
    return float(_get_model().predict(df)[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict a price from a JSON feature record.")
    parser.add_argument("record", help="JSON object with the nine diamond features")
    args = parser.parse_args()
    print(json.dumps({"prediction": predict_one(json.loads(args.record))}))
