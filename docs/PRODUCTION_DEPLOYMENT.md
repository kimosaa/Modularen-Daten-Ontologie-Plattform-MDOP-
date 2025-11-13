# MDOP Production Deployment Guide

## Overview

This guide covers deploying MDOP to production environments with high availability, security, and monitoring.

## Architecture Options

### Option 1: Kubernetes (Recommended for Enterprise)
- **Scalability:** Horizontal auto-scaling
- **High Availability:** Multi-node deployment
- **Cost:** Medium-High
- **Complexity:** High
- **Best For:** Enterprise customers, 50+ users

### Option 2: Docker Compose (Single Node)
- **Scalability:** Limited (vertical only)
- **High Availability:** None (single point of failure)
- **Cost:** Low
- **Complexity:** Low
- **Best For:** Small teams, POCs, development

### Option 3: Cloud Managed Services
- **Scalability:** Excellent
- **High Availability:** Managed by cloud provider
- **Cost:** High
- **Complexity:** Medium
- **Best For:** Customers wanting managed infrastructure

## Pre-Deployment Checklist

- [ ] Hardware/Cloud resources provisioned
- [ ] Network configured (firewalls, load balancers)
- [ ] SSL certificates obtained
- [ ] DNS records configured
- [ ] Backup strategy defined
- [ ] Monitoring tools setup
- [ ] Security review completed
- [ ] Disaster recovery plan documented

## Production Requirements

### Minimum System Requirements
- **CPU:** 8 cores
- **RAM:** 32 GB
- **Storage:** 500 GB SSD
- **Network:** 1 Gbps

### Recommended Production Specs
- **CPU:** 16+ cores
- **RAM:** 64 GB+
- **Storage:** 1 TB+ NVMe SSD
- **Network:** 10 Gbps

### Database Sizing Guide

| Users | Entities | Neo4j RAM | PostgreSQL | Redis | Total RAM |
|-------|----------|-----------|------------|-------|-----------|
| 10 | 100K | 8 GB | 4 GB | 2 GB | 16 GB |
| 50 | 500K | 16 GB | 8 GB | 4 GB | 32 GB |
| 100 | 1M | 32 GB | 16 GB | 8 GB | 64 GB |
| 500 | 5M | 64 GB | 32 GB | 16 GB | 128 GB |

## Kubernetes Deployment

### Step 1: Prerequisites
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify cluster access
kubectl cluster-info
```

### Step 2: Create Namespace
```bash
kubectl create namespace mdop-production
kubectl config set-context --current --namespace=mdop-production
```

### Step 3: Configure Secrets
```bash
# Create secrets for sensitive data
kubectl create secret generic mdop-secrets \
  --from-literal=neo4j-password='YOUR_SECURE_PASSWORD' \
  --from-literal=postgres-password='YOUR_SECURE_PASSWORD' \
  --from-literal=jwt-secret='YOUR_JWT_SECRET'
```

### Step 4: Deploy with Helm (Recommended)
```bash
# Add MDOP Helm repository (if available)
helm repo add mdop https://charts.mdop-platform.com
helm repo update

# Deploy
helm install mdop mdop/mdop-platform \
  --namespace mdop-production \
  --values production-values.yaml
```

### Step 5: Deploy with kubectl
```bash
# Apply all manifests
kubectl apply -f infrastructure/kubernetes/

# Verify deployment
kubectl get pods
kubectl get services
```

### Step 6: Configure Ingress
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mdop-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - mdop.your-company.com
    secretName: mdop-tls
  rules:
  - host: mdop.your-company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mdop-frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: mdop-backend-service
            port:
              number: 80
```

## Security Hardening

### 1. Network Security
```bash
# Configure network policies
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mdop-network-policy
spec:
  podSelector:
    matchLabels:
      app: mdop-backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: mdop-frontend
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: neo4j
