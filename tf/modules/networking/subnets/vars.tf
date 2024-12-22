variable "vpc_id" {
  description = "VPC ID for the subnets"
  type        = string
}

variable "public_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "name" {
  description = "Name prefix for subnets"
  type        = string
}
