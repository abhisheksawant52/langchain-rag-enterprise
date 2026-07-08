variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name (dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name used to prefix and tag resources."
  type        = string
  default     = "langchain-rag-enterprise"
}

variable "container_image" {
  description = "Container image reference for the RAG service."
  type        = string
  default     = "langchain-rag-enterprise:latest"
}

variable "vector_store_instance_type" {
  description = "EC2 instance type backing the vector store."
  type        = string
  default     = "t3.medium"
}

variable "vector_store_volume_size" {
  description = "Root volume size (GiB) for the vector store instance."
  type        = number
  default     = 50
}

variable "vpc_id" {
  description = "VPC in which to create the service security group."
  type        = string
  default     = ""
}

variable "log_retention_days" {
  description = "Number of days to retain application logs in CloudWatch."
  type        = number
  default     = 30
}
