# Fair Evaluator - Test Suite

## Setup

Per eseguire i test:

```bash
pip install pytest pytest-cov httpx
pytest tests/ -v --cov=src --cov-report=html
```

## Struttura Test

- `tests/test_api.py` - Test endpoint API
- `tests/test_crud.py` - Test CRUD operazioni
- `tests/test_models.py` - Test modelli database
- `tests/test_utils.py` - Test funzioni utility

## Coverage Target

Il target è 95% di coverage per:
- CRUD operations (Create, Read, Update, Delete)
- API endpoints
- Model serialization
- Error handling
- Import/Export Excel