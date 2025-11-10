# Accuknox DevOps Trainee Assessment

**Candidate:** Dhruv Vekariya
**Repository:** https://github.com/Dhruvekariya/accunox
**Docker Image:** https://hub.docker.com/r/dhruvekariyaa/wisecow

This repository contains the complete implementation of the Accuknox DevOps Trainee Practical Assessment including:
- Problem Statement 1: Wisecow Application Containerization & Kubernetes Deployment
- Problem Statement 2: System Monitoring Scripts (Application Health Checker + System Health Monitor)
- Problem Statement 3: KubeArmor Zero-Trust Policy (Optional - Complete)

---

## Overview

**Wisecow Application:** A simple web server that serves random fortune quotes with ASCII cow art on port 4499.

### Features Implemented
- ✅ Dockerized application (Ubuntu 22.04 base)
- ✅ Kubernetes deployment with 2 replicas
- ✅ Automated CI/CD pipeline (GitHub Actions)
- ✅ TLS/HTTPS support via NGINX Ingress (Challenge Goal)
- ✅ Continuous Deployment automation (Challenge Goal)
- ✅ Application Health Monitoring script
- ✅ System Health Monitoring script
- ✅ KubeArmor Zero-Trust Security Policy (Optional)

---

## 📋 Assessment Requirement Clarification

**Repository Visibility:**
The assessment PDF contains a contradiction:
- Page 1 states: "A **private** GitHub repository"
- Page 2 states: "The GitHub repository should be set to **public**"

**✅ Implementation Decision:** This repository is **PUBLIC** following the explicit "Access Control" section on page 2, which is the authoritative final requirement and necessary for assessment review.

---

## Prerequisites

- Docker
- Kubernetes cluster (Minikube, Kind, or OrbStack)
- kubectl
- Docker Hub account

## Project Structure

```
.
├── Dockerfile                      # Multi-arch container (linux/amd64, linux/arm64)
├── wisecow.sh                      # Main application script
├── LICENSE                         # Apache License 2.0
├── README.md                       # This file
│
├── k8s/                           # Kubernetes manifests
│   ├── deployment.yaml            # Deployment with 2 replicas, health probes
│   ├── service.yaml               # ClusterIP service
│   └── ingress.yaml               # Ingress with TLS configuration
│
├── .github/workflows/             # CI/CD automation
│   └── docker-build-push.yaml     # GitHub Actions workflow
│
├── scripts/                       # Deployment automation
│   └── deploy.sh                  # Kubernetes deployment script
│
├── docs/                          # Documentation
│   └── CD_SETUP.md                # Continuous Deployment guide
│
├── monitoring-scripts/            # Problem Statement 2
│   ├── app_health_checker.py      # HTTP health monitoring
│   ├── system_health_monitor.py   # System resource monitoring
│   ├── sample-urls.txt            # Sample URLs for testing
│   └── README.md                  # Monitoring scripts documentation
│
└── kubearmor-policies/            # Problem Statement 3 (Complete)
    ├── wisecow-zero-trust-policy.yaml  # KubeArmor security policy
    └── README.md                       # Policy documentation
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

---

## Problem Statement 2: Monitoring Scripts

This repository includes two production-ready monitoring scripts located in `monitoring-scripts/`:

### 1. Application Health Checker (`app_health_checker.py`)

Monitors application uptime by checking HTTP status codes.

**Features:**
- Single or multiple URL monitoring
- HTTP status code analysis (200-599)
- UP/DOWN status determination
- Continuous monitoring mode
- File-based URL input
- Configurable timeout
- Color-coded console output

**Usage:**
```bash
# Check single application
python3 monitoring-scripts/app_health_checker.py https://example.com

# Check multiple applications
python3 monitoring-scripts/app_health_checker.py https://google.com https://github.com

# Continuous monitoring (every 60 seconds)
python3 monitoring-scripts/app_health_checker.py --continuous --interval 60 https://example.com

# From file
python3 monitoring-scripts/app_health_checker.py --file monitoring-scripts/sample-urls.txt
```

### 2. System Health Monitor (`system_health_monitor.py`)

Monitors system resources with threshold-based alerting.

**Features:**
- CPU usage monitoring
- Memory usage monitoring
- Disk space monitoring
- Top 5 CPU-consuming processes
- Configurable thresholds (default: 80%)
- Alert system for exceeded thresholds
- Continuous monitoring mode
- File logging support
- Cross-platform (macOS/Linux)

**Usage:**
```bash
# One-time system check
python3 monitoring-scripts/system_health_monitor.py

# Continuous monitoring with logging
python3 monitoring-scripts/system_health_monitor.py --continuous --interval 60 --log health.log

# Custom thresholds
python3 monitoring-scripts/system_health_monitor.py --thresholds cpu=90,memory=85,disk=80
```

**📖 Complete documentation:** [monitoring-scripts/README.md](monitoring-scripts/README.md)

---

## Assessment Status

### ✅ Problem Statement 1: Complete (100%)
- [x] Dockerization (Multi-arch: amd64/arm64)
- [x] Kubernetes Deployment
- [x] CI/CD Pipeline (GitHub Actions)
- [x] TLS Implementation (Challenge Goal)
- [x] Continuous Deployment (Challenge Goal)

**Latest Updates:**
- Built and pushed multi-architecture Docker image (supports both Intel and ARM)
- Image available: `dhruvekariyaa/wisecow:latest`
- Verified deployment on OrbStack Kubernetes

### ✅ Problem Statement 2: Complete (100%)
- [x] Application Health Checker Script
- [x] System Health Monitor Script

**Both scripts tested and working:**
- HTTP health monitoring with status code analysis
- System resource monitoring with threshold alerts

### ✅ Problem Statement 3: Complete (100%) - Optional Extra Credit
- [x] KubeArmor installation (Helm deployed)
- [x] KubeArmor operator and controller running
- [x] Zero-trust policy written with proper syntax
- [x] Policy applied and enforced successfully
- [x] Policy validation and testing completed
- [x] Screenshots captured showing policy violations
- [x] Comprehensive documentation created

**Latest Updates:**
- KubeArmor v1.6.3 installed via Helm in `kubearmor` namespace
- Zero-trust policy enforcing file, process, network, and capability restrictions
- Policy successfully blocks unauthorized access while allowing application to function
- **Screenshots included**: 3 images demonstrating policy violations and enforcement
- Complete security documentation with verification steps

**📖 Complete documentation:** [kubearmor-policies/README.md](kubearmor-policies/README.md)
**📸 Screenshots:** [kubearmor-policies/screenshots/](kubearmor-policies/screenshots/)

---

## License

This project follows the original Wisecow repository license (Apache License 2.0).
