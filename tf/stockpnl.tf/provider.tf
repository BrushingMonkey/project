terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.70"
    }
  }

  required_version = ">= 1.2.0"
  
}
provider "aws" {
  region = "eu-north-1"
}

data "aws_eks_cluster_auth" "cluster_token" {
  name = module.eks.cluster_name
}

provider "kubernetes" {
  host                   = module.eks.eks_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster_token.token
}

provider "helm" {
  kubernetes {
    host                   = module.eks.eks_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_ca)
    token                  = data.aws_eks_cluster_auth.cluster_token.token
  }
}