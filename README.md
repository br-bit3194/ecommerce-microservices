# ecommerce-microservices

A demo e-commerce backend built using Django microservices architecture. Each service runs independently and communicates via HTTP and AWS SQS (emulated using LocalStack).

## 📦 Microservices

- `user_service` – Handles user auth & profile
- `product_service` – Manages product listings
- `order_service` – Manages orders
- `payment_service` – Handles payments (Razorpay integration)

---

## 🚀 Getting Started with Docker

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🧱 Setup Steps

### 1. Clone the repo

### 2. (Optional) Convert all `.env` files to UTF-8
```
python convert_envs.py
```

### 3. Run the service locally
```
docker-compose up --build
```
This will:
1. Start user_service, product_service, and localstack in parallel.

2. Run init_localstack.sh to create SQS queues.

3. Then start order_service and payment_service (which depend on the queues being ready).

### 4. Service Ports
| Service          | Port |
|------------------|------|
| User Service     | 8000 |
| Product Service  | 8001 |
| Order Service    | 8002 |
| Payment Service  | 8003 |
| LocalStack (SQS) | 4566 |
