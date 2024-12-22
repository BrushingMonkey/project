output "cluster_name" {
  description = "The name of the EKS cluster"
  value       = aws_eks_cluster.eks.name
}

output "eks_endpoint" {
  description = "The endpoint for the EKS cluster"
  value       = aws_eks_cluster.eks.endpoint
}

output "cluster_ca" {
  description = "The certificate authority data for the EKS cluster"
  value       = aws_eks_cluster.eks.certificate_authority[0].data
}
