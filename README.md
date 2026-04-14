# Valutatore di Fiere (Trade Fair Evaluator)

## Descrizione

Applicazione web per valutare se partecipare o meno a una fiera commerciale. L'app analizza automaticamente le fiere, estrae informazioni da siti web e documenti (PDF, brochure), e utilizza un modello LLM locale (Ollama) per generare report decisionali basati sulla strategia aziendale.

## Funzionalità

### Creazione e Gestione Fiere
- Creazione di nuove fiere con URL del sito web
- Recupero automatico delle informazioni dal sito della fiera (web scraping)
- Modifica e aggiornamento dei dati della fiera
- Eliminazione delle fiere
- Visualizzazione lista fiere con filtri e paginazione

### Analisi Automatica
- Estrazione dati dal sito web della fiera:
  - Nome, descrizione, località
  - Date, venue, organizzatore
  - Numero visitatori previsti, numero espositori
  - Settore target, categorie prodotto
- Salvataggio dei dati estratti nel record della fiera

### Caricamento Allegati
- Upload di brochure PDF e documenti
- Estrazione automatica del testo dai PDF
- Supporto per formati: PDF, TXT, DOC, DOCX, immagini (con OCR)

### Valutazione con LLM
- Caricamento della strategia aziendale (testo)
- Analisi della fiera basata sulla strategia
- Generazione report con:
  - Raccomandazione (Consigliata / Non Consigliata / Valutare)
  - Motivazione dettagliata
  - Stima budget consigliato
  - Valutazione ROI

### Storico e Analisi
- Cronologia delle valutazioni
- Dati storici delle fiere (anni precedenti)
- Statistiche sul database

### Report
- Generazione report HTML
- Export dati in Excel

## Stack Tecnologico

- **Backend**: Python 3.13, FastAPI
- **Database**: SQLite + SQLAlchemy ORM
- **LLM**: Ollama (locale)
- **Web Scraping**: Requests + BeautifulSoup
- **PDF**: PyMuPDF, pdfplumber
- **Report**: Jinja2, WeasyPrint (opzionale)
- **Frontend**: HTML/Jinja2 semplice

## Requisiti

- Python 3.11+
- Ollama installato e avviato locally (http://localhost:11434)
- Connessione Internet per scraping (opzionale in fase di sviluppo)

## Installazione

```bash
# Clona il repository
git clone <repo-url>
cd TFE-Trade-fair-evaluator

# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente virtuale
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Inizializza il database (automatico all'avvio)
python -m src.fair_evaluator.db_init
```

## Avvio

```bash
# Avvia il server
python run_server.py

# Oppure con uvicorn
uvicorn src.fair_evaluator.main:app --reload --port 8000
```

Accedi a: http://localhost:8000

## Utilizzo

### 1. Configurazione Strategia
- Vai su Impostazioni
- Carica il file di strategia aziendale (txt)
- Configura URL e modello Ollama

### 2. Creare una Fiera
- Clicca "Nuova Fiera"
- Inserisci URL del sito della fiera
- Opzionalmente: sito web azienda, LinkedIn, email

### 3. Analisi Automatica
- Clicca "Analizza" sulla fiera
- Il sistema estrae i dati dal sito web

### 4. Carica Allegati
- Carica brochure e preventivi nella scheda fiera

### 5. Valutazione
- Clicca "Valuta" per generare il report
- Ollama analizza fiera + strategia + allegati
- Ottieni raccomandazione e budget consigliato

## API Endpoints

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/fairs` | GET | Lista fiere |
| `/api/fairs` | POST | Crea fiera |
| `/api/fairs/{id}` | GET | Dettaglio fiera |
| `/api/fairs/{id}` | PUT | Aggiorna fiera |
| `/api/fairs/{id}` | DELETE | Elimina fiera |
| `/api/fairs/{id}/analyze` | POST | Analizza fiera (scraping) |
| `/api/fairs/{id}/evaluate` | POST | Valuta fiera con LLM |
| `/api/fairs/{id}/report` | POST | Genera report |
| `/api/settings` | GET/POST | Gestione impostazioni |
| `/api/import-excel-upload` | POST | Importa da Excel |
| `/api/export-excel` | GET | Esporta Excel |

## Struttura Progetto

```
TFE-Trade-fair-evaluator/
├── src/
│   └── fair_evaluator/
│       ├── main.py          # FastAPI app
│       ├── models.py        # SQLAlchemy models
│       ├── db.py            # Database setup
│       ├── services/
│       │   ├── ollama.py    # LLM client
│       │   └── ingest.py   # Data ingestion
│       └── templates/       # HTML templates
├── data/
│   ├── uploads/             # File allegati
│   ├── reports/            # Report generati
│   └── strategy/           # Strategia caricata
├── tests/                   # Test pytest
└── requirements.txt
```

## Testing

```bash
# Esegui test con coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

## Note

- L'applicazione funziona interamente in locale
- Per scraping, rispettare i termini di servizio dei siti
- Ollama deve essere avviato separatamente
- WeasyPrint opzionale per PDF (richiede GTK)

## License

MIT