# Blog API

Blog API is a production-ready RESTful backend application built with FastAPI, SQLAlchemy, PostgreSQL and Redis.
This project demonstrates modern backend architecture, async programming, environment-based configuration, containerization with Docker, and automated testing.

## Overview
This project implements a scalable blog platform backend with:
- User registration and JWT authentication (access + refresh tokens)
- Role-based access (admin bootstrap via environment variables)
- CRUD operations for blog posts
- CRUD operations for comments
- CRUD operations for categories
- CRUD operations for users
- Operations for health check
- Rate limiting for requests
- Asynchronous database interaction
- Redis integration
- Database migrations via Alembic
- Dockerized infrastructure
- Automated test suite (pytest)

The architecture follows clean separation of concerns and is designed for real-world production use.

## Tech Stack
- **Language:** Python 3.12+
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **ORM:** SQLAlchemy 2.0 (async)
- **Database:** PostgreSQL 16
- **Migrations:** Alembic
- **Cache / Broker:** Redis 7
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Passlib (bcrypt)
- **Configuratiom:** Pydantic Settings (.env)
- **Testing:** pytest + pytest-asyncio
- **Containerization:** Docker & Docker Compose

## Environment Configuration
The application is fully configurable via environment variables using Pydantic Settings.

Before running the project, create a `.env` file based on `.env.example`:
```bash
cp .env.example .env.
```

## Features
- JWT-based authentication (access + refresh tokens)
- Secure password hashing (bcrypt)
- Rate limiting for requests
- Hard and soft deleting
- Async-first database architecture
- Autocommit database migration on startup
- Admin auto-creation via environment variables
- Environment-based configuration
- Health-checked Docker services
- Isolated test environment

## Running with Docker
### **1. Configure environment**
```bash
cp .env.example .env
```

Adjust values if needed.

Ensure:
```
POSTGRES_HOST=db
REDIS_HOST=redis
```

Also create your own secret key:
```bash
openssl rand -hex 32
```

### **2. Build and start services**
```bash
docker compose up --build
```

API will be available at:
```
http://localhost:8001
```

### **3. Build and start API**
```bash
docker compose up --build api
```

### **4. Run tests inside Docker**
```bash
docker compose run --rm tests
```

## Local running
### **1. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

### **2. Install dependencies**
```bash
pip install --upgrade pip
pip install .[dev]
```

### **3. Configure environment**
```bash
cp .env.example .env
```

Adjust values if needed.

Ensure:
```
POSTGRES_HOST=localhost
REDIS_HOST=localhost
```

Also create your own secret key:
```bash
openssl rand -hex 32
```

### **4. Run PostgreSQL and Redis**
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

```bash
sudo systemctl start redis
sudo systemctl status redis
```

### **5. Run migrations**
```bash
alembic upgrade head
```

### **6. Start development server**
```bash
uvicorn app.main:app --reload
```

### **7. Local testing**
```bash
pytest -v
```

## API documentation
FastAPI automatically generates interactive documentation:
- Swagger UI -> `http://local:8001/docs`
- ReDoc -> `http://local:8001/redoc`

## Screenshots
Running API using Docker:

![1_run_api_with_docker.png](images/1_run_api_with_docker.png)

Running tests using Docker:

![2_run_tests_with_docker.png](images/2_run_tests_with_docker.png)

Running API using uvicorn:

![3_run_api_with_uvicorn.png](images/3_run_api_with_uvicorn.png)

Running tests using locally:

![4_run_tests_locally.png](images/4_run_tests_locally.png)

All endpoints:

![5_all_endpoints.png](images/5_all_endpoints.png)

All schemas:

![6_all_schemas.png](images/6_all_schemas.png)

Health DB endpoint (for guests, authorized users and admins):

![7_health_db_endpoint.png](images/7_health_db_endpoint.png)

Health Redis endpoint (for guests, authorized users and admins):

![8_health_redis_endpoint.png](images/8_health_redis_endpoint.png)

Health full endpoint (for guests, authorized users and admins):

![9_health_full_endpoint.png](images/9_health_full_endpoint.png)

Register endpoint (for guests, authorized users and admins):

![10_register_endpoint.png](images/10_register_endpoint.png)

Login endpoint (for guests, authorized users and admins):

![11_login_endpoint.png](images/11_login_endpoint.png)

Refresh token endpoint (for guests, authorized users and admins):

![12_refresh_endpoint.png](images/12_refresh_endpoint.png)

Authorization (for guests, authorized users and admins):

![13_authorization.png](images/13_authorization.png)

Create category endpoint (for admins):

![14_create_category_endpoint.png](images/14_create_category_endpoint.png)

Get categories endpoint (for admins):

![15_get_categories_endpoint.png](images/15_get_categories_endpoint.png)

Update category endpoint (for admins):

![16_update_category_endpoint.png](images/16_update_category_endpoint.png)

Delete category endpoint (for admins):

![17_delete_category_endpoint.png](images/17_delete_category_endpoint.png)

Hard delete category endpoint (for admins):

![18_hard_delete_category_endpoint.png](images/18_hard_delete_category_endpoint.png)

Create post endpoint (for authorized users and admins):

![19_create_post_endpoint.png](images/19_create_post_endpoint.png)

Get posts endpoint (for guests, authorized users and admins):

![20_get_posts_endpoint.png](images/20_get_posts_endpoint.png)

Update post endpoint (for authorized authors and admins):

![21_update_post_endpoint.png](images/21_update_post_endpoint.png)

Delete post endpoint (for authorized authors and admins):

![22_delete_post_endpoint.png](images/22_delete_post_endpoint.png)

Hard delete post endpoint (for authorized authors and admins):

![23_hard_delete_endpoint.png](images/23_hard_delete_post_endpoint.png)

Create comment endpoint (for authorized authors and admins):

![24_create_comment_endpoint.png](images/24_create_comment_endpoint.png)

Get comments endpoint (for guests, authorized users and admins):

![25_get_comments_endpoint.png](images/25_get_comments_endpoint.png)

Update comment endpoint (for authorized authors and admins):

![26_update_comment_endpoint.png](images/26_update_comment_endpoint.png)

Delete comment endpoint (for authorized authors and admins):

![27_delete_comment_endpoint.png](images/27_delete_comment_endpoint.png)

Hard delete comment endpoint (for authorized authors and admins):

![28_hard_delete_comment_endpoint.png](images/28_hard_delete_comment_endpoint.png)

Get users endpoint (for admins):

![29_get_users_endpoint.png](images/29_get_users_endpoint.png)

Create admin endpoint (for admins):

![30_create_admin_endpoint.png](images/30_create_admin_endpoint.png)

Get user endpoint (for admins):

![31_get_user_endpoint.png](images/31_get_user_endpoint.png)

Update user endpoint (for admins):

![32_update_user_endpoint.png](images/32_update_user_endpoint.png)

Delete user endpoint (for admins):

![33_delete_user_endpoint.png](images/33_delete_user_endpoint.png)

Hard delete user endpoint (for admins):

![34_hard_delete_user_endpoint.png](images/34_hard_delete_user_endpoint.png)

Root endpoint (for guests, authorized users and admins):

![35_root_endpoint.png](images/35_root_endpoint.png)