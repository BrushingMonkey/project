variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "cluster_name" {
  description = "The name of the Kubernetes (EKS) cluster"
  type        = string
}
