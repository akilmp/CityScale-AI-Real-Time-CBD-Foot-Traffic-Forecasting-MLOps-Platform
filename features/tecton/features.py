"""Tecton feature definitions for the foot traffic forecasting project."""

from datetime import timedelta

try:
    from tecton import (
        Aggregation,
        Entity,
        Field,
        FileConfig,
        batch_feature_view,
        batch_source,
    )
except Exception:  # pragma: no cover - Tecton may not be installed
    Aggregation = Entity = Field = FileConfig = batch_feature_view = batch_source = None  # type: ignore

# Entities
cbd = Entity(name="cbd", join_keys=["cbd_id"], description="Central business district identifier")  # type: ignore

# Data sources ---------------------------------------------------------------------------
# These sources are placeholders and should be updated with real data connectors.
foot_traffic_source = batch_source(  # type: ignore
    name="foot_traffic_source",
    batch_config=FileConfig(
        uri="s3://placeholder/foot_traffic/*.parquet",
        file_format="parquet",
    ),
    timestamp_field="timestamp",
)

weather_source = batch_source(  # type: ignore
    name="weather_source",
    batch_config=FileConfig(
        uri="s3://placeholder/weather/*.parquet",
        file_format="parquet",
    ),
    timestamp_field="timestamp",
)

events_source = batch_source(  # type: ignore
    name="events_source",
    batch_config=FileConfig(
        uri="s3://placeholder/events/*.parquet",
        file_format="parquet",
    ),
    timestamp_field="event_time",
)

holidays_source = batch_source(  # type: ignore
    name="holidays_source",
    batch_config=FileConfig(
        uri="s3://placeholder/holidays/*.parquet",
        file_format="parquet",
    ),
    timestamp_field="date",
)

# Feature views -------------------------------------------------------------------------

@batch_feature_view(  # type: ignore
    sources=[foot_traffic_source],
    entities=[cbd],
    mode="spark_sql",
    online=True,
    offline=True,
    ttl=timedelta(days=7),
    features=[
        Field(name="rolling_1h_count", dtype="int64"),
        Field(name="rolling_24h_count", dtype="int64"),
    ],
    aggregations=[
        Aggregation(
            column="count",
            function="sum",
            time_window=timedelta(hours=1),
            sliding_window=timedelta(hours=1),
            name="rolling_1h_count",
        ),
        Aggregation(
            column="count",
            function="sum",
            time_window=timedelta(hours=24),
            sliding_window=timedelta(hours=1),
            name="rolling_24h_count",
        ),
    ],
)
def foot_traffic_rolling_counts(foot_traffic):
    """Rolling 1h and 24h counts of foot traffic events."""
    return foot_traffic


@batch_feature_view(  # type: ignore
    sources=[weather_source],
    entities=[cbd],
    mode="spark_sql",
    online=True,
    offline=True,
    ttl=timedelta(days=7),
    features=[Field(name="temp_lag_1h", dtype="float64")],
)
def weather_lag(weather):
    """One hour lag of temperature readings."""
    return f"""
        SELECT
            cbd_id,
            timestamp,
            LAG(temperature, 1) OVER (PARTITION BY cbd_id ORDER BY timestamp) AS temp_lag_1h
        FROM {weather}
    """


@batch_feature_view(  # type: ignore
    sources=[events_source],
    entities=[cbd],
    mode="spark_sql",
    online=True,
    offline=True,
    ttl=timedelta(days=30),
    features=[Field(name="event_attendance", dtype="int64")],
    aggregations=[
        Aggregation(
            column="attendance",
            function="sum",
            time_window=timedelta(days=1),
            sliding_window=timedelta(days=1),
            name="event_attendance",
        )
    ],
)
def event_attendance(events):
    """Aggregate attendance for events in the previous day."""
    return events


@batch_feature_view(  # type: ignore
    sources=[holidays_source],
    entities=[cbd],
    mode="spark_sql",
    online=True,
    offline=True,
    ttl=timedelta(days=365),
    features=[Field(name="is_holiday", dtype="bool")],
)
def holiday_flag(holidays):
    """Boolean flag indicating whether the date is a public holiday."""
    return f"""
        SELECT
            cbd_id,
            date AS timestamp,
            TRUE AS is_holiday
        FROM {holidays}
    """
