from dagster import asset


@asset
def clean_data(raw_data: dict) -> dict:
    """Clean the raw foot-traffic data."""
    # Placeholder cleaning step.
    return raw_data
