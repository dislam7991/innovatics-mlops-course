"""Minimal tests — the notebook had none. This is the 'testable' half of the refactor.

Run with:  make test   (or: pytest -q)
"""

import pandas as pd
import pytest

from diamond.config import ORDINAL_FEATURES
from diamond.preprocess import build_preprocessor, clean, split


def _tiny_df():
    return pd.DataFrame(
        {
            "carat": [0.23, 0.21, 0.23],
            "cut": ["Ideal", "Premium", "Good"],
            "color": ["E", "E", "E"],
            "clarity": ["SI2", "SI1", "VS1"],
            "depth": [61.5, 59.8, 56.9],
            "table": [55.0, 61.0, 65.0],
            "price": [326, 326, 327],
            "x": [3.95, 3.89, 0.0],  # last row has x==0 -> should be dropped
            "y": [3.98, 3.84, 4.07],
            "z": [2.43, 2.31, 2.31],
        }
    )


def test_clean_drops_zero_dimension_rows():
    out = clean(_tiny_df())
    assert len(out) == 2
    assert (out[["x", "y", "z"]] > 0).all().all()


def test_preprocessor_encodes_and_scales():
    df = clean(_tiny_df())
    pre = build_preprocessor()
    X = pre.fit_transform(df.drop(columns=["price"]))
    # 3 ordinal + 6 numeric = 9 output columns
    assert X.shape[1] == len(ORDINAL_FEATURES) + 6


def test_clean_removes_duplicates_without_changing_input():
    original = _tiny_df()
    df = pd.concat([original, original.iloc[:1]], ignore_index=True)
    saved = df.copy(deep=True)
    # TODO M02: assert the cleaned row count, then remove this exception.
    raise NotImplementedError("TODO M02: test duplicate removal")
    pd.testing.assert_frame_equal(df, saved)


def test_quality_order_is_used_and_unknown_categories_fail():
    df = clean(_tiny_df())
    pre = build_preprocessor()
    encoded = pre.fit_transform(df.drop(columns=["price"]))
    # Ideal ranks above Premium even though alphabetical sorting reverses them.
    assert encoded[0, 0] == 4
    assert encoded[1, 0] == 3
    invalid = df.drop(columns=["price"]).copy()
    invalid.loc[0, "cut"] = "UNKNOWN"
    with pytest.raises(ValueError, match="unknown categories"):
        pre.transform(invalid)


def test_split_is_repeatable_disjoint_and_excludes_target():
    df = pd.concat([clean(_tiny_df())] * 10, ignore_index=True)
    first = split(df)
    second = split(df)
    for left, right in zip(first, second, strict=True):
        if isinstance(left, pd.DataFrame):
            pd.testing.assert_frame_equal(left, right)
        else:
            pd.testing.assert_series_equal(left, right)
    X_train, X_test, y_train, y_test = first
    assert "price" not in X_train.columns
    assert len(X_train) == len(y_train) == 16
    assert len(X_test) == len(y_test) == 4
    assert set(X_train.index).isdisjoint(X_test.index)
