terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = var.vpc_name
  cidr   = var.vpc_cidr

  azs             = var.availability_zones
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets
}

module "eks" {
  source = "terraform-aws-modules/eks/aws"

  name               = var.cluster_name
  kubernetes_version = var.cluster_version
  iam_role_arn       = var.cluster_iam_role_arn

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    for name, cfg in var.node_groups :
    name => merge(cfg, { iam_role_arn = var.node_iam_role_arn })
  }
}
