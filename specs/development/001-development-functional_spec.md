# Specifica Funzionale - Trade Fair Evaluator

## Panoramica del Prodotto

**Nome**: Trade Fair Evaluator (Valutatore di Fiere)
**Versione**: 1.0.0
**Descrizione**: Applicazione web per valutare se partecipare o meno a una fiera commerciale, con analisi automatica tramite web scraping e LLM locale (Ollama).
**Target Utenti**: Responsabili marketing, event manager, PM di PMI che valutano partecipazione a fiere B2B.

---

## 1. Funzionalità Core

### 1.1 Gestione Fiere (CRUD)

#### Creazione Fiera
- **Input**: URL sito fiera (obbligatorio), sito azienda, LinkedIn, email (opzionali)
- **Elaborazione**:
  - Generazione UUID univoco
  - Parsing URL per derivare nome fiera
  - Creazione record con stato iniziale "in_valutazione"
- **Output**: ID fiera, nome, URL, stato

#### Lettura Fiera
- **Input**: fair_id
- **Output**: tutti i campi della fiera in formato JSON

#### Aggiornamento Fiera
- **Input**: fair_id, campi da aggiornare
- **Elaborazione**: aggiornamento campi specificati (partial update)
- **Output**: stato "updated"

#### Eliminazione Fiera
- **Input**: fair_id
- **Elaborazione**: soft delete o hard delete
- **Output**: stato "deleted"

#### Lista Fiere
- **Input**: skip, limit (paginazione)
- **Output**: array di fiere ordinate per ID discendente

### 1.2 Analisi Automatica (Web Scraping)

#### Recupero Dati dal Sito
- **Trigger**: endpoint `/api/fairs/{id}/analyze` o creazione fiera
- **Elaborazione**:
  1. Richiesta HTTP al sito fiera
  2. Parsing HTML con BeautifulSoup
  3. Estrazione: title, meta description, OG tags, H1/H2, keywords, links, main text
  4. Invio contenuto a Ollama per analisi strutturata
  5. Parsing JSON risposta e popolamento campi Fair
- **Dati Estratti**:
  - Nome ufficiale fiera
  - Descrizione (2-3 frasi)
  - Location (città)
  - Venue (nome centro fieristico)
  - Indirizzo completo
  - Date (formato libero)
  - Frequency (annuale/biennale/etc)
  - Edition (numero edizione)
  - Organizer (nome organizzatore)
  - Sector (settore merceologico)
  - Target segments (array)
  - Expected visitors (numero)
  - Exhibitors count (numero)
  - Exhibitor countries (array)
  - Visitor profile (testo)
  - Product categories (array)
  - Key features (array)

### 1.3 Caricamento Allegati

#### Upload File
- **Input**: file (PDF, TXT, DOC, DOCX, immagini)
- **Elaborazione**:
  - Validazione tipo file
  - Generazione UUID per filename
  - Salvataggio in `./data/uploads/`
  - Aggiunta metadata alla fiera
- **Endpoint**: `/api/upload-pdf`, `/api/upload-strategy`

#### Estrazione Testo da Allegati
- **PDF**: PyMuPDF o pdfplumber
- **Immagini**: pytesseract (OCR)
- **DOCX**: python-docx
- **TXT**: lettura diretta

### 1.4 Valutazione con LLM

#### Workflow
1. Verifica presenza allegati (obbligatori)
2. Recupero strategia aziendale da settings
3. Preparazione context: dati fiera + strategia + contenuto allegati
4. Invio prompt strutturato a Ollama
5. Parsing risposta JSON

#### Prompt Structure
```
COMPANY STRATEGY:
{strategy_prompt}

FAIR DATA:
- Nome: {fair.name}
- URL: {fair.url}
- Descrizione: {fair.description}
- Location: {fair.location}
- Dates: {fair.dates}
- Expected Visitors: {fair.expected_visitors}
- Exhibitors: {fair.exhibitors_count}
- Stand Cost: {fair.stand_cost}
- Attachments: {attachments_count} files

Based on your analysis:
1. Recommendation (RECOMMENDED / NOT RECOMMENDED / EVALUATE)
2. Brief rationale (2-3 sentences)
3. Estimated ROI assessment (low/medium/high)
4. Suggested budget range (if recommended)
```

#### Output Valutazione
- Recommendation: stringa
- Rationale: testo descrittivo
- ROI_assessment: oggetto con assessment e data
- Cost_estimate: oggetto (opzionale)

### 1.5 Generazione Report

#### Report HTML
- Template Jinja2: `report.html`
- Include: dati fiera, valutazione, strategia
- Salvataggio in `./data/reports/`

#### Report PDF (opzionale)
- Conversione HTML → PDF con WeasyPrint
-richiede GTK installato)

### 1.6 Import/Export Excel

#### Import
- Parse Excel con openpyxl
- Mappatura colonne: nome, link evento, città, location, stato, inizio, fine, costo stand, contatto info, num leads, affluenza
- Creazione record Fair per ogni riga

#### Export
- Generazione Excel con openpyxl
- Include tutte le colonne importabili
- Download con nome `Fiere_YYYYMMDD_HHMMSS.xlsx`

---

## 2. Interfacce API

