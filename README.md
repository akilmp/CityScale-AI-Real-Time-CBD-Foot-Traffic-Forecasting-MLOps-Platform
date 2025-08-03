# CityScale-AI-Real-Time-CBD-Foot-Traffic-Forecasting-MLOps-Platform

## Repository Settings

### Secrets

- `REGISTRY_USERNAME` – Container registry username used to push Bento images.
- `REGISTRY_PASSWORD` – Password or token for the registry user.
- `KUBE_CONFIG` – Base64 encoded kubeconfig for the target Kubernetes cluster.

### Variables

- `REGISTRY` – Registry host, e.g. `ghcr.io/your-org`.
- `IMAGE_NAME` – Name of the Bento image repository.
- `ROLLOUT_NAME` – Name of the Argo Rollout resource to update.
- `ROLLOUT_NAMESPACE` – Kubernetes namespace where the rollout lives.
