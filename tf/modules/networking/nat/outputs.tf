output "nat_instance_id" {
  description = "ID of the NAT instance"
  value       = aws_instance.ec2_instance.id
}

output "nat_instance_public_ip" {
  description = "Public IP of the NAT instance"
  value       = aws_instance.ec2_instance.public_ip
}

output "nat_instance_network_interface_id" {
  description = "Primary network interface ID of the NAT instance"
  value       = aws_instance.ec2_instance.primary_network_interface_id
}
