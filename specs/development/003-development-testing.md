# Specifica: Testing Suite - Quality Assurance

## Panoramica

Suite di test completa per garantire qualità e affidabilità del sistema TFE.

## 1. Architettura Testing

### 1.1 Framework
- **pytest**: Framework principale
- **FastAPI TestClient**: Test API endpoints
- **SQLAlchemy**: Test database operations
- **unittest.mock**: Mocking dependencies esterne

### 1.2 Organizzazione File
```
tests/
├── test_api.py      # Test API endpoints
├── test_model.py    # Test modelli dati
├── README.md        # Documentazione test
└── __pycache__/     # Cache Python
```

### 1.3 Environment
- **Database**: SQLite in-memory per test
- **Isolation**: Ogni test ha database pulito
- **Mocking**: Servizi esterni (Ollama, HTTP requests)

## 2. Test API (test_api.py)

### 2.1 Setup
```python
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create test database tables."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Clean database session per test."""
    # Cleanup after each test
```

### 2.2 Coverage Target: 95%

**Endpoint Testati**:

#### Fiere CRUD
- `POST /api/fairs` - Creazione singola
- `POST /api/fairs/bulk` - Creazione multipla
- `GET /api/fairs` - Lista fiere
- `GET /api/fairs/{id}` - Dettaglio fiera
- `PUT /api/fairs/{id}` - Aggiornamento
- `DELETE /api/fairs/{id}` - Eliminazione

#### Tag Management
- `GET /api/tags` - Lista tag
- `POST /api/tags` - Crea/ottieni (deduplicazione)
- `PUT /api/tags/{id}` - Aggiorna tag
- `DELETE /api/tags/{id}` - Elimina tag
- `POST /api/tags/merge` - Merge duplicati
- `POST /api/tags/bulk` - Creazione multipla

#### Analisi e Componenti
- `GET /api/fairs/{id}/analyses` - Lista analisi
- `POST /api/fairs/{id}/analyses` - Crea analisi
- `DELETE /api/fairs/{id}/analyses/{id}` - Elimina analisi
- `GET /api/fairs/{id}/components` - Lista componenti
- `POST /api/fairs/{id}/components` - Crea componente
- `PUT /api/fairs/{id}/components/{id}` - Aggiorna componente
- `DELETE /api/fairs/{id}/components/{id}` - Elimina componente

#### Proposte Commerciali
- `POST /api/fairs/{id}/proposals` - Upload proposta
- `GET /api/fairs/{id}/proposals` - Lista proposte
- `DELETE /api/fairs/{id}/proposals/{id}` - Elimina proposta

#### Impostazioni
- `GET /api/settings` - Ottieni impostazioni
- `PUT /api/settings` - Aggiorna impostazioni

### 2.3 Test Patterns

#### Happy Path Tests
```python
def test_create_fair_success():
    response = client.post("/api/fairs", json=sample_fair_data)
    assert response.status_code == 200
    assert "id" in response.json()
```

#### Error Handling Tests
```python
def test_create_fair_invalid_url():
    invalid_data = sample_fair_data.copy()
    invalid_data["fair_url"] = "invalid-url"
    response = client.post("/api/fairs", json=invalid_data)
    assert response.status_code == 422  # Validation error
```

#### Edge Cases
- URL duplicate
- Campi required mancanti
- Relazioni m:n (tag, contatti)
- File upload validation

## 3. Test Modelli (test_model.py)

### 3.1 Database Schema Tests
- **Table Creation**: Verifica creazione tabelle
- **Relationships**: Test foreign keys e constraints
- **Indexes**: Verifica performance indexes
- **Data Types**: Validazione tipi colonna

### 3.2 Model Methods Tests
- **Tag Deduplication**: `find_or_create_tag()`
- **Tag Conversion**: `convert_fair_data_to_tags()`
- **Validation**: Required fields, unique constraints

### 3.3 Business Logic Tests
- **Fair Status Workflow**: Transizioni stato valide
- **Tag Analytics**: Tracking creazione/uso tag
- **Settings Defaults**: Valori default corretti

## 4. Test Automation

### 4.1 CI/CD Integration
```bash
# In CI pipeline
pytest tests/ --cov=src/fair_evaluator --cov-report=html --cov-fail-under=95
```

### 4.2 Coverage Requirements
- **Line Coverage**: ≥95%
- **Branch Coverage**: ≥90%
- **Function Coverage**: 100% funzioni critiche

### 4.3 Test Data
- **Fixtures**: Dati di test riutilizzabili
- **Factories**: Generatori dati fake
- **Cleanup**: Database reset tra test

## 5. Test Categories

### 5.1 Unit Tests
- Funzioni isolate
- Mock dependencies
- Fast execution (<100ms per test)

### 5.2 Integration Tests
- API endpoints completi
- Database operations
- External service mocks

### 5.3 End-to-End Tests
- Workflow completi (creazione → analisi → report)
- UI interactions (future)
- Performance validation

## 6. Quality Gates

### 6.1 Pre-commit Hooks
- **ruff check**: Linting
- **ruff format**: Code formatting
- **pytest**: Unit tests
- **Coverage check**: Minimum threshold

### 6.2 CI Pipeline
- **Build**: Python syntax check
- **Test**: Full test suite
- **Security**: Dependency scanning
- **Performance**: Response time validation

## 7. Test Documentation

### 7.1 README.md
- Come eseguire test
- Coverage report
- Troubleshooting

### 7.2 Test Naming Convention
```python
def test_{feature}_{scenario}_{expected_result}():
    # e.g., test_fair_creation_success
    # e.g., test_tag_merge_duplicates
```

### 7.3 Assertions Best Practices
- **Descriptive messages**: `assert condition, "Clear failure description"`
- **Multiple assertions**: Test aspetti diversi separatamente
- **Edge cases**: Test boundaries e corner cases

## 8. Future Enhancements

### 8.1 UI Testing
- Selenium/Playwright per test interfaccia
- Visual regression testing
- Accessibility testing

### 8.2 Performance Testing
- Load testing API endpoints
- Database query optimization
- Memory usage monitoring

### 8.3 Security Testing
- Input validation fuzzing
- SQL injection prevention
- Authentication/authorization tests
</content>
<parameter name="filePath">c:\Sviluppo\TFE-Trade fair evaluator\specs\development\003-development-testing.md