terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    snowflake = {
      source = "snowflakedb/snowflake"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "snowflake" {}

resource "aws_s3_bucket" "data_bucket" {
  bucket = var.data_bucket_name
}

# Placeholder for Snowflake role
# resource "snowflake_role" "data_engineer" {
#   name = var.snowflake_role_name
# }
