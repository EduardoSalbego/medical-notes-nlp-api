# Quick Start Guide

## Get Started in 5 Minutes

---

### 1. Prerequisites

Make sure you have installed:

- Docker & Docker Compose
- Git

---

### 2. Clone and Configure

```bash
# Clone the repository
git clone <repository-url>
cd medical-notes-nlp-api

# Copy environment file
cp .env.example .env
```

---

### 3. Start with Docker

```bash
# Start all services
docker-compose up -d

# Wait a few seconds for services to initialize
# Check logs
docker-compose logs -f
```

---

### 4. Configure the Database

```bash
# Run migrations and seeders
docker exec -it medical_notes_laravel php artisan migrate --force
docker exec -it medical_notes_laravel php artisan db:seed --force
```

---

### 5. Test the API

#### 5.1 Register a User

```bash
curl -X POST http://localhost:8000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "password_confirmation": "password123"
  }'
```

---

#### 5.2 Login

```bash
curl -X POST http://localhost:8000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@medical-notes.local",
    "password": "password"
  }'
```

Save the returned token for the next steps.

---

#### 5.3 Process a Medical Note

```bash
curl -X POST http://localhost:8000/api/v1/medical-notes/process \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "medical_note": "Patient presents with high fever, headache, and dry cough. Prescribed Paracetamol 500mg every 6 hours. Diagnosis: Common flu."
  }'
```

---

#### 5.4 View History

```bash
curl -X GET http://localhost:8000/api/v1/medical-notes/history \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

### 6. Access Documentation

- **FastAPI Docs**: http://localhost:8001/docs
- **Laravel Gateway**: http://localhost:8000

---

## Test Users

After running the seeder, you can use:

- **Admin**: admin@medical-notes.local / password
- **Doctor**: doctor@medical-notes.local / password
- **User**: user@medical-notes.local / password

---

## Next Steps

1. Read the [Full API Documentation](API_DOCUMENTATION.md)
2. Check the [Installation Guide](INSTALLATION.md) for advanced setup
3. Explore the source code to understand the architecture
4. Configure for production (HTTPS, secure environment variables)

---

## Quick Troubleshooting

### Services Not Starting?

```bash
docker-compose down
docker-compose up -d
docker-compose logs
```

---

### Permission Errors?

```bash
docker exec -it medical_notes_laravel chmod -R 775 storage bootstrap/cache
```

---

### Database Connection Issues?

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Verify environment variables
docker exec -it medical_notes_laravel php artisan config:show database
```

---

### AI Engine Not Responding?

```bash
# Check logs
docker logs medical_notes_ai_engine

# Test directly
curl http://localhost:8001/health
```

---

## Sample Medical Notes for Testing

### Portuguese

```
Paciente apresenta febre alta, dor de cabeça intensa e tosse seca persistente.
Relatou início dos sintomas há 3 dias. Prescrito Paracetamol 500mg a cada 6 horas
e Ibuprofeno 400mg caso a dor persista. Diagnóstico: Síndrome gripal.
```

---

### English

```
Patient presents with high fever, severe headache, and persistent dry cough.
Symptoms started 3 days ago. Prescribed Paracetamol 500mg every 6 hours and
Ibuprofen 400mg if pain persists. Diagnosis: Flu-like syndrome.
```

---

### High-Risk Case

```
Patient presents with severe chest pain, shortness of breath, and sweating.
Symptoms started 30 minutes ago. High blood pressure.
Referred to emergency care. Suspected acute myocardial infarction.
```

---
