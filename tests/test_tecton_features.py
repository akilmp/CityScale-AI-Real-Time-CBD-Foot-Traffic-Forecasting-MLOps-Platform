import pandas as pd

from dags.assets.tecton_features import TectonClient, compute_tecton_features


def test_tecton_features_pipeline():
    """Ensure feature engineering computes expected values."""
    data = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2023-01-01 00:00", "2023-01-01 01:00", "2023-01-02 00:00"]
            ),
            "cbd_id": 1,
            "count": [1, 2, 3],
            "temperature": [10.0, 11.0, 12.0],
            "attendance": [100, 0, 50],
        }
    )

    client = TectonClient()
    features = compute_tecton_features(data, client)

    assert list(features.columns) == [
        "cbd_id",
        "timestamp",
        "rolling_1h_count",
        "rolling_24h_count",
        "temp_lag_1h",
        "event_attendance",
        "is_holiday",
    ]

    # Rolling counts of "count"
    assert features["rolling_1h_count"].tolist() == [1.0, 3.0, 3.0]
    assert features["rolling_24h_count"].tolist() == [1.0, 3.0, 6.0]

    # Weather lag
    assert pd.isna(features["temp_lag_1h"].iloc[0])
    assert features["temp_lag_1h"].iloc[1] == 10.0
    assert features["temp_lag_1h"].iloc[2] == 11.0

    # Event attendance aggregation
    assert features["event_attendance"].tolist() == [100.0, 100.0, 150.0]

    # Holiday flag: first timestamp is a holiday/weekend
    assert bool(features["is_holiday"].iloc[0]) is True
    assert features["is_holiday"].dtype == bool

    # The Tecton client should receive the produced features
    pd.testing.assert_frame_equal(client.last_pushed, features)
