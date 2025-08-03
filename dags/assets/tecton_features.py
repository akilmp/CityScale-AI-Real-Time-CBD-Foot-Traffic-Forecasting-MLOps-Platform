"""Feature engineering and pushing to Tecton."""

import pandas as pd
from dagster import ConfigurableResource, asset


class TectonClient(ConfigurableResource):
    """Minimal Tecton client placeholder.

    In a real deployment this would wrap ``tecton``'s SDK.  For this exercise the
    ``push_features`` method simply acts as a stub so the asset can be executed
    without external dependencies.
    """

    api_key: str | None = None

    def push_features(self, features: pd.DataFrame) -> None:  # pragma: no cover - side effect
        """Pretend to push features to the Tecton feature store."""
        # This is where one would interact with the actual Tecton SDK.
        _ = features  # no-op to keep method side-effect free


@asset
def tecton_features(clean_data: pd.DataFrame, tecton: TectonClient) -> pd.DataFrame:
    """Generate and push features derived from the cleaned data."""

    numeric_cols = clean_data.select_dtypes(include="number").columns
    features = clean_data[numeric_cols].copy()
    tecton.push_features(features)
    return features
