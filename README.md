# Secure Medical NLP Gateway & Processing Pipeline

[![Laravel 11](https://img.shields.io/badge/Gateway-Laravel%2011-red)](https://laravel.com)
[![FastAPI](https://img.shields.io/badge/AI%20Engine-FastAPI%20%2F%20Python-005571?logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Environment-Docker%20%2F%20Orchestration-blue?logo=docker)](https://www.docker.com)
[![CI/CD](https://img.shields.io/badge/Pipeline-GitHub%20Actions-2088FF?logo=githubactions)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

An enterprise-grade, highly decoupled **Healthcare Data Ingestion & NLP Pipeline**. The architecture isolates an AI Processing Engine powered by **Python (FastAPI & spaCy)** from a secure Management Gateway built with **Laravel 11 (Sanctum & Spatie RBAC)**. 

The system is designed with a compliance-first approach mimicking HIPAA security standards, featuring automated PHI (Protected Health Information) de-identification, application-level AES-256 database encryption at rest, comprehensive compliance audit logging, and structured relational persistence powered by **PostgreSQL**.

---

## Architectural Topology

The monorepo enforces a strict separation of concerns, ensuring the heavy NLP compute workloads are isolated from user authentication, rate limiting, and compliance workflows:

```

   ┌─────────────────────────────────┐
   │    Laravel 11 Security Gateway  │  ← Ingestion & Compliance Layer
   │  - Stateless Sanctum Auth       │    - Symmetric Data Masking (PHI De-identification)
   │  - RBAC (Granular Permissions)  │    - AES-256 Data Encryption at Rest
   │  - Compliance Audit Trail       │    - Reverse Proxying & Upstream Rate Limiting
   └────────────────┬────────────────┘
                    │
                    ▼ Upstream REST Call (Stateless JSON Payload)
   ┌─────────────────────────────────┐
   │    FastAPI NLP Inference Engine │  ← Machine Learning Layer
   │  - Named Entity Recognition     │    - spaCy Pipeline Extraction
   │  - Medical Risk Classification  │    - Multi-Class Clinical Severity Indexing
   │  - Dynamic Confidence Scoring   │    - Asynchronous High-Throughput Handlers
   └────────────────┬────────────────┘
                    │
                    ▼ Data Persistence
   ┌─────────────────────────────────┐
   │    PostgreSQL                   │  ← Relational Storage Layer
   │  - Encrypted Note Payload Blobs │    - Relational Entity Indexing
   │  - Extracted Clinical Entities  │    - Fast Metadata Queries
   └─────────────────────────────────┘

```

---

## Core Engineering Features

### Clinical Named Entity Recognition (NER)
Utilizes custom NLP pipelines to parse unstructured medical text and extract high-value clinical entities including **Symptoms/Clinical Signs**, **Medications/Dosages**, and **Diagnoses** with strict confidence token scoring.

### Automated Severity Triaging (Risk Classification)
Processes extracted metadata through custom heuristic layers to categorize incoming patient notes into multi-class urgency indexes (`low`, `moderate`, `critical`), facilitating automated queue prioritization.

### Compliance-Driven De-Identification (Data Masking)
A compliance-first pipeline that systematically strips out or masks names, social identifiers, and sensitive timestamps before passing payload packages downstream to the AI inference layers.

### Cryptographic Encryption at Rest & Flight
Protects sensitive medical note content using application-level AES-256 encryption prior to database writes. All transit packets move strictly over authenticated bearer token channels managed by Laravel Sanctum.

### Comprehensive Compliance Audit Logging
Generates structured audit records capturing every microservice hit, user mutations, and inference executions, ensuring complete operational tracking accountability.

### Relational Data Storage & Indexing
Leverages PostgreSQL to store encrypted clinical note payloads, extracted entities, and historical risk classification statistics efficiently.

---

## Technical Stack Mappings

| Architecture Layer | Component Stack Elements |
|---|---|
| **API Management Gateway** | Laravel 11 (PHP 8.2), Laravel Sanctum, Spatie Laravel Permission |
| **Inference Machine Learning** | Python 3.11+, FastAPI, spaCy (Advanced NLP Framework) |
| **User Interface (UI)** | Vue.js 3, Vite, Axios Client |
| **Data Architecture** | PostgreSQL, AES-256 Crypto Drivers |
| **Orchestration & DevOps** | Nginx (Reverse Proxy), Docker, Docker Compose, GitHub Actions |
| **Quality & Assurance Suite** | PHPUnit (Backend Tests), PyTest (Inference Engine Profiling) |

---

## Setting Up the Local Topology

### Infrastructure Requirements
- Docker Engine & Docker Compose V2 running locally.
- Active package access for Composer and Python Virtual Environments (`venv`).

### Ingestion Steps

```bash
# 1. Clone the structural repository
git clone <repository-url>
cd medical-notes-nlp-api

# 2. Replicate downstream environment schemas
cp laravel-gateway/.env.example lara-gateway/.env
cp ai-engine/.env.example ai-engine/.env

# 3. Boot environment up via Docker Compose
docker-compose up -d --build

# 4. Bootstrap the Laravel Security Gateway
cd laravel-gateway
composer install
php artisan key:generate
php artisan migrate --seed

# 5. Initialize the Isolated Inference Environment
cd ../ai-engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## API Contracts & Execution Mappings

### Upstream Swagger & OpenAPI Visualizers
- **Security Gateway Playground:** `http://localhost:8000/api/documentation`
- **FastAPI Core Engine Docs:** `http://localhost:8001/docs`

### Clinical Processing Transaction Sample

```bash
POST http://localhost:8000/api/v1/medical-notes/process
Authorization: Bearer 3|vN4kRLXv9YmJ...
Content-Type: application/json

{
  "medical_note": "Patient presents high fever, headache, and dry cough. Prescribed Paracetamol 500mg every 6 hours. Diagnosis: Common flu."
}
```

### Response Payload Structure

```json
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
    "note_id": "crypto_masked_identifier_hash"
  }
}
```

---

## Operational Test Suites

Verify architectural contract execution boundaries by deploying the dual testing stacks:

```bash
# Execute Laravel Gateway Integration Tests
cd laravel-gateway
php artisan test

# Execute Python Inference Engine Unit Tests
cd ai-engine
pytest
```

---

## Author & System Architect

**Eduardo Salbego**  
Software Engineer — Specialized in Secure Backend Architecture & Applied AI  
Let's connect: [LinkedIn](https://www.linkedin.com/in/eduardo-salbego/)
