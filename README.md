# Wisecow Application - Kubernetes Deployment

This repository contains the containerized Wisecow application with Kubernetes deployment manifests and CI/CD pipeline.

## Overview

Wisecow is a simple web server that serves random fortune quotes with ASCII cow art on port 4499.

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

The GitHub Actions workflow automatically:
1. Builds the Docker image on every push to `main` branch
2. Pushes the image to Docker Hub with appropriate tags
3. Uses caching to speed up builds

### Setup GitHub Secrets

Add the following secret to your GitHub repository:

- `DOCKER_TOKEN`: Your Docker Hub access token

**Steps to add secrets:**
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `DOCKER_TOKEN` with your Docker Hub access token

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

## License

This project follows the original Wisecow repository license.
