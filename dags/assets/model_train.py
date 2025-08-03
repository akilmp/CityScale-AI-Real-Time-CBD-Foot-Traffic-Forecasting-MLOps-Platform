from dagster import asset


@asset
def trained_model(tecton_features: dict) -> dict:
    """Train a model using the provided features."""
    # Placeholder model training.
    return {"model": "trained"}
