output "nginx_ingress_loadbalancer_hostname" {
  description = "The hostname of the NGINX ingress LoadBalancer"
  value       = module.nginx_ingress.load_balancer_hostname
}

output "nginx_ingress_namespace" {
  description = "The namespace where the NGINX ingress controller is deployed"
  value       = module.nginx_ingress.namespace
}

output "argocd_ingress_url" {
  description = "The URL to access ArgoCD through the ingress"
  value       = module.argocd.ingress_url
}

output "argocd_namespace" {
  description = "The namespace where ArgoCD is deployed"
  value       = module.argocd.namespace
}
