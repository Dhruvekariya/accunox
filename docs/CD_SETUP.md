# Continuous Deployment Setup

This document explains the Continuous Deployment (CD) strategy for the Wisecow application.

## Current Setup

### Continuous Integration (CI) ✅
- **Automated:** Yes
- **Trigger:** Push to `main` branch
- **Actions:**
  - Build Docker image
  - Push to Docker Hub with tags (`latest` and SHA-based)
  - Cache layers for faster builds

### Continuous Deployment (CD) Options

Due to the local Kubernetes cluster (OrbStack), there are multiple CD approaches:

## Option 1: Manual Deployment Script (Current Implementation)

### Usage
```bash
# Deploy/Update with latest image
./scripts/deploy.sh

# Deploy with specific image tag
IMAGE_NAME=dhruvekariyaa/wisecow:main-abc1234 ./scripts/deploy.sh
```

### Features
- ✅ Updates deployment with new image
- ✅ Waits for rollout completion
- ✅ Shows deployment status
- ✅ Validates kubectl availability
- ✅ Handles both new and existing deployments

## Option 2: GitHub Actions Self-Hosted Runner (For Production)

For production environments with accessible Kubernetes clusters:

### Setup Steps

1. **Install Self-Hosted Runner**
   ```bash
   # On your cluster machine
   mkdir actions-runner && cd actions-runner
   # Follow GitHub instructions to download and configure runner
   ```

2. **Update Workflow** (`.github/workflows/docker-build-push.yaml`)
   ```yaml
   deploy:
     needs: build-and-push
     runs-on: self-hosted
     steps:
       - name: Deploy to Kubernetes
         run: |
           kubectl set image deployment/wisecow wisecow=${{ env.IMAGE_NAME }}:${{ github.sha }}
           kubectl rollout status deployment/wisecow
   ```

3. **Add Kubernetes Credentials**
   - Add `KUBECONFIG` as GitHub secret
   - Configure kubectl on self-hosted runner

## Option 3: GitOps with ArgoCD/FluxCD (Recommended for Production)

### ArgoCD Setup
```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Create application
argocd app create wisecow \
  --repo https://github.com/Dhruvekariya/accunox.git \
  --path k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --sync-policy automated
```

### Benefits
- Declarative GitOps workflow
- Automatic sync with repository
- Easy rollback capabilities
- Complete audit trail

## Option 4: Image Watcher Script (Automated for Local)

### Concept
A script that periodically checks for new images and updates deployment:

```bash
#!/bin/bash
# watch-and-deploy.sh
while true; do
  REMOTE_DIGEST=$(docker manifest inspect dhruvekariyaa/wisecow:latest | jq -r .config.digest)
  CURRENT_DIGEST=$(kubectl get deployment wisecow -o jsonpath='{.spec.template.spec.containers[0].image}')

  if [ "$REMOTE_DIGEST" != "$CURRENT_DIGEST" ]; then
    echo "New image detected, deploying..."
    ./scripts/deploy.sh
  fi

  sleep 60  # Check every minute
done
```

## Current Workflow

```
┌─────────────┐
│  Git Push   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  GitHub Actions CI  │
│  - Build Image      │
│  - Push to Docker   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Docker Hub        │
│  (dhruvekariyaa/    │
│   wisecow:latest)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Manual/Scripted    │
│  Deployment         │
│  ./scripts/deploy.sh│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Kubernetes         │
│  (OrbStack Local)   │
└─────────────────────┘
```

## Recommended Approach by Environment

| Environment | Recommended CD Method | Automation Level |
|-------------|----------------------|------------------|
| **Local Dev** | Manual script (`deploy.sh`) | Semi-automated |
| **Staging** | Self-hosted runner | Fully automated |
| **Production** | GitOps (ArgoCD/FluxCD) | Fully automated |

## Testing the Current Setup

### 1. Make a code change
```bash
echo "# Test change" >> README.md
git add README.md
git commit -m "Test CI/CD pipeline"
git push
```

### 2. Wait for CI to complete
- Check GitHub Actions: https://github.com/Dhruvekariya/accunox/actions
- Verify new image on Docker Hub

### 3. Deploy manually
```bash
./scripts/deploy.sh
```

### 4. Verify deployment
```bash
kubectl get pods
kubectl port-forward service/wisecow-service 8080:80
curl http://localhost:8080
```

## Security Considerations

- ✅ Docker Hub credentials stored as GitHub Secrets
- ✅ No cluster credentials in repository
- ✅ TLS certificates stored as Kubernetes secrets
- ⚠️ Self-signed certificates (use cert-manager for production)
- ⚠️ LoadBalancer exposed (use Ingress + authentication for production)

## Future Enhancements

1. **Implement rollback automation**
   ```bash
   kubectl rollout undo deployment/wisecow
   ```

2. **Add health checks in workflow**
   ```bash
   curl -f https://wisecow.local/health || exit 1
   ```

3. **Implement blue-green deployment**
   - Deploy to blue environment
   - Run smoke tests
   - Switch traffic to blue
   - Keep green for rollback

4. **Add Slack/Discord notifications**
   - Notify on deployment success/failure
   - Include image SHA and deployment time

## Monitoring Deployments

```bash
# Watch deployment progress
kubectl rollout status deployment/wisecow --watch

# View recent changes
kubectl rollout history deployment/wisecow

# Check pod logs
kubectl logs -f -l app=wisecow

# View events
kubectl get events --sort-by='.lastTimestamp'
```
