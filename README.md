# Secure Medical NLP Gateway

![PHP Version](https://img.shields.io/badge/php-8.2-777BB4.svg)
![Python Version](https://img.shields.io/badge/python-3.11-3776AB.svg)
![License](https://img.shields.io/badge/license-MIT-green)

A HIPAA-compliant, microservices-based system designed to process unstructured medical notes. It orchestrates a secure **Laravel Gateway** for governance and a **FastAPI/spaCy Engine** for Natural Language Processing (NER & Risk Classification).

---

## Architecture

The system follows a strict **Separation of Concerns** principle, isolating the heavy AI processing from the management/security layer.

```
graph LR
    Client[Client App] -->|HTTPS + Bearer Token| Gateway[Laravel Gateway]
    
    subgraph "Secure Zone (Laravel 11)"
        Gateway --> Auth[Sanctum Auth & RBAC]
        Auth --> Masking[Data Masking Service]
        Masking --> Audit[Audit Logger]
    end
    
    subgraph "AI Zone (Python FastAPI)"
        Masking -->|JSON (Anonymized)| AI[AI Engine]
        AI -->|SpaCy| NER[Entity Extraction]
        AI -->|Heuristic| Risk[Risk Classifier]
    end
    
    subgraph "Persistence"
        Gateway -->|AES-256 Encrypted| DB[(Postgres + pgvector)]
    end

    AI -->|Analysis Result| Gateway
```

## Tech Stack

### Gateway & Management Service
* **Framework:** Laravel 11
* **Authentication:** Laravel Sanctum
* **Testing:** Pest PHP
* **Documentation:** Swagger/OpenAPI

### AI Engine Microservice
* **Framework:** FastAPI (Python)
* **NLP Library:** spaCy (`pt_core_news_sm` / `en_core_web_sm`)
* **Validation:** Pydantic
* **Testing:** Pytest

### Infrastructure
* **Database:** PostgreSQL 16 with `pgvector` extension (ready for semantic search).
* **Containerization:** Docker & Docker Compose.
* **CI/CD:** GitHub Actions (Automated Testing, Linting, and Build).

---

## Getting Started

### Prerequisites
* Docker & Docker Compose
* Git

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/EduardoSalbego/medical-notes-nlp-api.git
    cd medical-notes-nlp-api
    ```

2.  **Start the environment (Docker)**
    This command will build both the Laravel and Python containers and start the database.
    ```bash
    docker-compose up -d --build
    ```

3.  **Setup Laravel**
    ```bash
    # Install dependencies
    docker exec -it medical_notes_laravel composer install
    
    # Run migrations and seeders
    docker exec -it medical_notes_laravel php artisan migrate --seed
    
    # Generate Encryption Keys
    docker exec -it medical_notes_laravel php artisan key:generate
    ```

4.  **Access the Application**
    * **Laravel API:** `http://localhost:8000`
    * **FastAPI Documentation:** `http://localhost:8001/docs`

---

## Project Status
* [X] Microservices Architecture Design
* [ ] CI/CD Pipeline Configuration
* [ ] Docker Infrastructure Setup
* [ ] AI Engine Implementation (NER)
* [ ] Laravel Gateway Implementation
* [ ] Security Layers (Masking & Encryption)

---

## 👤 Developed by

**Eduardo Salbego**
Last Year Software Engineering Student @ UNIPAMPA
