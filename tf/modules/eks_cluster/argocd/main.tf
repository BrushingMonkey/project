data "aws_eks_cluster_auth" "main" {
  name = var.cluster_name
}

resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "4.5.2"

  namespace        = "argocd"
  create_namespace = true

  set {
    name  = "server.service.type"
    value = "ClusterIP" # Internal service for use with ingress
  }
}

resource "kubernetes_ingress_v1" "argocd_ingress" {
  metadata {
    name      = "argocd-ingress"
    namespace = "argocd"

    annotations = {
      "kubernetes.io/ingress.class"                  = "nginx"
      "nginx.ingress.kubernetes.io/backend-protocol" = "HTTPS"
      "nginx.ingress.kubernetes.io/ssl-redirect"     = "true"
    }
  }

  spec {
    rule {
      host = "argocdproject.duckdns.com"

      http {
        path {
          path     = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "argocd-server"
              port {
                number = 443
              }
            }
          }
        }
      }
    }
  }

  depends_on = [helm_release.argocd]
}
