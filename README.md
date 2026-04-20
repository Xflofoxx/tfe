# TFE - Trade Fair Evaluator

## Descrizione

Applicazione web per valutare se partecipare a fiere commerciali, con analisi automatica tramite web scraping e LLM locale (Ollama).

**Versione**: 1.0.0
**Target Utenti**: Responsabili marketing, event manager, PM di PMI che valutano partecipazione a fiere B2B.

## Funzionalità Principali

### Gestione Fiere (CRUD)
- Creazione fiere da URL con analisi automatica
- Aggiornamento e gestione stato workflow
- Import/Export Excel
- Calendario annuale con visualizzazione stati

### Analisi Automatica
- Web scraping con BeautifulSoup
- Estrazione dati strutturata con Ollama LLM
- Valutazione ROI con prompt personalizzati
- Generazione report HTML/PDF

### Caricamento Allegati
- Upload PDF, immagini, documenti
- Estrazione testo automatica
- Supporto OCR per immagini

### Sistema Tag
- Tag categorizzati (settore, profilo visitatori, categorie prodotto)
- Gestione CRUD con interfaccia dedicata
- Deduplicazione automatica

## Stack Tecnologico

- **Backend**: Python 3.13+, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Bootstrap 5, Jinja2 templates
- **AI**: Ollama (llama3.2), supporto ChatGPT/Copilot
- **Documenti**: OpenPyXL (Excel), PyMuPDF (PDF), WeasyPrint (PDF generation)

## Installazione

### Prerequisiti
- Python 3.13+
- Ollama installato (opzionale, per AI locale)

### Setup
```bash
# Clona repository
git clone <repository-url>
cd TFE-Trade-fair-evaluator

# Installa dipendenze
pip install -r requirements.txt

# Avvia server
python -m uvicorn src.fair_evaluator.main:app --reload --port 8000
```

### Configurazione Ollama (Opzionale)
```bash
# Installa Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Scarica modello
ollama pull llama3.2

# Configura in settings: http://localhost:11434
```

## Utilizzo

### Flusso Principale
1. Vai su `/fairs/new`
2. Inserisci URL fiera
3. Clicca "Genera Prompt" → copia prompt
4. Incolla in ChatGPT/Copilot o usa Ollama locale
5. Copia JSON risposta → incolla in "Estrai Dati"
6. Campi compilati automaticamente

### Workflow Stati
```
in_valutazione → approvata → in_gestione → conclusa
                 ↓
               rifiutata
```

## API Principali

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/fairs` | GET | Lista fiere (paginata) |
| `/api/fairs` | POST | Crea fiera |
| `/api/fairs/{id}/analyze` | POST | Avvia analisi web |
| `/api/fairs/{id}/evaluate` | POST | Valuta con LLM |
| `/api/fairs/{id}/report` | POST | Genera report |
| `/api/settings` | GET/POST | Gestione impostazioni |
| `/api/upload-pdf` | POST | Upload allegati |
| `/api/export-excel` | GET | Esporta dati Excel |

## Documentazione

### Specifiche

**Organizzate per area funzionale:**

**Main:**
- [main/001-main-project_overview.md](specs/main/001-main-project_overview.md) - Panoramica progetto

**Core (Fairs & Tags):**
- [core/002-fairs-management.md](specs/core/002-fairs-management.md) - CRUD operations fiere
- [core/003-fairs-evaluation.md](specs/core/003-fairs-evaluation.md) - Workflow valutazione AI
- [core/004-fairs-creation.md](specs/core/004-fairs-creation.md) - UI creazione fiere
- [core/008-fairs-detail-page.md](specs/core/008-fairs-detail-page.md) - Pagina dettaglio fiera
- [core/001-tags-tag_system.md](specs/core/001-tags-tag_system.md) - Sistema tag base
- [core/007-tags-expansion.md](specs/core/007-tags-expansion.md) - Tag avanzati e analytics

**UI:**
- [ui/005-homepage-dashboard.md](specs/ui/005-homepage-dashboard.md) - Dashboard principale

**System:**
- [system/006-settings-management.md](specs/system/006-settings-management.md) - Configurazioni sistema

**Development:**
- [development/001-development-functional_spec.md](specs/development/001-development-functional_spec.md) - Specifica funzionale
- [development/001-process-development_process.md](specs/development/001-process-development_process.md) - Processi sviluppo

**Agent:**
- [agent/001-agent-developer_profile.md](specs/agent/001-agent-developer_profile.md) - Regole sviluppo AI

**Indice completo:** [SPEC_INDEX.md](specs/SPEC_INDEX.md)

### API Documentation
- OpenAPI: `/docs` (quando server attivo)
- [docs/openapi.yaml](docs/openapi.yaml) - Specifica OpenAPI

## Sviluppo

### Struttura Progetto
```
TFE-Trade-fair-evaluator/
├── src/fair_evaluator/     # Codice applicazione
├── specs/                  # Specifiche e documentazione
│   ├── main/              # Specifiche principali
│   ├── core/              # Funzionalità core (fairs, tags)
│   ├── ui/                # Interfacce utente
│   ├── system/            # Configurazioni sistema
│   ├── development/       # Processi sviluppo
│   ├── agent/             # Regole AI
│   └── SPEC_INDEX.md      # Indice specifiche
├── tests/                  # Test suite
├── data/                   # Dati (uploads, reports, db)
├── docs/                   # Documentazione aggiuntiva
└── requirements.txt
```

### Comandi Sviluppo
```bash
# Test
pytest tests/ -v

# Linting
ruff check .

# Formattazione
ruff format .

# Coverage
pytest tests/ --cov=src --cov-report=html
```

### Workflow Git
- `main`: produzione
- `develop`: integrazione
- `feature/*`: sviluppo funzionalità
- `hotfix/*`: correzioni urgenti

## Contributi

1. Leggi le [regole sviluppo](specs/agent/001-agent-developer_profile.md)
2. Crea branch feature dal `develop`
3. Scrivi test per nuove funzionalità
4. Aggiorna documentazione se necessario
5. Crea PR verso `develop`

## Licenza

[MIT License](LICENSE)

---

**Autore**: TFE Team
**Versione**: 1.0.0
**Ultimo aggiornamento**: 2026-04-20