from dagster import Definitions, define_asset_job, load_assets_from_modules

from dags.assets import raw_assets, clean_assets, tecton_features, model_train

# Load all asset definitions from their modules
all_assets = load_assets_from_modules(
    [raw_assets, clean_assets, tecton_features, model_train]
)

# Job chaining the assets together
foot_traffic_pipeline = define_asset_job("foot_traffic_pipeline")

# Definitions used by Dagster to load assets and jobs
defs = Definitions(assets=all_assets, jobs=[foot_traffic_pipeline])

if __name__ == "__main__":
    foot_traffic_pipeline.execute_in_process()
