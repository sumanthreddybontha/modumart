
# ModuMart

ModuMart is a modular, microservices-ready marketplace platform built to demonstrate clean architecture, scalable backend systems, and modern system design concepts. Users can buy, sell, or offer services in a community-focused environment.

## 🔧 Key Features
- User Authentication & Roles
- Listings (Products & Services)
- Cart & Checkout Flow
- Secure Payments via Stripe
- Order Processing with Queues
- Microservices-Ready Architecture

## 🧱 Tech Stack
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Search**: Elasticsearch
- **Queue**: RabbitMQ
- **Payments**: Stripe
- **Monitoring**: Prometheus + Grafana (or AWS CloudWatch)
- **Containers**: Docker

## 🧪 Planned Microservices
- Auth Service
- Product Service (with Elasticsearch)
- Cart Service (Redis + SQL)
- Payment Service (Stripe + Async Queue)
- Order Service → Queue → Email, Billing, Inventory

## 🚀 Getting Started

```bash
git clone https://github.com/sumanthreddybontha/modumart.git
cd modumart
docker-compose up --build
