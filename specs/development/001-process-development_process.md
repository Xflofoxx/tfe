# Processi di Sviluppo e Delivery

## 1. Git Workflow

### 1.1 Branch Strategy

```
main (production-ready)
  ↑
  ↑
develop (integration)
  ↑
  ↑
feature/xxx (feature development)
  ↑
  ↑
hotfix/xxx (urgent fixes)
```

### 1.2 Naming Convention

- **Feature**: `feature/<ticket>-<description>` (es. `feature/001-add-ocr`)
- **Bugfix**: `bugfix/<ticket>-<description>` (es. `bugfix/002-fix-upload-error`)
- **Hotfix**: `hotfix/<ticket>-<description>` (es. `hotfix/003-security-patch`)
- **Refactor**: `refactor/<ticket>-<description>` (es. `refactor/004-clean-models`)

### 1.3 Commit Messages

Formato: `<type>(<scope>): <subject>`

Tipi:
- `feat`: Nuova funzionalità
- `fix`: Bug fix
- `refactor`: Refactoring
- `docs`: Documentazione
- `test`: Test
- `chore`: Manutenzione

Esempi:
```
feat(fairs): add pagination to list endpoint
fix(analyze): handle empty scraped data gracefully
refactor(models): add indexes to frequently queried fields
docs(readme): update installation instructions
```

### 1.4 PR Requirements

- [ ] Code segue style guide
- [ ] Test passano
- [ ] Coverage >= 80%
- [ ] Linting passa
- [ ] Documentazione aggiornata
- [ ] Almeno una review approvata

---

## 2. Continuous Integration

### 2.1 Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Run linter
        run: ruff check src/
        
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
        
      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

---

## 3. Release Management

### 3.1 Versioning

Formato: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: Nuove funzionalità (backward compatible)
- **PATCH**: Bug fix

### 3.2 Milestones

#### v1.0.0 - MVP (Current)
**Target**: 2026-04-30

Features:
- [x] CRUD fiere
- [x] Web scraping base
- [x] Upload allegati
- [x] Valutazione LLM base
- [x] Report HTML
- [x] Import/Export Excel
- [x] Test coverage >= 60%

#### v1.1.0 - Enhanced Analysis
**Target**: 2026-05-31

Features:
- [ ] OCR per immagini
- [ ] Analisi PDF avanzata
- [ ] Report PDF
- [ ] Dashboard stats avanzate
- [ ] Test coverage >= 75%

#### v1.2.0 - Enterprise
**Target**: 2026-07-31

Features:
- [ ] Autenticazione
- [ ] Multi-tenant
- [ ] Backup automatico
- [ ] API rate limiting
- [ ] Test coverage >= 85%

#### v2.0.0 - Production
**Target**: 2026-09-30

Features:
- [ ] Deploy container (Docker)
- [ ] CI/CD pipeline
- [ ] Monitoring
- [ ] Test coverage >= 95%

---

## 4. Code Quality Gates

### 4.1 Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
      - id: ruff-format
      
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### 4.2 Quality Thresholds

| Metrica | Min | Target |
|---------|-----|--------|
| Test Coverage | 60% | 80% |
| Linting Errors | 0 | 0 |
| Code Complexity | - | < 15 |

---

## 5. Documentation Standards

### 5.1 Required Documentation

- README.md: Installazione e usage
- SPEC.md: Specifiche funzionali
- API.md: Documentazione endpoint (OpenAPI)
- CHANGELOG.md: Cronologia versioni

### 5.2 Inline Documentation

- Docstrings per tutte le funzioni pubbliche
- Commenti per logica complessa
- Type hints obbligatori