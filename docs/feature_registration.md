# Feature Registration and Materialization

This project uses [Tecton](https://www.tecton.ai/) for feature management. The
`scripts/register_and_materialize.sh` helper wraps the Tecton CLI to register the
feature views defined under `features/tecton` and backfill their offline data.

## Prerequisites
- Tecton CLI installed and authenticated (`tecton login`).
- Target workspace selected (`tecton workspace use <workspace>`).
- AWS credentials with access to the S3 buckets referenced by the feature
  sources.

## Usage
From the repository root, run:

```bash
./scripts/register_and_materialize.sh START_TIME END_TIME
```

`START_TIME` and `END_TIME` must be ISO-8601 timestamps. The script will:
1. Register or update feature definitions via `tecton apply`.
2. Materialize each feature view for the specified time window using
   `tecton materialize`.

Example:

```bash
./scripts/register_and_materialize.sh 2024-01-01T00:00:00Z 2024-01-07T00:00:00Z
```

This will backfill a week of data for the registered feature views.
