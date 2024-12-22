variable "vpc_id" {
  description = "VPC ID for the NAT instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the NAT instance"
  type        = string
  default     = "t3.micro"
}

variable "public_subnet_id" {
  description = "Public subnet ID where the NAT instance will be created"
  type        = string
}

variable "private_cidr_blocks" {
  description = "CIDR blocks of private subnets that need NAT access"
  type        = list(string)
}

variable "name" {
  description = "Name prefix for NAT instance resources"
  type        = string
}
