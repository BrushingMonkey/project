variable "vpc_id" {
  description = "VPC ID for route tables"
  type        = string
}

variable "igw_id" {
  description = "Internet Gateway ID for public routes"
  type        = string
}

variable "nat_instance_network_interface_id" {
  description = "Primary network interface ID of the NAT instance"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "name" {
  description = "Name prefix for route tables"
  type        = string
}
