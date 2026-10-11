"""Test the complete saved preprocessing/prediction contract with a tiny model."""

import joblib
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression

from diamond import predict
from diamond.train import make_pipeline


def test_prediction_reloads_the_complete_saved_pipeline(tmp_path, monkeypatch):
    records = pd.DataFrame(
        [
            {
                "carat": 0.2,
                "cut": "Good",
                "color": "E",
                "clarity": "SI1",
                "depth": 60.0,
                "table": 55.0,
                "x": 3.9,
                "y": 4.0,
                "z": 2.4,
            },
            {
                "carat": 0.4,
                "cut": "Ideal",
                "color": "D",
                "clarity": "VS1",
                "depth": 62.0,
                "table": 57.0,
                "x": 4.9,
                "y": 5.0,
                "z": 3.0,
            },
        ]
    )
    pipe = make_pipeline(LinearRegression()).fit(records, [300.0, 800.0])
    artifact = tmp_path / "model.joblib"
    joblib.dump(pipe, artifact)
    monkeypatch.setattr(predict, "MODEL_PATH", artifact)
    monkeypatch.setattr(predict, "_model", None)
    record = records.iloc[0].to_dict()
    assert predict.predict_one(record) == pytest.approx(pipe.predict(records.iloc[:1])[0])
    record.pop("carat")
    with pytest.raises(ValueError, match="columns are missing"):
        predict.predict_one(record)
