# API Documentation - Medical Notes NLP

## Endpoints

### Authentication

#### POST /register

Registers a new user.

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "password_confirmation": "password123"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "token": "1|xxxxxxxxxxxx"
}
```

#### POST /login

Authenticates a user.

**Request Body:**

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Logged in successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "token": "1|xxxxxxxxxxxx"
}
```

#### POST /logout

Logs out the current user.

**Headers:**

```
Authorization: Bearer {token}
```

**Response:**

```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

---

### Medical Notes Processing

#### POST /medical-notes/process

Processes a medical note and extracts entities.

**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "medical_note": "Patient presents high fever, headache, and dry cough. Prescribed Paracetamol 500mg every 6 hours. Diagnosis: Common flu.",
  "skip_masking": false
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "entities": {
      "symptoms": ["high fever", "headache", "dry cough"],
      "medications": ["Paracetamol 500mg"],
      "diagnoses": ["Common flu"]
    },
    "risk_classification": "moderate",
    "confidence_score": {
      "low": 0.1,
      "moderate": 0.7,
      "high": 0.15,
      "critical": 0.05
    },
    "processing_time_ms": 245.67,
    "language_detected": "en",
    "note_hash": "abc123def456",
    "masking_applied": true,
    "removed_entities": {
      "names": [],
      "ids": [],
      "emails": [],
      "phones": []
    },
    "processed_at": "2026-01-15T10:30:00.000000Z"
  },
  "processed_at": "2026-01-15T10:30:00.000000Z"
}
```

---

#### GET /medical-notes/history

Returns the user's processing history.

**Headers:**

```
Authorization: Bearer {token}
```

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "note_hash": "abc123def456",
      "entities": {
        "symptoms": ["high fever"],
        "medications": ["Paracetamol"],
        "diagnoses": ["Flu"]
      },
      "risk_classification": "moderate",
      "confidence_score": {...},
      "language_detected": "en",
      "processed_at": "2026-01-15T10:30:00.000000Z"
    }
  ]
}
```

---

#### GET /medical-notes/statistics

Returns user processing statistics.

**Headers:**

```
Authorization: Bearer {token}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "total_processed": 15,
    "by_risk_classification": {
      "low": 3,
      "moderate": 8,
      "high": 3,
      "critical": 1
    },
    "average_processing_time_ms": 234.56,
    "last_processed_at": "2026-01-15T10:30:00.000000Z"
  }
}
```

---

### User Profile

#### GET /user

Returns authenticated user information.

**Headers:**

```
Authorization: Bearer {token}
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "roles": ["user"],
  "permissions": ["process_medical_notes"]
}
```

---

## Risk Classification

The system classifies medical notes into four risk levels:

- **low**: Mild cases, common symptoms
- **moderate**: Moderate cases requiring attention
- **high**: Serious cases that may require immediate care
- **critical**: Critical cases requiring urgent attention

---

## Data Masking

By default, all medical notes go through a de-identification process that removes:

- **Personal IDs**
- **SSNs**
- **Emails**
- **Phone numbers**
- **Patient names**

You can disable masking by passing `"skip_masking": true` (not recommended for production).

---

## HTTP Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

---

## Usage Examples (cURL)

### Register User

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "password_confirmation": "password123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Process Medical Note

```bash
curl -X POST http://localhost:8000/medical-notes/process \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "medical_note": "Patient presents high fever and headache. Prescribed Paracetamol."
  }'
```

### Get History

```bash
curl -X GET http://localhost:8000/medical-notes/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Technical Notes

### Performance

- Average processing time: 200–500ms
- Asynchronous processing can be implemented for large volumes

### Limits

- Maximum note size: 10,000 characters
- Minimum size: 10 characters
- Rate limiting: Configurable via Laravel middleware

### Security

- All original notes are encrypted before storage
- Sensitive data is removed before NLP processing
- All requests are logged in audit logs
- Authentication tokens expire after inactivity
