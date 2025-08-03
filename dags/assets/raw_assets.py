"""Dagster assets for ingesting raw data from Airbyte output."""

from pathlib import Path
from typing import List

import pandas as pd
from dagster import ConfigurableResource, asset


class AirbyteOutput(ConfigurableResource):
    """Location of Airbyte's extracted data."""

    base_path: str = "airbyte/output"


@asset
def raw_data(airbyte_output: AirbyteOutput) -> pd.DataFrame:
    """Fetch raw foot-traffic data produced by Airbyte.

    The asset expects Airbyte to dump JSON or CSV files into ``airbyte/output``.
    All files in that directory are concatenated into a single :class:`pandas.DataFrame`.
    """

    output_dir = Path(airbyte_output.base_path)
    if not output_dir.exists():
        raise FileNotFoundError(
            f"Airbyte output directory '{output_dir}' does not exist."
        )

    frames: List[pd.DataFrame] = []
    for file in sorted(output_dir.glob("*")):
        if file.suffix == ".json":
            frames.append(pd.read_json(file))
        elif file.suffix == ".csv":
            frames.append(pd.read_csv(file))

    if not frames:
        raise ValueError(
            f"No Airbyte output files found in '{output_dir}'. Ensure Airbyte has run."
        )

    return pd.concat(frames, ignore_index=True)
