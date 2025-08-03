import bentoml
import torch
from bentoml.io import JSON
from pydantic import BaseModel


class TrafficRequest(BaseModel):
    """Input data schema for foot traffic forecasting."""
    features: list[float]


# Load the latest trained PyTorch model registered in BentoML's model store.
model_runner = bentoml.pytorch.get("foot_traffic:latest").to_runner()

# Define the BentoML service with a /predict endpoint.
svc = bentoml.Service("foot_traffic_service", runners=[model_runner])


@svc.api(input=JSON(pydantic_model=TrafficRequest), output=JSON())
def predict(req: TrafficRequest) -> dict:
    """Return foot traffic predictions for the provided features."""
    tensor = torch.tensor(req.features, dtype=torch.float32).unsqueeze(0)
    prediction = model_runner.run(tensor)
    return {"prediction": float(prediction.squeeze().item())}
