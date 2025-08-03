# CityScale-AI-Real-Time-CBD-Foot-Traffic-Forecasting-MLOps-Platform

## Airbyte Connections

Example source and destination configuration templates are available under `airbyte/config`.
Each file contains placeholder credentials and incremental sync settings so that only new or
updated records are transferred on each run.

### Deploy with Docker Compose

1. Replace the credential placeholders in the YAML files or provide the values as environment
   variables before deployment.
2. Start the Airbyte services using Docker Compose:

   ```bash
   docker compose up -d
   ```
3. Apply the configuration files via the Airbyte CLI or API. Example using the Airbyte CLI
   container:

   ```bash
   docker compose run --rm airbyte-cli apply --config-dir airbyte/config
   ```

The above command will register the sources and Snowflake destination defined in the YAML files.
