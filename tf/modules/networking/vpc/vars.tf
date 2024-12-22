variable "cidr_block" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "name" {
  description = "Name prefix for the VPC"
  type        = string
}
