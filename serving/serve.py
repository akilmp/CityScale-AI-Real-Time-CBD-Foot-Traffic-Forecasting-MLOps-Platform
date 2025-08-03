from pathlib import Path
import os
import yaml
import whylogs as why

CONFIG_PATH = Path(__file__).resolve().parent.parent / "monitoring" / "whylabs.yaml"
config = yaml.safe_load(CONFIG_PATH.read_text())
logger = why.logger(
    project=config["org_id"],
    dataset_name=config["dataset_id"],
    api_key=os.getenv(config.get("api_key_env", "WHYLABS_API_KEY")),
)


def predict(features):
    """Dummy prediction routine that logs inputs and outputs to WhyLabs."""
    prediction = sum(features)
    with logger.session() as session:
        session.log({"features": features, "prediction": prediction})
    return prediction


if __name__ == "__main__":
    print(predict([1, 2, 3]))
