# Installation Guide - Medical Notes NLP API

This guide provides detailed instructions to install and configure the complete system.

---

## Prerequisites

### Required Software

1. **Docker & Docker Compose** (Recommended)
   - Docker Desktop: https://www.docker.com/products/docker-desktop
   - Or Docker Engine + Docker Compose

2. **Python 3.11+** (For local development)
   - Download: https://www.python.org/downloads/

3. **PHP 8.2+** (For local development)
   - Download: https://www.php.net/downloads.php

4. **Composer** (For Laravel)
   - Download: https://getcomposer.org/download/

5. **PostgreSQL 14+** (If not using Docker)
   - Download: https://www.postgresql.org/download/

---

## Installation with Docker (Recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd medical-notes-nlp-api
```

### Step 2: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit variables as needed
# DB_USER, DB_PASSWORD, DB_DATABASE
```

### Step 3: Start the Services

```bash
docker-compose up -d
```

This will:

- Download and start PostgreSQL with pgvector
- Build and start the AI Engine (FastAPI)
- Build and start the Laravel Gateway
- Configure all dependencies

### Step 4: Configure the Database

```bash
# Enter the Laravel container
docker exec -it medical_notes_laravel bash

# Run migrations and seeders
php artisan migrate
php artisan db:seed

# Exit container
exit
```

### Step 5: Verify Installation

- **Laravel Gateway**: http://localhost:8000
- **FastAPI AI Engine**: http://localhost:8001/docs
- **PostgreSQL**: localhost:5432

---

## Manual Installation (Development)

### AI Engine (Python)

```bash
cd ai-engine

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy models
python -m spacy download en_core_web_sm
python -m spacy download pt_core_news_sm

# Configure .env
cp .env.example .env
# Edit .env with your settings

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

### Laravel Gateway

```bash
cd laravel-gateway

# Install Composer dependencies
composer install

# Configure .env
cp .env.example .env

# Generate application key
php artisan key:generate

# Configure database in .env
# DB_CONNECTION=pgsql
# DB_HOST=localhost
# DB_PORT=5432
# DB_DATABASE=medical_notes_db
# DB_USERNAME=medical_user
# DB_PASSWORD=medical_pass
# AI_ENGINE_URL=http://localhost:8001

# Publish Spatie Permission (if needed)
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"

# Run migrations
php artisan migrate

# Run seeders
php artisan db:seed

# Start server
php artisan serve
```

---

## PostgreSQL Configuration with pgvector

If using PostgreSQL without Docker:

```sql
-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation
SELECT * FROM pg_extension WHERE extname = 'vector';
```

---

## Default Users

After running `php artisan db:seed`, the following users will be created:

- **Admin**: admin@medical-notes.local / password
- **Doctor**: doctor@medical-notes.local / password
- **User**: user@medical-notes.local / password

---

## Testing

### AI Engine Tests

```bash
cd ai-engine
pytest tests/ -v
```

### Laravel Tests

```bash
cd laravel-gateway
php artisan test
```

---

## Troubleshooting

### Error: "spaCy model not found"

```bash
cd ai-engine
python -m spacy download en_core_web_sm
python -m spacy download pt_core_news_sm
```

### Error: "Database connection failed"

1. Check if PostgreSQL is running
2. Verify credentials in `.env`
3. Make sure pgvector extension is installed

### Error: "AI Engine unreachable"

1. Check if AI Engine is running on port 8001
2. Verify `AI_ENGINE_URL` in Laravel `.env`
3. Test connection:

```bash
curl http://localhost:8001/health
```

### Error: "Permission denied" (Laravel storage)

```bash
cd laravel-gateway
chmod -R 775 storage
chmod -R 775 bootstrap/cache
```

---

## Next Steps

1. Read README.md to understand the architecture
2. Explore API documentation at http://localhost:8001/docs
3. Test requests using Postman or curl
4. Configure HTTPS for production
5. Set production environment variables

---

## Support

For issues or questions, please open an issue in the project repository.
