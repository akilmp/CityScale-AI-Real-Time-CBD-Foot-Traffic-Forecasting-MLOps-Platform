# CityScale-AI-Real-Time-CBD-Foot-Traffic-Forecasting-MLOps-Platform

## Monitoring

This repository includes baseline monitoring and alerting:

- **WhyLabs**: `training/train.py` and `serving/serve.py` log datasets and predictions using [whylogs](https://whylabs.ai/). Configuration lives in `monitoring/whylabs.yaml` and expects a `WHYLABS_API_KEY` environment variable.
- **Prometheus**: Scrape configs live in `monitoring/prometheus/prometheus.yml` and alerting rules in `monitoring/prometheus/alert_rules.yml`.
- **Alertmanager**: Routes alerts to Slack (update webhook in `monitoring/prometheus/alertmanager.yml`).

### Dagster retraining

Alertmanager notifications can trigger Dagster sensors to kick off retraining. A sensor listening for Alertmanager webhooks starts a Dagster job that rebuilds and redeploys the model when alerts fire, ensuring production issues automatically lead to model updates.
