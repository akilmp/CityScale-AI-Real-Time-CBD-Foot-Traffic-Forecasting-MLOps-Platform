from dagster import asset


@asset
def raw_data() -> dict:
    """Fetch raw foot-traffic data."""
    # Placeholder implementation.
    return {"data": "raw"}
