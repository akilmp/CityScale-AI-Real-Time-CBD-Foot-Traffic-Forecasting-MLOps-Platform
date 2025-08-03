"""Model training Dagster assets."""

import pandas as pd
from dagster import asset
from sklearn.linear_model import LinearRegression


@asset
def trained_model(tecton_features: pd.DataFrame) -> LinearRegression:
    """Train a model using the provided features.

    The final column of ``tecton_features`` is treated as the prediction target
    while all preceding columns serve as features.
    """

    if tecton_features.shape[1] < 2:
        raise ValueError("Expected at least one feature column and one target column")

    X = tecton_features.iloc[:, :-1]
    y = tecton_features.iloc[:, -1]
    model = LinearRegression()
    model.fit(X, y)
    return model
