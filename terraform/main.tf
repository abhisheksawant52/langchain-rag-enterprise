locals {
  name_prefix = "${var.project_name}-${var.environment}"
  vpc_id      = var.vpc_id != "" ? var.vpc_id : data.aws_vpc.default.id
}

# Fallback to the account's default VPC when none is provided.
data "aws_vpc" "default" {
  default = true
}

# Container registry for the RAG service image.
resource "aws_ecr_repository" "app" {
  name                 = local.name_prefix
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Application log group.
resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/${local.name_prefix}"
  retention_in_days = var.log_retention_days
}

# Security group for the RAG service (HTTP on port 8000).
resource "aws_security_group" "service" {
  name        = "${local.name_prefix}-svc"
  description = "Allow inbound HTTP traffic to the RAG service"
  vpc_id      = local.vpc_id

  ingress {
    description = "RAG service HTTP"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Vector store backing the retriever.
module "vector_store" {
  source = "./modules/vector-store"

  name_prefix       = local.name_prefix
  instance_type     = var.vector_store_instance_type
  volume_size       = var.vector_store_volume_size
  vpc_id            = local.vpc_id
  security_group_id = aws_security_group.service.id
}
