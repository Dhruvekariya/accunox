# Wisecow Application - DevOps Assessment

A containerized fortune-telling web application deployed on Kubernetes with automated CI/CD, TLS support, and zero-trust security policies.

**Live Demo:** [Docker Hub](https://hub.docker.com/r/dhruvekariyaa/wisecow)
**Repository:** [github.com/Dhruvekariya/accunox](https://github.com/Dhruvekariya/accunox)

## What is Wisecow?

Wisecow is a simple web server that combines classic Unix tools (`fortune` and `cowsay`) to serve random inspirational quotes with ASCII cow art. This project demonstrates containerization, Kubernetes orchestration, automated deployment pipelines, and security hardening practices.

## Features

- **Containerized Application**: Multi-architecture Docker image supporting AMD64 and ARM64
- **Kubernetes Ready**: Production-grade deployment manifests with health probes and resource limits
- **Automated CI/CD**: GitHub Actions workflow for building and pushing images
- **Secure by Default**: TLS/HTTPS support via NGINX Ingress Controller
- **Zero-Trust Security**: KubeArmor policy implementation (optional challenge completed)
- **Monitoring Tools**: Python scripts for application and system health monitoring

## Quick Start

### Running Locally with Docker

```bash
# Build the image
docker build -t wisecow:latest .

# Run the container
docker run -p 4499:4499 wisecow:latest

# Visit http://localhost:4499
```

### Deploying to Kubernetes

```bash
# Deploy application
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -l app=wisecow

# Access the service
kubectl port-forward service/wisecow-service 8080:80
curl http://localhost:8080
```

## Project Structure

```
.
├── Dockerfile                      # Multi-arch container image
├── wisecow.sh                      # Application entrypoint
├── k8s/                           # Kubernetes manifests
│   ├── deployment.yaml            # Deployment with 2 replicas
│   ├── service.yaml               # ClusterIP service
│   └── ingress.yaml               # TLS-enabled ingress
├── .github/workflows/             # CI/CD automation
│   └── docker-build-push.yaml     # GitHub Actions pipeline
├── scripts/                       # Helper scripts
│   └── deploy.sh                  # Automated deployment
├── monitoring-scripts/            # Health monitoring tools
│   ├── app_health_checker.py      # HTTP endpoint monitoring
│   └── system_health_monitor.py   # System resource monitoring
└── kubearmor-policies/            # Security policies
    ├── wisecow-zero-trust-policy.yaml
    └── screenshots/               # Policy enforcement demos
```

## Prerequisites

- Docker (for local development)
- Kubernetes cluster (Minikube, Kind, or managed cluster)
- kubectl CLI tool
- Docker Hub account (for CI/CD)

## CI/CD Pipeline

This project uses GitHub Actions to automate building and publishing Docker images. On every push to the `main` branch:

1. Docker image is built with layer caching
2. Image is tagged with `latest` and commit SHA
3. Image is pushed to Docker Hub

### Setting Up CI/CD

Add your Docker Hub credentials to GitHub Secrets:

```
Settings → Secrets and variables → Actions → New repository secret
Name: DOCKER_TOKEN
Value: <your-docker-hub-access-token>
```

### Deploying Updates

```bash
# Automated deployment script
./scripts/deploy.sh

# Or deploy specific image tag
IMAGE_NAME=dhruvekariyaa/wisecow:main-abc1234 ./scripts/deploy.sh
```

For more deployment strategies, see [docs/CD_SETUP.md](docs/CD_SETUP.md).

## TLS Configuration

The application supports HTTPS using NGINX Ingress Controller with self-signed certificates.

### Setup TLS

```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout wisecow-tls.key \
  -out wisecow-tls.crt \
  -subj "/CN=wisecow.local/O=wisecow"

# Create TLS secret
kubectl create secret tls wisecow-tls --cert=wisecow-tls.crt --key=wisecow-tls.key

# Deploy with ingress
kubectl apply -f k8s/ingress.yaml
```

### Testing HTTPS

```bash
# Port forward ingress controller
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8443:443

# Test connection
curl -k -H "Host: wisecow.local" https://localhost:8443
```

## Monitoring Scripts

This project includes two Python-based monitoring tools for production environments.

### Application Health Checker

Monitors HTTP endpoints and reports their status.

```bash
# Check single URL
python3 monitoring-scripts/app_health_checker.py https://example.com

# Monitor continuously
python3 monitoring-scripts/app_health_checker.py --continuous --interval 60 https://api.example.com

# Check multiple URLs from file
python3 monitoring-scripts/app_health_checker.py --file monitoring-scripts/sample-urls.txt
```

**Features**: HTTP status code validation, continuous monitoring, file-based URL input, timeout handling

### System Health Monitor

Tracks system resources and alerts on threshold violations.

```bash
# One-time check
python3 monitoring-scripts/system_health_monitor.py

# Continuous monitoring with logging
python3 monitoring-scripts/system_health_monitor.py --continuous --log /var/log/health.log

# Custom thresholds
python3 monitoring-scripts/system_health_monitor.py --thresholds cpu=90,memory=85,disk=80
```

**Features**: CPU/memory/disk monitoring, process tracking, threshold alerts, cross-platform support (Linux/macOS)

See [monitoring-scripts/README.md](monitoring-scripts/README.md) for complete documentation.

## Security: KubeArmor Zero-Trust Policy

This project implements runtime security using KubeArmor with a zero-trust policy that restricts container behavior.

**Policy Highlights**:
- Blocks access to sensitive system directories (`/etc`, `/root`, `/var/log`)
- Prevents execution from temporary directories (`/tmp`, `/var/tmp`)
- Restricts network protocols (UDP blocked, TCP allowed)
- Limits process execution to application-required binaries

**Installation**:
```bash
# Install KubeArmor via Helm
helm repo add kubearmor https://kubearmor.github.io/charts
helm install kubearmor-operator kubearmor/kubearmor-operator -n kubearmor --create-namespace

# Apply policy
kubectl apply -f kubearmor-policies/wisecow-zero-trust-policy.yaml
```

**Verification**:
```bash
# Check policy status
kubectl get kubearmorpolicies

# View policy details
kubectl describe kubearmorpolicy wisecow-zero-trust-policy
```

See [kubearmor-policies/README.md](kubearmor-policies/README.md) for detailed policy documentation and [screenshots](kubearmor-policies/screenshots/) demonstrating policy enforcement.

## Application Specifications

| Component | Details |
|-----------|---------|
| Base Image | Ubuntu 22.04 |
| Runtime Port | 4499 |
| Dependencies | fortune-mod, cowsay, netcat |
| Replicas | 2 (configurable) |
| CPU Request/Limit | 100m / 200m |
| Memory Request/Limit | 64Mi / 128Mi |
| Health Checks | TCP socket on port 4499 |

## Assessment Implementation

This repository fulfills the requirements for the Accuknox DevOps Trainee Practical Assessment:

**Problem Statement 1** - Wisecow Containerization & Kubernetes Deployment
- Dockerfile with multi-architecture support
- Kubernetes manifests (deployment, service, ingress)
- GitHub Actions CI/CD workflow
- TLS implementation (challenge goal)
- Automated deployment (challenge goal)

**Problem Statement 2** - System Monitoring Scripts
- Application health checker (HTTP monitoring)
- System health monitor (resource monitoring)

**Problem Statement 3** - KubeArmor Zero-Trust Policy (Optional)
- Policy implementation and enforcement
- Documentation with screenshots
- Security verification tests

## Contributing & Development

This project was developed as part of a technical assessment. Feel free to fork, modify, and use it as a reference for your own Kubernetes deployments.

## License

Apache License 2.0 - following the original [Wisecow](https://github.com/nyrahul/wisecow) project license.

---

**Note**: This repository is set to public as specified in the assessment requirements (Access Control section, Page 2).
