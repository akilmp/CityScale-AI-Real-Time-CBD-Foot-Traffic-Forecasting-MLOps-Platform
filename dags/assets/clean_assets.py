"""Cleaning and transformation Dagster assets."""

import pandas as pd
from dagster import asset


@asset
def clean_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw foot-traffic data.

    The transformation performs a very small set of common cleaning steps:

    * Drop rows containing missing values.
    * Convert a ``timestamp`` column to ``datetime`` if present.
    """

    df = raw_data.dropna().reset_index(drop=True)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df
