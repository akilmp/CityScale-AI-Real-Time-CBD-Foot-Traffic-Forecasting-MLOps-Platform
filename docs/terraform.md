# Terraform Infrastructure

This guide explains how to apply Terraform configurations and manage state for the AWS infrastructure.

## Applying Changes

1. Navigate to the core Terraform directory:

   ```bash
   cd infra/terraform/core
   ```

2. Copy the example variables file and edit values for your environment:

   ```bash
   cp ../terraform.tfvars.example terraform.tfvars
   # update terraform.tfvars with appropriate values
   ```

3. Initialize Terraform providers and modules:

   ```bash
   terraform init
   ```

4. Review the execution plan:

   ```bash
   terraform plan
   ```

5. Apply the configuration:

   ```bash
   terraform apply
   ```

## Managing State

Terraform stores state in a `terraform.tfstate` file. For collaboration, configure a remote backend such as Amazon S3 with DynamoDB locking. After updating the backend configuration, re-initialize with:

```bash
terraform init -reconfigure
```

Useful state commands:

```bash
terraform state list        # View tracked resources
terraform state show <res>  # Inspect a specific resource
terraform state rm <res>    # Remove a resource from state
```

To tear down all managed resources:

```bash
terraform destroy
```

