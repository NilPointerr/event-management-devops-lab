#!/bin/bash
set -e

NAMESPACE="inventory-ns"

echo "🚀 Starting Minikube..."
minikube start

echo "📦 Building Docker images..."
docker build -t product_service:latest ./services/product_service
docker build -t order_service:latest ./services/order_service
docker build -t user_service:latest ./services/user_service

echo "📥 Loading images into Minikube..."
minikube image load product_service:latest
minikube image load order_service:latest
minikube image load user_service:latest

echo "🛠️ Creating namespace..."
kubectl apply -f deployment/k8s/namespace.yaml

echo "🐘 Deploying Postgres..."
kubectl apply -f deployment/k8s/postgres-deployment.yaml
kubectl apply -f deployment/k8s/postgres-service.yaml

echo "📦 Deploying Product Service..."
kubectl apply -f deployment/k8s/product-deployment.yaml
kubectl apply -f deployment/k8s/product-service.yaml

echo "📦 Deploying Order Service..."
kubectl apply -f deployment/k8s/order-deployment.yaml
kubectl apply -f deployment/k8s/order-service.yaml

echo "📦 Deploying User Service..."
kubectl apply -f deployment/k8s/user-deployment.yaml
kubectl apply -f deployment/k8s/user-service.yaml

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=90s || true
kubectl wait --for=condition=ready pod -l app=product-service -n $NAMESPACE --timeout=90s || true
kubectl wait --for=condition=ready pod -l app=order-service -n $NAMESPACE --timeout=90s || true
kubectl wait --for=condition=ready pod -l app=user-service -n $NAMESPACE --timeout=90s || true

echo "✅ All services deployed successfully!"
kubectl get pods -n $NAMESPACE
kubectl get svc -n $NAMESPACE

echo "🌐 Access services at:"
echo " - Product Service → http://localhost:30001"
echo " - Order Service   → http://localhost:30002"
echo " - User Service    → http://localhost:30003"
