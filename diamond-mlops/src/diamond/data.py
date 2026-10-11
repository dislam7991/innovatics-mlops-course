"""Data ingestion and loading.

Notebook equivalent: the 'Load the diamond dataset' cell. The difference: this
reads from a versioned local file (data/raw/diamonds.csv) instead of a network
fetch, so runs are reproducible and DVC-trackable.
"""

from __future__ import annotations

import pandas as pd

from .config import DATA_RAW


def load_raw() -> pd.DataFrame:
    """Load the raw diamonds dataset from the versioned CSV."""
    if not DATA_RAW.exists():
        raise FileNotFoundError(
            f"Raw data not found at {DATA_RAW}. "
            "Restore data/raw/diamonds.csv from Git. Week 3 adds DVC."
        )
    return pd.read_csv(DATA_RAW)
