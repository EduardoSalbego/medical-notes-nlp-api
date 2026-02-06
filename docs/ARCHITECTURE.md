# System Architecture - Medical Notes NLP API

## Overview

The system is designed with a microservices architecture, clearly separating responsibilities between the AI Engine and the management/governance layer.

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                     │
│              (Web, Mobile, Third-party APIs)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Laravel Gateway (Port 8000)                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Authentication & Authorization (Sanctum + RBAC)    │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Request Validation & Rate Limiting                 │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Data Masking (De-identification)                   │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Encryption Service                                 │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Audit Logging (HIPAA-like)                          │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Request
                       │ (Masked Data)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI AI Engine (Port 8001)                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  NLP Processing (spaCy + Transformers)               │    │
│  │  - Named Entity Recognition (NER)                    │    │
│  │  - Risk Classification                              │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Language Detection (EN/PT)                          │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Response Processing                                 │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL + pgvector (Port 5432)               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Medical Notes (Encrypted)                           │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Audit Logs                                          │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Users, Roles, Permissions                           │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Semantic Search (pgvector)                          │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Laravel Gateway (Management Layer)

**Technologies:**

- Laravel 11
- Laravel Sanctum (Authentication)
- Spatie Permission (RBAC)
- Guzzle HTTP (HTTP Client)

**Responsibilities:**

- User authentication and authorization
- Request validation
- Data masking (remove PII before processing)
- Sensitive data encryption
- Audit logging (HIPAA-like compliance)
- Rate limiting and abuse protection
- REST API exposure for clients

**Data Flow:**

1. Receives client request
2. Authenticates user (Sanctum token)
3. Checks permissions (RBAC)
4. Validates input data
5. Applies data masking (removes PII)
6. Registers audit log
7. Forwards to AI Engine
8. Receives processed result
9. Encrypts original note
10. Saves to database
11. Returns response to client

---

### 2. FastAPI AI Engine (AI Engine)

**Technologies:**

- FastAPI
- spaCy (NLP)
- Transformers (Hugging Face) - optional
- SQLAlchemy (ORM)
- Pydantic (Validation)

**Responsibilities:**

- NLP processing of medical notes
- Named Entity Recognition (NER):
  - Symptoms
  - Medications
  - Diagnoses
- Risk classification:
  - Low, Moderate, High, Critical
- Language detection (EN/PT)
- Confidence score calculation

**NLP Models:**

- **English**: `en_core_web_sm` (spaCy)
- **Portuguese**: `pt_core_news_sm` (spaCy)

**Processing Flow:**

1. Receives masked text
2. Detects language
3. Processes with spaCy
4. Extracts entities using regex + NER
5. Classifies risk based on keywords and context
6. Returns structured JSON

---

### 3. PostgreSQL + pgvector

**Technologies:**

- PostgreSQL 14+
- pgvector extension

**Data Schema:**

- `users`: System users
- `medical_notes`: Processed notes (encrypted data)
- `audit_logs`: Audit records
- `roles`, `permissions`, `model_has_roles`: RBAC (Spatie)

**pgvector:**

- Enables semantic search for medical notes
- Stores text embeddings
- Helps find similar notes

---

## End-to-End Processing Flow

### Example: Processing a Medical Note

1. **Client** → POST `/api/v1/medical-notes/process`

   ```json
   {
     "medical_note": "Patient John Doe, ID 123456, presents fever..."
   }
   ```

2. **Laravel Gateway**:
   - Authenticates token
   - Checks `process_medical_notes` permission
   - Validates payload
   - **Data Masking**:
     ```json
     {
       "medical_note": "Patient [PATIENT_NAME], ID [ID], presents fever..."
     }
     ```
   - Logs audit event
   - Sends to AI Engine

3. **AI Engine**:
   - Detects language: EN
   - Processes with spaCy
   - Extracts entities
   - Classifies risk: "moderate"
   - Returns JSON

4. **Laravel Gateway**:
   - Receives result
   - Encrypts original note
   - Saves to database
   - Returns response

5. **Client** receives:
   ```json
   {
     "status": "success",
     "data": {
       "entities": {...},
       "risk_classification": "moderate"
     }
   }
   ```

---

## Security

### Security Layers

1. **Authentication**: Sanctum tokens (Bearer tokens)
2. **Authorization**: RBAC with Spatie Permission
3. **Encryption**: AES-256 for sensitive data
4. **Data Masking**: PII removal before processing
5. **Audit Logs**: Full activity logging
6. **Rate Limiting**: Abuse protection
7. **Validation**: Strict input validation

### Compliance (HIPAA-like)

- **Audit Trails**: All actions are logged
- **Access Control**: Granular RBAC
- **Data Encryption**: Sensitive data encrypted
- **De-identification**: PII removed
- **Data Retention**: Configurable

---

## Scalability

### Horizontal Scaling

- **Laravel Gateway**: Multiple instances behind load balancer
- **AI Engine**: Stateless instances
- **PostgreSQL**: Read replicas

### Optimizations

- **Cache**: Redis for frequent data
- **Queue**: Asynchronous processing (Laravel Queue)
- **CDN**: For static assets (if applicable)

---

## Monitoring

### Logs

- **Laravel**: `storage/logs/laravel.log`
- **Audit**: `storage/logs/audit.log`
- **FastAPI**: Python logging

### Metrics

- Processing time
- Error rate
- Resource usage
- Request volume

---

## DevOps

### Docker Compose

All services run in containers:

- `medical_notes_postgres`
- `medical_notes_ai_engine`
- `medical_notes_laravel`
- `medical_notes_nginx` (optional)

### CI/CD

GitHub Actions pipeline:

- Automated tests (Laravel + Python)
- Python linting
- Docker image builds
- Deployment (configurable)

---

## Production Considerations

1. Enable HTTPS (SSL/TLS)
2. Use secrets manager for environment variables
3. Automated PostgreSQL backups
4. Application Performance Monitoring (APM)
5. Proper rate limiting
6. Database firewall rules
7. Secrets management (do not commit credentials)
8. Health check endpoints
9. Centralized logging (ELK, CloudWatch, etc.)
10. Alerting for critical errors
