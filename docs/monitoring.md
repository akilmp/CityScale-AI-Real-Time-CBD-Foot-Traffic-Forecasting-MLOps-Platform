# Monitoring Configuration

To integrate WhyLabs monitoring and Slack alerting, the application reads several values from environment variables.

## Development

Set the variables locally before running services:

```bash
export WHYLABS_API_KEY=<api-key>
export WHYLABS_ORG_ID=<org-id>
export WHYLABS_DATASET_ID=<dataset-id>
export SLACK_WEBHOOK_URL=<slack-webhook-url>
```

## Continuous Integration

For CI pipelines (e.g., GitHub Actions), add these variables as repository secrets and expose them to jobs. Example:

```yaml
env:
  WHYLABS_API_KEY: ${{ secrets.WHYLABS_API_KEY }}
  WHYLABS_ORG_ID: ${{ secrets.WHYLABS_ORG_ID }}
  WHYLABS_DATASET_ID: ${{ secrets.WHYLABS_DATASET_ID }}
  SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

This ensures WhyLabs logging and Slack notifications work in automated environments.
