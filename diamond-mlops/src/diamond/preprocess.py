"""Cleaning, feature preparation, and the sklearn preprocessing pipeline.

Notebook equivalent: the cleaning + 'feature preparation' cells. Key correctness
details made explicit here:
  * rows with x/y/z == 0 are physically impossible (zero-dimension diamond) -> dropped
  * cut/color/clarity are ORDINAL and encoded in quality order (see config)
"""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from .config import NUMERIC_FEATURES, ORDINAL_FEATURES, TARGET, load_params


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop impossible/duplicate rows. Deterministic and side-effect free."""
    df = df.drop_duplicates()
    # x, y, z are physical dimensions in mm; zero means a data error.
    df = df[(df[["x", "y", "z"]] > 0).all(axis=1)]
    return df.reset_index(drop=True)


def build_preprocessor() -> ColumnTransformer:
    """ColumnTransformer: ordinal-encode ordered categoricals, scale numerics."""
    ordinal_cols = list(ORDINAL_FEATURES.keys())
    ordinal_categories = [ORDINAL_FEATURES[c] for c in ordinal_cols]
    return ColumnTransformer(
        transformers=[
            ("ord", OrdinalEncoder(categories=ordinal_categories), ordinal_cols),
            ("num", StandardScaler(), NUMERIC_FEATURES),
        ],
        remainder="drop",
    )


def split(df: pd.DataFrame):
    """Train/test split with a fixed seed (reproducibility)."""
    params = load_params()
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    return train_test_split(X, y, test_size=params["test_size"], random_state=params["seed"])
