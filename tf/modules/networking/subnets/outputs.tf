output "public_subnets" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnets" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "public_cidr_blocks" {
  description = "CIDR blocks of public subnets"
  value       = aws_subnet.public[*].cidr_block
}

output "private_cidr_blocks" {
  description = "CIDR blocks of private subnets"
  value       = aws_subnet.private[*].cidr_block
}
