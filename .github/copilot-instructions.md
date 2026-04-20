# TFE - Copilot Instructions

## Workflow Principale

Questo workspace segue la metodologia **spec-code-alignment**: le specifiche sono la fonte di verità e il codice viene implementato in allineamento rigoroso con esse.

### 1. Prima di Implementare
1. Verifica il file `specs/SPEC_INDEX.md`
2. Leggi la specifica rilevante (cartella main/, core/, ui/, system/)
3. Assicurati di comprendere i requisiti completamente

### 2. Durante l'Implementazione
1. Implementa il codice seguendo la specifica esattamente
2. Mantieni la struttura del progetto (src/fair_evaluator/, tests/)
3. Usa le convenzioni del codice (type hints, docstrings)
4. Linkamo le specifiche nei commenti del codice

### 3. Quando Finisci
1. Verifica che il codice soddisfi tutti i requisiti spec
2. Aggiorna la specifica se scopri gap o ottimizzazioni
3. Segnala quali specifiche implementate nel messaggio di commit

## Custom Agents Available

### spec-code-developer
**Agente Senior con 30+ anni di esperienza nello stack TFE**

**Quando usarlo**:
- Implementare una nuova feature da specifica
- Allineare il codice quando cambia una specifica
- Refactoring di codice per conformità spec
- Auto-trigger quando rileva cambiamenti spec

**Tech Stack Expertise**:
- Backend: FastAPI, SQLAlchemy, SQLite, Python
- Frontend: Bootstrap 5, JavaScript
- AI: Ollama, ChatGPT integration
- Tools: ruff, pytest

**Come invocare**:
- Digita `/` in una chat e seleziona "spec-code-developer"
- O menziona "spec-code-developer" nel context

File: `.github/agents/spec-code-developer.agent.md`

## Mode Attuale

Questo workspace è configurato in modalità **spec-code-alignment**:
- Usa `spec-code-developer` come agente principale
- Verifica sempre `specs/` prima di modificare il codice
- Crea/aggiorna specifiche se il codice non è specificato
- Allinea issue GitHub alle specifiche

## Repository Structure

```
.github/
├── agents/
│   └── spec-code-developer.agent.md   # Senior dev agent
└── AGENTS.md                           # Registry degli agents

specs/
├── SPEC_INDEX.md                       # Indice e mappa
├── main/                               # Panoramica progetto
├── core/                               # Funzionalità core
├── ui/                                 # Interfacce
├── system/                             # Configurazioni
├── development/                        # Processi tecnici
└── agent/                              # Regole AI

src/fair_evaluator/                    # Implementazione
tests/                                  # Test suite
docs/                                   # Documentazione
```

## Quick Links

- **Progetto**: [main/001-main-project_overview.md](../specs/main/001-main-project_overview.md)
- **Dev Process**: [development/001-process-development_process.md](../specs/development/001-process-development_process.md)
- **API Spec**: [development/001-development-functional_spec.md](../specs/development/001-development-functional_spec.md)
- **Agent Rules**: [agent/001-agent-developer_profile.md](../specs/agent/001-agent-developer_profile.md)

## Stack Tecnologico

- **Language**: Python 3.9+
- **Backend**: FastAPI, SQLAlchemy ORM
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **AI**: Ollama (llama3.2), ChatGPT/Copilot
- **QA**: pytest, ruff formatter/linter
- **Version Control**: Git with conventional commits

## Development Commands

```bash
# Installa dipendenze
pip install -r requirements.txt

# Avvia il server
python run_server.py
# oppure
./start_server.bat  # Windows
./root_starter.sh   # Linux/Mac

# Esegui test
pytest tests/

# Formatta e linta
ruff check .
ruff format .
```

---

**Created**: 2026-04-20  
**Mode**: spec-code-alignment  
**Primary Agent**: spec-code-developer
