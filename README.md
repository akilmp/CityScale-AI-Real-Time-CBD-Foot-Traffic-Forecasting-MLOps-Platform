# CityScale-AI Real-Time CBD Foot Traffic Forecasting MLOps Platform

## Overview
CityScale-AI is an end-to-end platform for forecasting pedestrian foot traffic in central business districts (CBDs). The system ingests real-time signals from edge sensors and open data feeds, builds ML features, trains forecasting models, and serves predictions to downstream applications.

Key capabilities:
- Streaming data ingestion via Airbyte
- Feature engineering with Tecton
- Model training using PyTorch Lightning
- Model serving in Kubernetes with continuous deployment
- Infrastructure automation with Terraform and Helmfile
- Automated workflows orchestrated through DAGs

## Architecture
### Data and ML Pipeline
```mermaid
flowchart LR
    Sensors[IoT / Open Data] --> Airbyte
    Airbyte --> FeatureStore[Tecton Feature Store]
    FeatureStore --> Training[Lightning Training Jobs]
    Training --> Registry[Model Registry]
    Registry --> Serving[Real-time Serving on K8s]
    Serving --> Monitoring[Dashboards & Alerts]
```

### Infrastructure
```mermaid
graph TD
    TF[Terraform] --> Cloud[Cloud Resources]
    Helm[Helmfile] --> k8s[Kubernetes Cluster]
    DAGs[Workflows] -->|schedule| Airbyte
    DAGs --> Training
    DAGs --> Serving
```

## Directory Structure
```
airbyte/          # Airbyte connector configurations
dags/
  assets/         # Shared DAG assets
  jobs/           # Workflow definitions
features/
  tecton/         # Tecton feature definitions
models/
  lightning/      # Training code (PyTorch Lightning)
  serving/        # Deployment and inference code
k8s/              # Kubernetes manifests
infra/
  terraform/
    core/         # Core infrastructure
    data/         # Data infrastructure
  helmfile/       # Helmfile deployments
.github/
  workflows/      # CI/CD pipelines
docs/             # Project documentation
```

## Usage
1. **Provision infrastructure**
    ```bash
    cd infra/terraform/core
    terraform init && terraform apply
    ```

2. **Deploy services**
    ```bash
    cd ../../helmfile
    helmfile sync
    ```

3. **Configure Airbyte connectors**
    ```bash
    cd ../../../airbyte/config
    # edit connector config files
    ```

4. **Run feature and model pipelines**
    ```bash
    cd ../../dags/jobs
    # schedule DAGs via your orchestrator
    ```

5. **Develop models**
    ```bash
    cd ../../models/lightning
    # implement training scripts
    ```

6. **Serve predictions**
    ```bash
    cd ../serving
    # deploy serving container to Kubernetes
    ```

## Contributing
Pull requests are welcome. Please run tests before submitting.

## License
MIT