### 2.1 Endpoints Pubblici

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/fairs` | GET | Lista fiere (paginated) |
| `/api/fairs` | POST | Crea fiera |
| `/api/fairs/{id}` | GET | Dettaglio fiera |
| `/api/fairs/{id}` | PUT | Aggiorna fiera |
| `/api/fairs/{id}` | DELETE | Elimina fiera |
| `/api/fairs/{id}/analyze` | POST | Avvia analisi web |
| `/api/fairs/{id}/evaluate` | POST | Valuta con LLM |
| `/api/fairs/{id}/report` | POST | Genera report |
| `/api/fairs/{id}/report/download` | GET | Scarica report |
| `/api/settings` | GET | Leggi impostazioni |
| `/api/settings` | POST | Aggiorna impostazioni |
| `/api/settings/ollama-status` | GET | Stato Ollama |
| `/api/upload-pdf` | POST | Upload allegato |
| `/api/upload-strategy` | POST | Upload strategia PDF |
| `/api/extract-pdf` | POST | Estrai da PDF |
| `/api/scrape-url` | POST | Scraping veloce URL |
| `/api/import-excel-upload` | POST | Importa da Excel |
| `/api/export-excel` | GET | Esporta Excel |
| `/api/db/clear` | POST | Svuota database |
| `/api/db/stats` | GET | Statistiche database |
| `/api/strategy/load` | POST | Carica strategia TXT |
| `/api/strategy/analyze` | POST | Analizza strategia PDF |

### 2.2 Pagine UI

| Endpoint | Descrizione |
|----------|-------------|
| `/` | Home dashboard |
| `/fairs` | Lista fiere |
| `/fairs/new` | Nuova fiera |
| `/fairs/{id}` | Dettaglio fiera |
| `/settings` | Impostazioni |
| `/maintenance` | Manutenzione e stats |

---

## 3. Modello Dati

### 3.1 Entità Fair

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | String (PK) | UUID |
| name | String | Nome fiera |
| url | String | URL sito fiera |
| description | Text | Descrizione |
| folder_path | String | Path cartella locale |
| dates | JSON | Array date |
| location | String | Città |
| target_segments | JSON | Array segmenti target |
| expected_visitors | Integer | Visitatori attesi |
| exhibitors_count | Integer | Numero espositori |
| sources | JSON | Fonti dati |
| company_website | String | Sito azienda |
| company_linkedin | String | LinkedIn |
| fair_email | String | Email contatto fiera |
| gallery | JSON | Array URL immagini |
| attachments | JSON | Array allegati |
| contacts | JSON | Contatti (nome, email, tel) |
| stand_cost | Integer | Costo stand |
| status | String | Stato workflow |
| scraped_data | JSON | Dati estratti da web |
| historical_data | JSON | Dati storici |
| ROI_assessment | JSON | Valutazione ROI |
| cost_estimate | JSON | Stima costi |
| recommendation | String | Raccomandazione |
| rationale | Text | Motivazione |
| report_pdf_path | String | Path report PDF |
| report_html_path | String | Path report HTML |
| frequency | String | Frequenza fiera |
| edition | String | Numero edizione |
| organizer | String | Nome organizzatore |
| sector | String | Settore merceologico |
| exhibitor_countries | JSON | Paesi espositori |
| visitor_profile | Text | Profilo visitatori |
| product_categories | JSON | Categorie prodotto |
| key_features | JSON | Caratteristiche chiave |
| venue | String | Venue |
| address | String | Indirizzo |

### 3.2 Entità Settings

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer (PK) | ID |
| ollama_url | String | URL Ollama |
| ollama_model | String | Nome modello |
| strategy_prompt | Text | Strategia aziendale |
| strategy_pdf | String | Path PDF strategia |

### 3.3 Workflow Fiera

```
in_valutazione → approvata → in_gestione → conclusa
                 ↓
               rifiutata
```

---

## 4. Requisiti Non Funzionali

### 4.1 Performance
- Tempo risposta API < 200ms (senza scraping)
- Web scraping timeout: 15s
- LLM timeout: 120s

### 4.2 Scalabilità
- Supporto fino a 1000 fiere
- Upload file max 50MB

### 4.3 Sicurezza
- Validazione input
- Sanitization HTML output
- No credential hardcoded

### 4.4 Affidabilità
- Error handling globale
- Logging operazioni
- Database backup (manuale)

---

## 5. Dipendenze Esterne

| Libreria | Versione | Uso |
|----------|----------|-----|
| fastapi | latest | API framework |
| sqlalchemy | latest | ORM |
| requests | latest | HTTP client |
| beautifulsoup4 | latest | HTML parsing |
| jinja2 | latest | Templating |
| openpyxl | latest | Excel I/O |
| pymupdf | latest | PDF extraction |

### Opzionali
- weasyprint: PDF generation
- pdfplumber: alternative PDF
- pytesseract: OCR
- python-docx: DOCX parsing
- pytesseract: OCR

---

## 6. Note di Implementazione

### 6.1 Web Scraping
- Rispetto robots.txt dove possibile
- User-Agent realistico
- Rate limiting implicito (1 richiesta/fiera)
- Cache risultati in scraped_data

### 6.2 Ollama Integration
- Endpoint: `/api/generate`
- Modello default: `llama3.2`
- Fallback graceful se offline
- Streaming disabilitato per semplicità

### 6.3 Testing
- Database in-memory per test
- Mock Ollama per test unitari
- Coverage target: 80%+

---

**Autore**: Specifica funzionale v1.0
**Ultimo aggiornamento**: 2026-04-14
**Stato**: Approved