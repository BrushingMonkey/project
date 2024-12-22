variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "ingress_namespace" {
  description = "The namespace where the NGINX ingress controller will be deployed"
  type        = string
  default     = "ingress-nginx"
}
