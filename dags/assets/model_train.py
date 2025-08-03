"""Model training Dagster assets."""

from dagster import Output, asset
import bentoml
import torch


@asset(required_resource_keys={"bentoml_model_tag"})
def trained_model(context) -> torch.nn.Module:
    """Load the BentoML-registered PyTorch model.

    The model is trained separately in ``train.py`` and saved to BentoML's model
    store. This asset retrieves the latest registered model and emits metadata
    such as the model tag and storage path for downstream evaluation or rollout
    steps.
    """

    tag = context.resources.bentoml_model_tag
    bento_model = bentoml.pytorch.get(tag)
    model = bentoml.pytorch.load_model(bento_model)

    metadata = {
        "bento_model_tag": str(bento_model.tag),
        "bento_model_path": bento_model.path,
    }

    return Output(model, metadata=metadata)
