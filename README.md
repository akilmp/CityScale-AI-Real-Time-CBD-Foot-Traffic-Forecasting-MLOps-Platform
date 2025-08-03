# CityScale-AI-Real-Time-CBD-Foot-Traffic-Forecasting-MLOps-Platform

## Bento Service

A BentoML service for foot traffic forecasting is defined in `models/serving/service.py` and configured via `bentofile.yaml`.

### Build the Bento bundle

```bash
bentoml build
```

### Build the container image

```bash
bentoml containerize foot_traffic_service:latest
```
