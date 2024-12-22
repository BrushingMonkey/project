variable "name" {
  description = "Name prefix for the Node Group"
  type        = string
}

variable "cluster_name" {
  description = "EKS cluster name for the Node Group"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for the Node Group"
  type        = list(string)
}
