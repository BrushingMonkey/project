data "aws_eks_cluster_auth" "main" {
  name = var.cluster_name
}

resource "helm_release" "nginx_ingress" {
  name       = "nginx-ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  version    = "4.10.0" # You can update this to the latest version if needed

  namespace        = var.ingress_namespace
  create_namespace = true

  set {
    name  = "controller.service.type"
    value = "LoadBalancer" # Ensure LoadBalancer is used for external access
  }

  set {
    name  = "controller.service.annotations.service\\.beta\\.kubernetes\\.io/aws-load-balancer-type"
    value = "nlb" # Changed to "nlb" (Network Load Balancer) as "alb" is not correct for ingress
  }

  set {
    name  = "controller.service.externalTrafficPolicy"
    value = "Cluster"
  }
}

data "kubernetes_service" "nginx_ingress_controller" {
  metadata {
    name      = "nginx-ingress-controller"
    namespace = var.ingress_namespace
  }
  depends_on = [helm_release.nginx_ingress]
}
