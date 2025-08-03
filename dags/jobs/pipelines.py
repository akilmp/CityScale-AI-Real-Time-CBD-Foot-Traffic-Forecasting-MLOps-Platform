from dagster import Definitions, ResourceDefinition, define_asset_job, load_assets_from_modules

from dags.assets import clean_assets, model_train, raw_assets, tecton_features
from dags.assets.raw_assets import AirbyteOutput
from dags.assets.tecton_features import TectonClient

# Load all asset definitions from their modules
all_assets = load_assets_from_modules(
    [raw_assets, clean_assets, tecton_features, model_train]
)

# Job chaining the assets together
foot_traffic_pipeline = define_asset_job("foot_traffic_pipeline")

# Definitions used by Dagster to load assets, jobs and resources
defs = Definitions(
    assets=all_assets,
    jobs=[foot_traffic_pipeline],
    resources={
        "airbyte_output": AirbyteOutput(),
        "tecton": TectonClient(),
        "bentoml_model_tag": ResourceDefinition.hardcoded_resource("foot_traffic:latest"),
    },
)

if __name__ == "__main__":
    foot_traffic_pipeline.execute_in_process()
