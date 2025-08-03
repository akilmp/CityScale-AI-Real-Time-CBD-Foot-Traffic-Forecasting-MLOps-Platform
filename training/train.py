from pathlib import Path
import os
import yaml
import whylogs as why

CONFIG_PATH = Path(__file__).resolve().parent.parent / "monitoring" / "whylabs.yaml"


def train():
    """Dummy training routine that logs data to WhyLabs."""
    config = yaml.safe_load(CONFIG_PATH.read_text())
    logger = why.logger(
        project=config["org_id"],
        dataset_name=config["dataset_id"],
        api_key=os.getenv(config.get("api_key_env", "WHYLABS_API_KEY")),
    )

    data = {"feature": [1, 2, 3], "target": [0, 1, 0]}
    with logger.session() as session:
        session.log(data)

    print("training complete")


if __name__ == "__main__":
    train()
