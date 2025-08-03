import bentoml
from bentoml.io import JSON
from pydantic import BaseModel


class TrafficRequest(BaseModel):
    """Input data schema for foot traffic forecasting."""
    features: list[float]


# Load the latest trained model registered in BentoML's model store.
model_runner = bentoml.sklearn.get("foot_traffic:latest").to_runner()

# Define the BentoML service with a /predict endpoint.
svc = bentoml.Service("foot_traffic_service", runners=[model_runner])


@svc.api(input=JSON(pydantic_model=TrafficRequest), output=JSON())
def predict(req: TrafficRequest) -> dict:
    """Return foot traffic predictions for the provided features."""
    prediction = model_runner.run(req.features)
    return {"prediction": prediction}
