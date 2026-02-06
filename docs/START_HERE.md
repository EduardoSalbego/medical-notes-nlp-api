# Start Here — Medical Notes NLP API

This is a complete medical notes processing system using NLP, built according to all project specifications.

---

## What Has Been Implemented

**AI Engine (Python + FastAPI)**

- NLP processing with spaCy
- Entity extraction (symptoms, medications, diagnoses)
- Risk classification
- Portuguese and English support

**Laravel Gateway**

- Authentication with Sanctum
- RBAC with Spatie Permission
- Data masking (de-identification)
- Sensitive data encryption
- Audit logs (HIPAA-like)

**Infrastructure**

- Docker Compose for all services
- PostgreSQL with pgvector
- CI/CD with GitHub Actions
- Complete documentation

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Enter the project directory
cd medical-notes-nlp-api

# 2. Copy the environment file
cp .env.example .env

# 3. Start services
docker-compose up -d

# 4. Configure the database
docker exec -it medical_notes_laravel php artisan migrate --force
docker exec -it medical_notes_laravel php artisan db:seed --force

# 5. Test it!
curl http://localhost:8000
```

---

### Option 2: Manual Setup

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

---

## Documentation

- **[README.md](../README.md)** — Project overview
- **[INSTALLATION.md](INSTALLATION.md)** — Full installation guide
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** — API reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System architecture
- **[QUICKSTART.md](QUICKSTART.md)** — 5-minute setup guide

---

## Quick Test

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"password123","password_confirmation":"password123"}'
```

---

### 2. Login (or use admin account)

```bash
curl -X POST http://localhost:8000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@medical-notes.local","password":"password"}'
```

---

### 3. Process a Medical Note

```bash
curl -X POST http://localhost:8000/api/v1/medical-notes/process \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"medical_note":"Patient presents with high fever and headache. Prescribed Paracetamol."}'
```

---

## Default Users

After running `php artisan db:seed`:

- **Admin**: admin@medical-notes.local / password
- **Doctor**: doctor@medical-notes.local / password
- **User**: user@medical-notes.local / password

---

## Main Endpoints

- **Laravel Gateway**: http://localhost:8000
- **FastAPI Docs**: http://localhost:8001/docs
- **PostgreSQL**: localhost:5432

---

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart
docker-compose restart

# Run tests
docker exec -it medical_notes_laravel php artisan test
docker exec -it medical_notes_ai_engine pytest tests/ -v
```

---

## Important Notes

- All medical notes are encrypted before storage
- PII (CPF, emails, etc.) is removed before NLP processing
- All actions are recorded in audit logs

---

## Need Help?

Check:

- [INSTALLATION.md](INSTALLATION.md) — Troubleshooting section
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) — API issues
- Container logs: `docker-compose logs`

---
