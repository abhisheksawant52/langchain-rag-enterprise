output "ecr_repository_url" {
  description = "URL of the ECR repository for the service image."
  value       = aws_ecr_repository.app.repository_url
}

output "log_group_name" {
  description = "CloudWatch log group name for the service."
  value       = aws_cloudwatch_log_group.app.name
}

output "service_security_group_id" {
  description = "Security group ID guarding the RAG service."
  value       = aws_security_group.service.id
}

output "vector_store_endpoint" {
  description = "Private endpoint of the vector store instance."
  value       = module.vector_store.endpoint
}

output "vector_store_instance_id" {
  description = "Instance ID of the vector store."
  value       = module.vector_store.instance_id
}
