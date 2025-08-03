variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "data_bucket_name" {
  description = "Name of the S3 bucket for data"
  type        = string
}

variable "snowflake_account" {
  description = "Snowflake account identifier"
  type        = string
}

variable "snowflake_user" {
  description = "Snowflake user name"
  type        = string
}

variable "snowflake_password" {
  description = "Snowflake user password"
  type        = string
}

variable "snowflake_role_name" {
  description = "Name of the Snowflake role"
  type        = string
}
