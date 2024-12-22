output "load_balancer_hostname" {
  description = "The LoadBalancer hostname for the NGINX ingress controller"
  value       = try(data.kubernetes_service.nginx_ingress_controller.status.0.load_balancer.0.ingress.0.hostname)
}

output "namespace" {
  description = "The namespace where the NGINX ingress controller is deployed"
  value       = var.ingress_namespace
}