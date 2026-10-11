"""Central configuration — paths, column definitions, and hyperparameters.

Everything the notebook hardcoded inline lives here instead, loaded from params.yaml
where possible. This is one of the core notebook -> production changes.
"""

from __future__ import annotations

from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw" / "diamonds.csv"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "diamond_pipeline.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

TARGET = "price"

# Ordinal features MUST be encoded in quality order (worst -> best), not alphabetically.
# This is a correctness detail the notebook makes explicit.
ORDINAL_FEATURES = {
    "cut": ["Fair", "Good", "Very Good", "Premium", "Ideal"],
    "color": ["J", "I", "H", "G", "F", "E", "D"],
    "clarity": ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"],
}
NUMERIC_FEATURES = ["carat", "depth", "table", "x", "y", "z"]


def load_params() -> dict:
    """Load params.yaml (seed, test_size, model hyperparameters)."""
    path = PROJECT_ROOT / "params.yaml"
    with path.open() as f:
        return yaml.safe_load(f)
