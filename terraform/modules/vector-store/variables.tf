variable "name_prefix" {
  description = "Prefix used to name vector store resources."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for the vector store."
  type        = string
  default     = "t3.medium"
}

variable "volume_size" {
  description = "Root volume size in GiB."
  type        = number
  default     = 50
}

variable "vpc_id" {
  description = "VPC in which to place the vector store."
  type        = string
}

variable "security_group_id" {
  description = "Security group allowed to reach the vector store."
  type        = string
}
