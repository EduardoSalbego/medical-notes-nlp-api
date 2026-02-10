# Medical Notes NLP API - Medical Notes Processing System

A complete system for processing medical notes using NLP, with a separated architecture between the AI Engine (Python/FastAPI) and the Management Gateway (Laravel 11).

---

## Architecture

```

┌─────────────────┐
│  Laravel 11     │  ← Gateway & Management
│  (Sanctum/RBAC) │     - Authentication
│                 │     - Permission Control
│                 │     - Audit Logs
│                 │     - Data Masking
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI        │  ← AI Engine
│  (Python/NLP)   │     - NER (Symptoms, Medications, Diagnoses)
│                 │     - Risk Classification
│                 │     - NLP Processing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL     │
│  (pgvector)     │  ← Database
└─────────────────┘

```

---

## Features

- **NER (Named Entity Recognition)**: Extraction of symptoms, medications, and diagnoses
- **Risk Classification**: Automatic case severity categorization
- **Authentication**: Laravel Sanctum
- **RBAC**: Role-based access control (Spatie)
- **Audit Logs**: Full request logging (HIPAA-like)
- **Data Masking**: Automatic removal of sensitive data (De-identification)
- **Encryption**: Sensitive data encrypted before storage
- **Semantic Search**: PostgreSQL with pgvector

---

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- PHP 8.2+
- Composer
- Node.js & NPM (for frontend, if needed)

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd medical-notes-nlp-api
```

### 2. Configure environment variables

```bash
cp .env.example .env
cp ai-engine/.env.example ai-engine/.env
```

### 3. Start services with Docker Compose

```bash
docker-compose up -d
```

### 4. Set up Laravel

```bash
cd laravel-gateway
composer install
php artisan key:generate
php artisan migrate
php artisan db:seed
```

### 5. Set up the Python AI Engine

```bash
cd ai-engine
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## Usage

### API Documentation

- Laravel Gateway: http://localhost:8000/api/documentation
- FastAPI AI Engine: http://localhost:8001/docs

### Request Example

```bash
POST http://localhost:8000/api/v1/medical-notes/process
Authorization: Bearer {token}
Content-Type: application/json

{
  "medical_note": "Patient presents high fever, headache, and dry cough. Prescribed Paracetamol 500mg every 6 hours. Diagnosis: Common flu."
}
```

### Response

```bash
{
  "status": "success",
  "data": {
    "entities": {
      "symptoms": ["high fever", "headache", "dry cough"],
      "medications": ["Paracetamol 500mg"],
      "diagnoses": ["Common flu"]
    },
    "risk_classification": "moderate",
    "confidence_score": 0.92,
    "processed_at": "2026-01-15T10:30:00Z",
    "note_id": "masked_identifier"
  }
}
```

---

## Security

- **Encryption**: All sensitive data is encrypted using AES-256
- **Data Masking**: Names, personal IDs, and identifiers are removed before NLP processing
- **Audit Logs**: All operations are logged for compliance
- **RBAC**: Granular role-based permission control

---

## Testing

```bash
# Laravel
cd laravel-gateway
php artisan test

# Python
cd ai-engine
pytest
```

---

## Project Structure

```
medical-notes-nlp-api/
├── ai-engine/                  # Python FastAPI
│   ├── app/
│   ├── tests/
│   └── requirements.txt
│
├── laravel-gateway/            # Laravel 11
│   ├── app/
│   ├── database/
│   └── tests/
│
├── frontend/                   # Vue.js 3 + Vite (UI)
│   ├── src/
│   │   ├── views/
│   │   └── App.vue
│   └── vite.config.js
│
├── nginx/                      # Web Server Configuration
│   └── nginx.conf              # Reverse Proxy
│
├── .github/
│   └── workflows/              # CI/CD Pipelines
│
├── docs/                       # Project Documentation
│
├── docker-compose.yml
│
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## CI/CD

The project includes a GitHub Actions pipeline for:

- Automated testing
- Code quality checks (Linting)
- Build and deployment

---

## Developed by

**Eduardo Salbego** Software Engineering Student | Final Year / 9th Semester @ UNIPAMPA
