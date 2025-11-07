# Wisecow Application - Kubernetes Deployment

This repository contains the containerized Wisecow application with Kubernetes deployment manifests and CI/CD pipeline.

## Overview

Wisecow is a simple web server that serves random fortune quotes with ASCII cow art on port 4499.

**Features:**
- Random fortune quotes
- ASCII art cow display
- Dockerized application
- Kubernetes deployment ready
- TLS/HTTPS support via Ingress
- Automated CI/CD pipeline

## Prerequisites

- Docker
- Kubernetes cluster (Minikube, Kind, or OrbStack)
- kubectl
- Docker Hub account

## Project Structure

```
.
├── Dockerfile                 # Container image definition
├── wisecow.sh                # Main application script
├── k8s/
│   ├── deployment.yaml       # Kubernetes Deployment manifest
│   └── service.yaml          # Kubernetes Service manifest (LoadBalancer)
└── .github/
    └── workflows/
        └── docker-build-push.yaml  # CI/CD workflow
```

## Local Development

### Build Docker Image

```bash
docker build -t dhruvekariyaa/wisecow:latest .
```

### Run Locally

```bash
docker run -p 4499:4499 dhruvekariyaa/wisecow:latest
```

Access the application at `http://localhost:4499`

## Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f k8s/deployment.yaml

# Apply service
kubectl apply -f k8s/service.yaml

# Check status
kubectl get deployments,pods,services
```

### Test the Deployment

```bash
# Port forward to test
kubectl port-forward service/wisecow-service 8080:80

# Test
curl http://localhost:8080
```

## CI/CD Pipeline

### Continuous Integration (Automated)

The GitHub Actions workflow automatically:
1. Builds the Docker image on every push to `main` branch
2. Pushes the image to Docker Hub with tags (`latest` and SHA-based)
3. Uses layer caching to speed up builds

**Workflow file:** `.github/workflows/docker-build-push.yaml`

### Continuous Deployment

For deployment automation:
```bash
# Deploy latest image
./scripts/deploy.sh

# Deploy specific image tag
IMAGE_NAME=dhruvekariyaa/wisecow:main-abc1234 ./scripts/deploy.sh
```

**📖 For detailed CD setup options, see:** [docs/CD_SETUP.md](docs/CD_SETUP.md)

### Setup GitHub Secrets

Add the following secret to your GitHub repository:

- `DOCKER_TOKEN`: Your Docker Hub access token

**Steps to add secrets:**
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `DOCKER_TOKEN` with your Docker Hub access token

### Verify CI/CD Pipeline

```bash
# Make a change
git commit -am "Test CI/CD"
git push

# Watch GitHub Actions
# Visit: https://github.com/YOUR_USERNAME/accunox/actions

# Once CI completes, deploy
./scripts/deploy.sh
```

## Application Features

- **Base Image**: Ubuntu 22.04
- **Dependencies**: fortune-mod, cowsay, netcat
- **Port**: 4499
- **Replicas**: 2 (configurable)
- **Resource Limits**:
  - Memory: 64Mi (request) / 128Mi (limit)
  - CPU: 100m (request) / 200m (limit)
- **Health Checks**: Liveness and Readiness probes configured

## Docker Hub

Image available at: `dhruvekariyaa/wisecow:latest`

## TLS Configuration

The application is configured with HTTPS using self-signed certificates and NGINX Ingress Controller.

### Prerequisites for TLS
- NGINX Ingress Controller installed in cluster
- Self-signed TLS certificate (or use cert-manager for production)

### Deploy with TLS

```bash
# Install NGINX Ingress Controller (if not already installed)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Create TLS certificate (self-signed for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout wisecow-tls.key \
  -out wisecow-tls.crt \
  -subj "/CN=wisecow.local/O=wisecow"

# Create Kubernetes TLS secret
kubectl create secret tls wisecow-tls --cert=wisecow-tls.crt --key=wisecow-tls.key

# Apply all manifests
kubectl apply -f k8s/

# Verify Ingress
kubectl get ingress
```

### Access via HTTPS

```bash
# Port forward the Ingress controller
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8443:443

# Test HTTPS connection
curl -k -H "Host: wisecow.local" https://localhost:8443
```

**TLS Details:**
- Domain: wisecow.local
- Certificate: Self-signed X.509
- Validity: 365 days
- Ingress: NGINX with TLS termination

## License

This project follows the original Wisecow repository license.
