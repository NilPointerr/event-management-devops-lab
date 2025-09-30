# Inventory Management Microservices Project

This project is a **microservices-based Inventory Management system** built using **FastAPI** and **PostgreSQL**.  
The main purpose of this project is to practice **Docker, Kubernetes, and Jenkins** with a real-world style application.

---

## 📂 Project Structure

```
inventory_management/
│── deployment/
│   ├── docker-compose.yml
│── services/
│   ├── product_service/
│   │   ├── main.py
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   ├── order_service/
│   │   ├── main.py
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   ├── user_service/
│   │   ├── main.py
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
└── README.md
```

---

## 🚀 Microservices Overview

- `product_service` → port **8001**
- `order_service` → port **8002**
- `user_service` → port **8003**

All services share a **single PostgreSQL database**.

---

## 📦 Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [uv package manager](https://docs.astral.sh/uv/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Kubernetes (kubectl + minikube)](https://kubernetes.io/docs/tasks/tools/)

---

## 🛠️ Installing `uv` Package Manager

`uv` is a modern Python package/dependency manager (faster than pip).

### 🔹 On Linux/macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Add to PATH (if not already):  
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 🔹 On Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Make sure it's installed:

```bash
uv --version
```

---

## ▶️ Run Without Docker

1. Create PostgreSQL Database:

```sql
CREATE DATABASE inventory_db;
```

2. Start services one by one:

```bash
# Product Service
cd services/product_service
uv run uvicorn main:app --reload --port 8001

# Order Service
cd services/order_service
uv run uvicorn main:app --reload --port 8002

# User Service
cd services/user_service
uv run uvicorn main:app --reload --port 8003
```

---

## 🐳 Run with Docker

```bash
docker-compose -f deployment/docker-compose.yml up --build
```

---

## ☸️ Run with Kubernetes

### 1. Start Minikube

```bash
minikube start
```

### 2. Build Docker Images

```bash
# Product Service
cd services/product_service
docker build -t product_service:latest .

# Order Service
cd ../order_service
docker build -t order_service:latest .

# User Service
cd ../user_service
docker build -t user_service:latest .
```

Load images into Minikube:

```bash
minikube image load product_service:latest
minikube image load order_service:latest
minikube image load user_service:latest
```

### 3. Apply Kubernetes Manifests

```bash
kubectl apply -f namespace.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f product-deployment.yaml
kubectl apply -f product-service.yaml
kubectl apply -f order-deployment.yaml
kubectl apply -f order-service.yaml
kubectl apply -f user-deployment.yaml
kubectl apply -f user-service.yaml
```

### 4. Verify

```bash
kubectl get pods -n inventory-ns
kubectl get svc -n inventory-ns
```

### 5. Access Services

- Product Service → <http://localhost:30001>
- Order Service → <http://localhost:30002>
- User Service → <http://localhost:30003>

---

## ⚡ Next Steps

- Use **Ingress** for a single entrypoint instead of multiple NodePorts.  
- Store DB credentials in **ConfigMaps & Secrets**.  
- Add **Horizontal Pod Autoscaler (HPA)** for scaling.  
- Setup **Jenkins pipeline** for CI/CD automation.  

---

## 💻 Helper Scripts

### Linux/macOS

```bash
chmod +x deployment/deploy_k8s.sh
./deployment/deploy_k8s.sh
```

### Windows

```powershell
deployment/deploy_k8s.sh
```

---

## ✅ Learning Goals

This project was built to practice:  
- FastAPI microservices development  
- Docker containerization  
- Kubernetes orchestration  
- CI/CD with Jenkins  



