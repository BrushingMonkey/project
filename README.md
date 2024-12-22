Terraform EKS Cluster with ArgoCD and NGINX Ingress Controller

This project automates the deployment of an Amazon EKS cluster with associated infrastructure, including VPC, subnets, NAT gateway, and route tables. Additionally, it deploys an NGINX Ingress Controller and ArgoCD for managing Kubernetes workloads.

Features

    Amazon EKS Cluster:
        Creates an EKS cluster and associated IAM roles and policies.
        Deploys worker node groups for cluster operation.

    Networking:
        Configures a VPC with public and private subnets.
        Sets up NAT Instance and Internet Gateway for routing.
        Implements route tables for managing traffic.

    NGINX Ingress Controller:
        Deploys an NGINX ingress controller for managing external access to Kubernetes services.
        Configures an AWS Network Load Balancer (NLB) for high availability.

    ArgoCD:
        Deploys ArgoCD for GitOps-based application deployment and management.
        Configures ingress rules for accessing the ArgoCD UI.

Usage
1. Clone the Repository

git clone <repository-url>
cd <repository-folder>

2. Initialize Terraform

terraform init

3. Configure Variables

Edit variables.tf or pass variables directly via CLI or a terraform.tfvars file. Key variables:

    cluster_name: Name of the EKS cluster.
    region: AWS region for deployment.
    argocd_hostname: Hostname for ArgoCD ingress.
    ingress_namespace: Namespace for NGINX ingress deployment.

Example terraform.tfvars:

cluster_name = "my-eks-cluster"
region       = "us-west-2"
argocd_hostname = "argocd.example.com"
ingress_namespace = "ingress-nginx"

4. Apply the Configuration

terraform apply

5. Access ArgoCD

    Get the ArgoCD ingress hostname:

    terraform output argocd_ingress_url

    Access the ArgoCD UI using the provided URL.

Cleanup

To destroy the resources:

terraform destroy

If the state file is locked or resources are stuck, use:

terraform destroy -lock=false

Troubleshooting

    Service LoadBalancer Not Ready:
        Check Kubernetes service status:

    kubectl describe service nginx-ingress-controller -n ingress-nginx

ArgoCD UI Inaccessible:

    Verify ingress rules:

    kubectl get ingress -n argocd

State Lock Issues:

    Unlock the state:

        terraform force-unlock <LOCK_ID>

Contributing

Feel free to submit issues and pull requests to improve this project.
