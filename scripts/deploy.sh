#!/bin/bash

# Deployment script for Wisecow application
# This script updates the Kubernetes deployment with the latest image

set -e

IMAGE_NAME="${IMAGE_NAME:-dhruvekariyaa/wisecow:latest}"
NAMESPACE="${NAMESPACE:-default}"
DEPLOYMENT_NAME="wisecow"

echo "🚀 Deploying Wisecow application..."
echo "Image: $IMAGE_NAME"
echo "Namespace: $NAMESPACE"
echo "Deployment: $DEPLOYMENT_NAME"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if deployment exists
if ! kubectl get deployment $DEPLOYMENT_NAME -n $NAMESPACE &> /dev/null; then
    echo "⚠️  Deployment '$DEPLOYMENT_NAME' not found in namespace '$NAMESPACE'"
    echo "📦 Applying all manifests from k8s/ directory..."
    kubectl apply -f k8s/
else
    echo "🔄 Updating deployment with new image..."
    kubectl set image deployment/$DEPLOYMENT_NAME \
        $DEPLOYMENT_NAME=$IMAGE_NAME \
        -n $NAMESPACE
fi

# Wait for rollout to complete
echo "⏳ Waiting for deployment rollout..."
kubectl rollout status deployment/$DEPLOYMENT_NAME -n $NAMESPACE --timeout=120s

# Get deployment status
echo "✅ Deployment completed successfully!"
echo ""
echo "📊 Deployment Status:"
kubectl get deployment $DEPLOYMENT_NAME -n $NAMESPACE
echo ""
echo "🏃 Running Pods:"
kubectl get pods -l app=wisecow -n $NAMESPACE

# Get service endpoint
echo ""
echo "🌐 Service Info:"
kubectl get svc wisecow-service -n $NAMESPACE

echo ""
echo "✨ Deployment completed! Application is ready."
