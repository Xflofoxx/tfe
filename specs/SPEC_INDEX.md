# Indice Specifiche - TFE Trade Fair Evaluator

## Panoramica

Questo documento fornisce un indice completo delle specifiche tecniche e funzionali del progetto TFE (Trade Fair Evaluator).

## Struttura Specifiche

Le specifiche sono organizzate in cartelle per area funzionale con formato `xxx-module-desc.md`:
- **main/**: Specifiche principali del progetto
- **core/**: Funzionalità core (fairs, tags)
- **ui/**: Interfacce utente e dashboard
- **system/**: Configurazioni e impostazioni
- **development/**: Processi e specifiche tecniche
- **agent/**: Regole e profili AI

## Stato Implementazione

### ✅ Implementato Completamente
- [core/007-tags-expansion.md](core/007-tags-expansion.md) - Sistema tag con categorie gerarchiche, bulk operations, analytics
- [ui/005-homepage-dashboard.md](ui/005-homepage-dashboard.md) - Dashboard principale con metriche KPIs e grafici
- [system/006-settings-management.md](system/006-settings-management.md) - Sistema impostazioni completo con tutti i campi richiesti

### 🔄 In Corso
- [core/008-fairs-detail-page.md](core/008-fairs-detail-page.md) - Pagina dettaglio fiera (parzialmente implementata)
- [core/004-fairs-creation.md](core/004-fairs-creation.md) - Workflow creazione fiera (base implementato)

### 📋 Pianificato
- [core/002-fairs-management.md](core/002-fairs-management.md) - Operazioni CRUD complete per fiere
- [core/003-fairs-evaluation.md](core/003-fairs-evaluation.md) - Sistema valutazione AI avanzato
- [development/001-development-functional_spec.md](development/001-development-functional_spec.md) - Specifica funzionale completa
- [development/002-development-services.md](development/002-development-services.md) - Servizi e architettura

### Main (Principale)
- [main/001-main-project_overview.md](main/001-main-project_overview.md)
  - Panoramica progetto, stack tecnologico, modello dati, flussi principali

### Core - Fairs (Gestione Fiere)
- [core/002-fairs-management.md](core/002-fairs-management.md)
  - CRUD operations per fiere, workflow creazione e gestione
- [core/003-fairs-evaluation.md](core/003-fairs-evaluation.md)
  - Workflow valutazione AI, scoring system, report generation
- [core/004-fairs-creation.md](core/004-fairs-creation.md)
  - UI/UX flow creazione nuova fiera, wizard steps, validation
- [core/008-fairs-detail-page.md](core/008-fairs-detail-page.md)
  - Pagina dettaglio fiera con tabs, analytics, bulk operations

### Core - Tags (Sistema Tag)
- [core/001-tags-tag_system.md](core/001-tags-tag_system.md)
  - Sistema tag categorizzati per settore, profilo visitatori, categorie prodotto
- [core/007-tags-expansion.md](core/007-tags-expansion.md)
  - Espansione sistema tag con categorie gerarchiche, bulk operations, analytics

### UI (Interfacce Utente)
- [ui/005-homepage-dashboard.md](ui/005-homepage-dashboard.md)
  - Dashboard principale, widgets, navigation, user experience

### System (Impostazioni)
- [system/006-settings-management.md](system/006-settings-management.md)
  - Configurazione sistema, AI, strategia aziendale, preferenze utente

### Development (Sviluppo)
- [development/001-development-functional_spec.md](development/001-development-functional_spec.md)
  - Specifica funzionale completa: API, modelli dati, workflow, requisiti
- [development/002-development-services.md](development/002-development-services.md)
  - Servizi core: AI (Ollama), web scraping, ingest
- [development/003-development-testing.md](development/003-development-testing.md)
  - Suite test completa: unit, integration, quality gates
- [development/001-process-development_process.md](development/001-process-development_process.md)
  - Workflow Git, CI/CD, release management, quality gates

### Agent (AI Development)
- [agent/001-agent-developer_profile.md](agent/001-agent-developer_profile.md)
  - Regole di comportamento e sviluppo per l'agente AI, convenzioni codice

### Modulo Process (Processi)
- [001-process-development_process.md](001-process-development_process.md)
  - Workflow Git, CI/CD, release management, quality gates

## Stato Specifiche

| Specifica | Stato | Ultimo Aggiornamento | Responsabile |
|-----------|-------|---------------------|-------------|
| 001-main-project_overview | ✅ Approved | 2026-04-20 | Team | ✅ Aggiornato modello dati e API per riflettere implementazione completa |
| 001-tags-tag_system | ✅ Approved | 2026-04-20 | Team | ✅ Completato sistema tag avanzato con categorie gerarchiche, analytics, AI |
| 002-fairs-management | ✅ Approved | 2026-04-20 | Team | |
| 003-fairs-evaluation | ✅ Approved | 2026-04-20 | Team | |
| 004-fairs-creation | ✅ Approved | 2026-04-20 | Team | |
| 005-homepage-dashboard | ✅ Approved | 2026-04-20 | Team | |
| 006-settings-management | ✅ Approved | 2026-04-20 | Team | ✅ Completata specifica impostazioni con tutti i campi implementati |
| 007-tags-expansion | ✅ Approved | 2026-04-20 | Team | |
| 008-fairs-detail-page | ✅ Approved | 2026-04-20 | Team | |
| 001-agent-developer_profile | ✅ Approved | 2026-04-20 | Team | |
| 001-development-functional_spec | ✅ Approved | 2026-04-20 | Team |
| 002-development-services | ✅ Approved | 2026-04-20 | Team |
| 003-development-testing | ✅ Approved | 2026-04-20 | Team |
| 001-process-development_process | ✅ Approved | 2026-04-20 | Team |

## Come Leggere le Specifiche

1. **Inizia da main/** per comprensione generale del sistema
2. **Esplora core/** per funzionalità principali (fairs e tags)
3. **Consulta ui/** per interfacce utente
4. **Configura system/** per impostazioni
5. **Sviluppa seguendo development/** per workflow tecnici
6. **Applica regole agent/** per convenzioni AI
4. **Riferisci process** per workflow e deployment
5. **Usa tag_system** per gestione categorizzazione

## Aggiornamenti

Le specifiche vengono aggiornate secondo il processo definito in `001-process-development_process.md`.

Per proposte di modifica:
1. Crea issue GitHub con tag `specification`
2. Discuti modifiche nel team
3. Aggiorna specifica e commit
4. Aggiorna questo indice

## Contatti

- **Team Development**: [team@company.com]
- **Product Owner**: [po@company.com]
- **Repository**: [GitHub Link]

---

**Ultimo aggiornamento**: 2026-04-20
**Versione**: 1.0.0