# CityScale AI Demo Script

This script walks through a six‑minute demo of the platform. Follow it while recording as outlined in the README.

## Prerequisites

- Local stack running (Airbyte, Dagster dev server, and Grafana) as per [Local Development Environment](../README.md#local-development-environment).
- OBS configured with the profile in `docs/obs/cityscale.json`.

## Steps

1. **Intro (0:00‑0:30)** – Introduce CityScale AI and what the demo will show.
2. **Live heat‑map (0:30‑1:00)** – Share the Grafana panel that visualises current pedestrian counts.
3. **Inject festival (1:00‑1:45)** – Insert a mock event via Dagster and show the WhyLabs drift alert in Slack.
4. **Dagster retrain (1:45‑2:30)** – Trigger `python dags/jobs/run_local.py --sample` and browse the Dagster UI as the job runs.
5. **W&B sweep (2:30‑3:00)** – Open the latest Weights & Biases sweep and highlight top metrics.
6. **Rollout (3:00‑4:00)** – Use the Argo Rollouts UI to show a canary progressing from 5 % to 100 %.
7. **Autoscale (4:00‑5:00)** – Run `kubectl top pod` to show Ray Serve scaling.
8. **Outro (5:00‑6:00)** – Wrap up with the monthly cost slide and link to the repository.

Record at 1440p@60 fps. Adjust timing as needed to stay within six minutes.
