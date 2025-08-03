# CityScale AI – Real‑Time CBD Foot‑Traffic Forecasting MLOps Platform

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Key Competencies & Their Implementation](#key-competencies--their-implementation)
4. [Tech Stack](#tech-stack)
5. [Data Sources](#data-sources)
6. [Repository Layout](#repository-layout)
7. [Local Development Environment](#local-development-environment)
8. [Infrastructure‑as‑Code](#infrastructure-as-code)
9. [Data Ingestion & Versioning](#data-ingestion--versioning)
10. [Feature Engineering & Store](#feature-engineering--store)
11. [Training, Tuning & Experiment Tracking](#training-tuning--experiment-tracking)
12. [CI/CD & Promotion Pipeline](#cicd--promotion-pipeline)
13. [Model Serving & Deployment Strategies](#model-serving--deployment-strategies)
14. [Monitoring, Drift & Alerting](#monitoring-drift--alerting)
15. [Cost Management](#cost-management)
16. [Demo Recording Guide](#demo-recording-guide)
17. [Troubleshooting & FAQ](#troubleshooting--faq)
18. [Stretch Goals](#stretch-goals)
19. [References](#references)

---

## Project Overview

**CityScale AI** forecasts hourly pedestrian foot‑traffic across Sydney’s CBD using live pedestrian‑counter feeds, weather data, and public event schedules. The platform automates the ML lifecycle end‑to‑end: ❶ Airbyte pipelines raw data into Snowflake and versions each snapshot with DVC, ❷ Dagster asset graphs clean and join data then push features to Tecton, ❸ PyTorch Lightning + Optuna train and tune models logged to Weights & Biases, ❹ GitHub Actions validate metrics and containerise the BentoML service, ❺ Argo Rollouts canaries the model on a Ray Serve cluster with Istio mTLS, and ❻ WhyLabs + Prometheus monitor drift and latency, triggering automatic Dagster retraining if SLOs break.  Idle cost ≈ AUD 25/month.

---

## System Architecture

```text
Ped‑Counter API ─┐
Weather API ─────┼─► Airbyte ▸ Snowflake RAW ▸ Dagster ETL ▸ Snowflake CLEAN
Event Feed CSV ──┘                                   │
                                                    ▼
                                   +─── Feature Store (Tecton) ───+
                                   │  rolling counts, weather lag │
                                   +────────────┬─────────────────+
                                                 │
                             Dagster Train & Tune (Optuna)
                                   │        │
                     W&B run logs  │        └──→ W&B Model Registry
                                   ▼
                                GitHub PR → Metrics Gate (≥0.82 F1)
                                   ▼
                             Docker Build → BentoML Bundle
                                   ▼
                         Ray Serve (GPU optional) on EKS
                                   ▲
                Argo Rollouts canary 5 % → 25 % → 100 %
                                   ▼
     WhyLabs drift + Prometheus latency ───► Slack #cityscale‑alerts
```

The diagram above is maintained in [docs/architecture.drawio](docs/architecture.drawio).
To export it to PNG for slides or docs:

```bash
npx @drawio/cli docs/architecture.drawio -o docs/architecture.png
```

---

## Key Competencies & Their Implementation

| Competency                         | Implementation                                                                                  |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Data ingestion & versioning**    | Airbyte incremental syncs ➜ Snowflake; DVC tracks exported Parquet snapshots on S3              |
| **Orchestration (Dagster)**        | Asset graph: `raw_assets → clean_assets → tecton_features → model_train → evaluation → rollout` |
| **Feature Store (Tecton)**         | Dev tier SaaS; Redis online store (<10 ms lookup) + Snowflake offline                           |
| **Experiment tracking & registry** | Weights & Biases sweeps, model artefacts promoted to W\&B Model Registry stages                 |
| **Hyper‑parameter tuning**         | Optuna multi‑trial study executed as Dagster job, GPU spot node pool                            |
| **Containerised serving**          | BentoML service bundled and deployed to Ray Serve cluster (autoscaler to 0)                     |
| **Deployment strategy**            | Argo Rollouts canary with automatic abort via Prometheus SLO query                              |
| **Monitoring**                     | WhyLabs dataset + prediction drift; Prometheus latency, error‑rate; Grafana dashboards          |
| **Security & policy**              | Istio STRICT mTLS, OPA Gatekeeper image‑scan policy, secrets in AWS Parameter Store             |
| **FinOps**                         | Snowflake auto‑suspend, Ray autoscale, Infracost check in GitHub CI                             |

---

## Tech Stack

| Layer               | Tool / Service                                 |
| ------------------- | ---------------------------------------------- |
| Object Storage      | S3 (raw snapshots, model artefacts)            |
| Data Warehouse      | Snowflake (RAW & CLEAN)                        |
| Orchestrator        | Dagster 1.5 (Docker → EKS)                     |
| Feature Store       | Tecton dev tier (Redis + Snowflake)            |
| Training & Tuning   | PyTorch Lightning 2.2, Optuna 3                |
| Tracking & Registry | Weights & Biases 2025 plan                     |
| Serving             | BentoML 1.2, Ray Serve 2.9, Istio ingress      |
| Deployment          | Argo Rollouts 1.6, Helm 3                      |
| Monitoring          | WhyLabs free tier, Prometheus 2.51, Grafana 11 |
| IaC                 | Terraform 1.7, Helmfile, DVC, Infracost        |

---

## Data Sources

| Feed                                                  | Frequency         | Access         | Notes                           |
| ----------------------------------------------------- | ----------------- | -------------- | ------------------------------- |
| Sydney Pedestrian Counters (City of Sydney Open Data) | Hourly JSON        | API token (`PEDESTRIAN_API_TOKEN`) | \~60 counters                   |
| BOM Weather API (Observations + Forecast)             | Hourly REST       | Public         | Temp, rain, wind                |
| Ticketek / Eventbrite scraping (CBD events)           | Nightly CSV       | Scraper + cron | Event type, expected attendance |
| NSW Public Holidays                                   | Annual CSV        | Static         | Used for holiday flag feature   |

---

## Repository Layout

```
cityscale-ai/
├── airbyte/
│   └── config/                    # source & destination yaml
├── dags/                          # Dagster definitions
│   ├── assets/
│   └── jobs/
├── features/
│   └── tecton/
│       ├── repo.py
│       └── features.py
├── models/
│   ├── lightning/
│   │   ├── datamodule.py
│   │   ├── model.py
│   │   └── train.py
│   └── serving/
│       ├── service.py
│       └── bentofile.yaml
├── k8s/
│   ├── ray-cluster.yaml
│   └── argo-rollout.yaml
├── infra/
│   ├── terraform/
│   │   ├── core/      # VPC, EKS, RDS (if needed)
│   │   └── data/      # S3 buckets, Snowflake IAM bindings
│   └── helmfile/
│       ├── ray.yaml
│       └── monitoring.yaml
├── .github/workflows/
│   ├── ci.yml
│   └── rollout.yml
└── docs/
    ├── architecture.drawio
    └── demo_script.md
```

---

## Local Development Environment

```bash
# 1. Clone and set up env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# 2. Pull sample data (requires dvc)
dvc pull

# 3. Start Airbyte (compose)
docker compose -f airbyte/docker-compose.yaml up -d

# 3. Populate required environment variables
# export SNOWFLAKE_ACCOUNT=<account>
# export SNOWFLAKE_USER=<user>
# export SNOWFLAKE_PASSWORD=<password>
# export PEDESTRIAN_API_TOKEN=<token>
# export WANDB_API_KEY=<api-key>
# export WHYLABS_API_KEY=<api-key>


# 4. Run Dagster dev server
export DAGSTER_HOME=$PWD/dagster_home
dagster dev -f dags/jobs/local_dev.py &

# 5. Trigger sample ETL + training
python dags/jobs/run_local.py --sample
```

---

## Infrastructure‑as‑Code

* **Terraform modules**: `core` (VPC, EKS, IAM OIDC, S3), `data` (Snowflake roles, warehouses), `ray` (Karpenter GPU node pool).
* **Helmfile** installs: Istio 1.23, Prometheus stack, Ray cluster, Argo Rollouts CRDs, Gatekeeper.
* **DVC** remote set to `s3://cityscale-raw/<branch>`; `dvc exp` used for quick local experiments.

Deploy sequence example:

```bash
cd infra/terraform/core && terraform init && terraform apply
cd ../data && terraform init && terraform apply
helmfile -f infra/helmfile/00_istio.yaml apply
helmfile -f infra/helmfile/ray.yaml apply
```

---

## Data Ingestion & Versioning

1. **Airbyte Connections**: each API → Snowflake RAW table (incremental + append).
2. Nightly Dagster job exports RAW tables to Parquet → commits to DVC; tag = ingestion date.
3. DVC pushes to S3; Git hash stored in Dagster metadata for lineage.
4. Sample datasets for local development live in `data/`; run `dvc pull` to download or `dvc add data` to version new snapshots.

---

## Feature Engineering & Store

* **Tecton** declarative feature definitions: rolling 60‑min foot‑count, weather lag 3 h, event attendance indicator, holiday flag.
* Online materialisation to Redis every 5 min; offline to Snowflake every hour.
* SparkFeatureJob in Tecton free tier handles mini‑batches.

---

## Training, Tuning & Experiment Tracking

* **Lightning Module** combines TabPFN (tabular transformer) with categorical embeddings.
* **Optuna** search space: learning rate, dropout, transformer depth, l1/l2.
* **W\&B Sweep** orchestrated inside Dagster op; top‑metric (`MAPE`) model auto‑logged.
* Promotion rule: `MAPE <= 12 %` and drift score < 0.15.

---

## CI/CD & Promotion Pipeline

1. **GitHub Action ci.yml**: lint + unit tests + Great Expectations validation on sample dataset + DVC data checksum.
2. Build BentoML bundle, run `bentoml containerize`, push to GHCR.
3. `rollout.yml` patches `image:` in `argo-rollout.yaml`; Argo CD auto‑sync triggers canary.
4. Rollout steps: 5 %, wait 2 min; 25 %, wait 5; 100 %. Auto‑abort if Prometheus alert fires.

---

## Model Serving & Deployment Strategies

| Cluster      | Runtime                  | Autoscale              | Traffic Split        |
| ------------ | ------------------------ | ---------------------- | -------------------- |
| **EKS**      | Ray Serve Python runtime | min 0, max 10 replicas | Argo Rollouts canary |
| **Dev Kind** | uvicorn server in Docker | manual                 | 100 %                |

* Istio Gateway exposes `/predict` with JWT auth.
* TLS cert via ACM + cert‑manager.

---

## Monitoring, Drift & Alerting

* **WhyLabs** model package monitors feature drift, prediction drift, data quality.
* **Prometheus** scrapes Ray Serve `/metrics`; RED dashboard shows P95 latency, error rate.
* **Alertmanager** routes: `latency_p95 > 150ms` or `drift > 0.2` → Slack `#cityscale-alerts`.
* Drift alert triggers Dagster sensor which launches `retrain_on_drift.py`.

---

## Cost Management

| Resource              | Optimisation                             | Est. AUD/mo |
| --------------------- | ---------------------------------------- | ----------- |
| Snowflake DW          | X‑Small warehouse suspend after 10 min   | 6           |
| EKS nodes             | Spot + Karpenter scale‑to‑zero on Ray    | 9           |
| Ray Serve GPUs        | On‑demand g4dn.xlarge only on peak hours | 5           |
| Monitoring stack      | Grafana Cloud free tier                  | 0           |
| Misc (NS data egress) | CloudFront cache, compressed JSON        | 3           |
| **Total**             |                                          | **≈ 25**    |

---

## Demo Recording Guide

| Segment         | Duration  | Visual                   |
| --------------- | --------- | ------------------------ |
| Intro           | 0:00‑0:30 | Selfie                   |
| Live heat‑map   | 0:30‑1:00 | Grafana panel            |
| Inject festival | 1:00‑1:45 | WhyLabs drift → Slack    |
| Dagster retrain | 1:45‑2:30 | Dagster UI DAG           |
| W\&B sweep      | 2:30‑3:00 | W\&B dashboard           |
| Rollout         | 3:00‑4:00 | Argo Rollouts UI + Kiali |
| Autoscale       | 4:00‑5:00 | kubectl top pod          |
| Outro           | 5:00‑6:00 | Cost slide & repo link   |

A step‑by‑step narration lives in [docs/demo_script.md](docs/demo_script.md).
Start the local stack as described in [Local Development Environment](#local-development-environment)
and follow the script while recording.

Record 1440p\@60 fps; OBS profile saved to `docs/obs/cityscale.json`.

---

## Troubleshooting & FAQ

\| Issue | Cause | Resolution |
\|-------|-------|
\| Airbyte job timeout | API rate‑limit | Enable incremental sync + small batch size |
\| Dagster asset error "SnowflakeSessionError" | Network Δ | Increase SF retry + keep‑alive |
\| Tecton feature out of sync | Clock skew | Ensure cluster NTP; re‑run materialisation |
\| Ray Serve 503 | Autoscaled to 0 | Pre‑warm min 1 replica 5 min before peak |
\| WhyLabs drift false positive | Event injection | Adjust drift window or whitelist feature |

---

## Stretch Goals

* **Realtime Graph Features** via Materialize streaming views.  |
* **Edge Forecast** on Nvidia Jetson deployed in cafés via K3s.  |
* **SaaS Self‑Service Portal** using Backstage + Service Catalog for data team onboarding.  |
* **Carbon Dashboard** integrating Cloud Carbon Footprint SDK.  |

---

## References

* City of Sydney Pedestrian Counters – [https://data.cityofsydney.nsw.gov.au/](https://data.cityofsydney.nsw.gov.au/)
* Tecton Dev Tier docs – 2025
* Dagster Asset Graph patterns – Dagster blog 2025
* BentoML 1.x best practices – BentoML docs 2025
* WhyLabs Open Source SDK – 2024

---

*Last updated: 3 Aug 2025*
