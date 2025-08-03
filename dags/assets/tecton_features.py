"""Feature engineering and pushing to Tecton."""

from __future__ import annotations

import pandas as pd
from dagster import ConfigurableResource, asset
from pydantic import PrivateAttr

try:  # pragma: no cover - optional dependency
    from tecton import TectonClient as _TectonSDKClient
except Exception:  # pragma: no cover - the SDK is not required for tests
    _TectonSDKClient = None  # type: ignore


class TectonClient(ConfigurableResource):
    """Thin wrapper around the Tecton SDK.

    The resource attempts to use Tecton's Python SDK when available.  When the
    SDK is missing (such as in unit tests or offline environments) the
    ``push_features`` method stores the dataframe on ``last_pushed`` for
    inspection.  This provides a documented mock interface that mimics the
    side–effects of sending data to Tecton without requiring external
    connectivity.
    """

    api_key: str | None = None
    workspace: str | None = None
    _last_pushed: pd.DataFrame | None = PrivateAttr(default=None)

    @property
    def last_pushed(self) -> pd.DataFrame | None:
        """Return the most recently pushed features when using the mock interface."""
        return self._last_pushed

    def push_features(self, features: pd.DataFrame) -> None:  # pragma: no cover - side effect
        """Push a features dataframe to Tecton or store it locally.

        Parameters
        ----------
        features:
            The features to push.  When the Tecton SDK is available this method
            forwards the call to ``tecton.TectonClient.push_features``.  When the
            SDK is not installed the dataframe is saved to ``self.last_pushed``
            for later inspection.
        """

        if _TectonSDKClient is not None:
            client = _TectonSDKClient(api_key=self.api_key, workspace=self.workspace)
            client.push_features(features)
        else:  # pragma: no cover - simple mock behaviour
            # Store the dataframe so tests can assert on its contents.
            self._last_pushed = features.copy()


def compute_tecton_features(clean_data: pd.DataFrame, tecton: TectonClient) -> pd.DataFrame:
    """Generate and push features derived from the cleaned data.

    The input ``clean_data`` is expected to contain the following columns:

    ``timestamp``
        ``datetime64`` index of the observation.
    ``cbd_id``
        Identifier for the central business district.
    ``count``
        Foot traffic counts for the observation window.
    ``temperature``
        Ambient temperature at the timestamp.
    ``attendance``
        Attendance for any events occurring at the timestamp.
    """

    df = clean_data.copy().sort_values(["cbd_id", "timestamp"])  # ensure ordering

    # Rolling counts of foot traffic.
    df["rolling_1h_count"] = (
        df.groupby("cbd_id")
        .rolling("1h", on="timestamp", closed="both")["count"]
        .sum()
        .reset_index(level=0, drop=True)
        .reset_index(drop=True)
    )
    df["rolling_24h_count"] = (
        df.groupby("cbd_id")
        .rolling("24h", on="timestamp", closed="both")["count"]
        .sum()
        .reset_index(level=0, drop=True)
        .reset_index(drop=True)
    )

    # One hour lag of temperature readings.
    df["temp_lag_1h"] = df.groupby("cbd_id")["temperature"].shift(1)

    # Aggregate event attendance over the previous day.
    df["event_attendance"] = (
        df.groupby("cbd_id")
        .rolling("1D", on="timestamp", closed="both")["attendance"]
        .sum()
        .reset_index(level=0, drop=True)
        .reset_index(drop=True)
    )

    # Public holiday flag.
    try:  # pragma: no cover - optional dependency
        import holidays

        us_holidays = holidays.US()
        df["is_holiday"] = df["timestamp"].dt.date.isin(us_holidays)
    except Exception:  # pragma: no cover - fallback when library unavailable
        # Fall back to marking weekends as holidays when the package is missing.
        df["is_holiday"] = df["timestamp"].dt.dayofweek >= 5

    feature_cols = [
        "cbd_id",
        "timestamp",
        "rolling_1h_count",
        "rolling_24h_count",
        "temp_lag_1h",
        "event_attendance",
        "is_holiday",
    ]

    features = df[feature_cols]
    tecton.push_features(features)
    return features


@asset
def tecton_features(clean_data: pd.DataFrame, tecton: TectonClient) -> pd.DataFrame:
    """Dagster asset wrapper around :func:`compute_tecton_features`."""

    return compute_tecton_features(clean_data, tecton)
