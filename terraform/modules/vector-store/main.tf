# Latest Amazon Linux 2023 AMI for the vector store host.
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# Dedicated security group for the vector store, reachable only from the
# service security group.
resource "aws_security_group" "vector_store" {
  name        = "${var.name_prefix}-vstore"
  description = "Vector store access from the RAG service"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Vector store API"
    from_port       = 6333
    to_port         = 6333
    protocol        = "tcp"
    security_groups = [var.security_group_id]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance hosting the vector store engine.
resource "aws_instance" "vector_store" {
  ami                    = data.aws_ami.al2023.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.vector_store.id]

  root_block_device {
    volume_size = var.volume_size
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "${var.name_prefix}-vector-store"
    Role = "vector-store"
  }
}
