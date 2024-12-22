variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "argocd_hostname" {
  description = "The hostname for ArgoCD ingress"
  type        = string
}

variable "argocd_namespace" {
  description = "The namespace where ArgoCD is deployed"
  type        = string
  default     = "argocd"
}
