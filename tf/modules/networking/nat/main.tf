# Fetch the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]  # Filter to Amazon-owned AMIs

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]  # Amazon Linux 2 AMIs
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Security Group for NAT Instance
resource "aws_security_group" "nat" {
  name        = "${var.name}-nat-sg"
  description = "Allow NAT Instance to forward traffic"
  vpc_id      = var.vpc_id

  # Allow inbound traffic from private subnets
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = var.private_cidr_blocks
  }

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "udp"
    cidr_blocks = var.private_cidr_blocks
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-nat-sg"
  }
}

# NAT Instance
resource "aws_instance" "ec2_instance" {
  ami                    = data.aws_ami.amazon_linux_2.id  # Use the fetched Amazon Linux 2 AMI
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [aws_security_group.nat.id]
  source_dest_check      = false  # Disable source/destination check for NAT functionality

  # User Data to configure NAT instance
  user_data = <<-EOF
    #!/bin/bash
    # Install iptables for NAT
    sudo yum install iptables-services -y
    sudo systemctl enable iptables
    sudo systemctl start iptables

    # Enable IP forwarding
    echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/custom-ip-forwarding.conf > /dev/null
    sudo sysctl -p /etc/sysctl.d/custom-ip-forwarding.conf

    # Get the primary network interface
    iface=$(netstat -i | awk 'NR>2 {print $1}' | grep -E '^(eth|en)' | head -n 1)

    # Configure NAT masquerading
    sudo /sbin/iptables -t nat -A POSTROUTING -o $iface -j MASQUERADE
    sudo /sbin/iptables -F FORWARD
    sudo service iptables save
  EOF

  tags = {
    Name = "${var.name}-nat-instance"
  }
}
