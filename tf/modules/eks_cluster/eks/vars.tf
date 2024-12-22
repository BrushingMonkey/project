variable "name" {
  description = "Name prefix for the EKS cluster"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for the EKS cluster"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for the EKS cluster"
  type        = list(string)
}