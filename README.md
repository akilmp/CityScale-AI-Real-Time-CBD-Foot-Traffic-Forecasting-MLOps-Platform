# CityScale-AI-Real-Time-CBD-Foot-Traffic-Forecasting-MLOps-Platform

## Infrastructure

### Terraform
Infrastructure as code is organized under `infra/terraform`. Copy the example variables file and adjust values for your environment:

```bash
cp infra/terraform/terraform.tfvars.example infra/terraform/terraform.tfvars
terraform -chdir=infra/terraform/core init
terraform -chdir=infra/terraform/core apply
```

### Helmfile
Helmfile manifests for Ray, Prometheus, and Grafana live in `infra/helmfile`. Deploy the charts with:

```bash
cd infra/helmfile
helmfile sync
```
