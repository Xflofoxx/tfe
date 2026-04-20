# Agent AI - Regole di Comportamento e Sviluppo

## Profilo dello Sviluppatore

**Ruolo**: Senior Developer con 30 anni di esperienza
**Stack Tecnologico**: Python 3.13+, FastAPI, SQLAlchemy, SQLite, Ollama, HTML/Jinja2

## Principi Fondamentali

### 1. Qualità del Codice
- **PRIMO**: Leggibilità e manutenibilità del codice
- **SECONDO**: Efficienza e performance
- **TERZO**: Correttezza funzionale
- Zero tecnicismo inutile, ogni riga deve servire uno scopo

### 2. Processo di Sviluppo
1. **Analisi**: Comprendere il problema a fondo prima di scrivere codice
2. **Pianificazione**: Valutare se esiste specifica esistente o crearne una nuova
3. **Implementazione**: Seguire le convenzioni esistenti del codebase
4. **Verifica**: Testare sempre (unit test + integration test)
5. **Documentazione**: Aggiornare specs/documentazione se necessario

### 3. Gestione delle Richieste
- Ogni richiesta deve essere valutata:
  - Esiste già una specifica? → Arricchirla
  - Serve una nuova specifica? → Crearla
- Non procedere mai senza capire il contesto
- Chiedere chiarimenti se qualcosa non è chiaro

## Regole Operative

### Struttura del Progetto
```
TFE-Trade-fair-evaluator/
├── src/
│   └── fair_evaluator/
│       ├── main.py          # FastAPI app (entry point)
│       ├── models.py        # SQLAlchemy models
│       ├── db.py            # Database configuration
│       ├── cli.py           # Command line interface
│       ├── services/        # Business logic
│       └── templates/        # HTML templates
├── tests/                   # Test suite
├── specs/                  # Specifiche e documentazione
├── data/                    # Data (uploads, reports, db)
└── requirements.txt
```

### Convenzioni di Codice

#### Naming
- **Variabili**: snake_case (es. `fair_name`, `user_id`)
- **Funzioni**: snake_case con verbo (es. `get_fair()`, `create_fair()`)
- **Classi**: PascalCase (es. `Fair`, `Settings`)
- **Costanti**: UPPER_SNAKE_CASE (es. `MAX_UPLOAD_SIZE`)

#### Imports
- Ordine: standard → third-party → local
- Preferire import espliciti a `from x import *`
- Usare alias solo se necessario (es. `from sqlalchemy.orm import Session`)

#### Type Hints
- Obbligatori per parametri e ritorno delle funzioni pubbliche
- Preferire tipi concreti a `Any`
- Usare `Optional[X]` invece di `X | None`

#### Docstrings
- Obbligatorie per funzioni pubbliche
- Format: Google style o NumPy style
- Contenere: args, returns, raises (se rilevante)

#### Error Handling
- Mai usare `except:` nudo
- Catturare eccezioni specifiche
- Loggare sempre gli errori (mai swallow silently)
- Propagare solo se necessario

### Database Design

#### Modelli
- Un modello per tabella
- Usare `Column` con tipi appropriati
- Definire primary key esplicite
- Aggiungere indici su campi query frequenti

#### Query
- Usare Query SQLAlchemy (non raw SQL)
- Evitare N+1 queries (usare eager loading)
- Commit espliciti dopo modifiche
- Chiudere sempre le sessioni

### API Design

#### Endpoints REST
- `/api/resource` → GET (lista)
- `/api/resource` → POST (crea)
- `/api/resource/{id}` → GET (dettaglio)
- `/api/resource/{id}` → PUT/PATCH (aggiorna)
- `/api/resource/{id}` → DELETE (elimina)