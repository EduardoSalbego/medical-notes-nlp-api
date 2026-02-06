# Contribution Guide

## How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/medical-notes-nlp-api.git
cd medical-notes-nlp-api
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature
# or
git checkout -b fix/your-bug-fix
```

### 3. Develop

- Follow existing code standards
- Write tests for new features
- Update documentation when needed

### 4. Tests

#### Laravel

```bash
cd laravel-gateway
php artisan test
```

#### Python

```bash
cd ai-engine
pytest tests/ -v
```

### 5. Commit

```bash
git commit -m "feat: add new feature"
```

Please follow the commit pattern:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

### 6. Push and Pull Request

```bash
git push origin feature/your-feature
```

Open a Pull Request on GitHub.

---

## Code Standards

### PHP (Laravel)

- Use PSR-12
- Use type hints
- Document public methods
- Follow Laravel conventions

### Python

- Use PEP 8
- Maximum 120 characters per line
- Use type hints when possible
- Document functions and classes

---

## Test Structure

### Laravel

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class MedicalNoteTest extends TestCase
{
    public function test_can_process_medical_note(): void
    {
        // Test implementation
    }
}
```

### Python

```python
import pytest
from app.services.nlp_processor import NLPProcessor

def test_process_medical_note():
    processor = NLPProcessor()
    result = processor.process("Test note")
    assert "entities" in result
```

---

## Checklist Before Submitting a PR

- [ ] Code follows standards
- [ ] Tests are passing
- [ ] Documentation updated
- [ ] No lint errors
- [ ] Commit messages follow the standard
- [ ] No credentials in the code
