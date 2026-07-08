output "instance_id" {
  description = "EC2 instance ID of the vector store."
  value       = aws_instance.vector_store.id
}

output "endpoint" {
  description = "Private DNS endpoint of the vector store instance."
  value       = "${aws_instance.vector_store.private_dns}:6333"
}

output "security_group_id" {
  description = "Security group ID protecting the vector store."
  value       = aws_security_group.vector_store.id
}
