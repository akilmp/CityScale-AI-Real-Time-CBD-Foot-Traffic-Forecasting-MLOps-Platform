variable "aws_region" {
  description = "AWS region for resources"
  type        = string
}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
}

variable "private_subnets" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "cluster_version" {
  description = "EKS Kubernetes version"
  type        = string
}

variable "cluster_iam_role_arn" {
  description = "Existing IAM role ARN for the EKS control plane"
  type        = string
}

variable "node_iam_role_arn" {
  description = "IAM role ARN for EKS managed node groups"
  type        = string
}

variable "node_groups" {
  description = "Map of EKS managed node group configurations"
  type        = any
}
