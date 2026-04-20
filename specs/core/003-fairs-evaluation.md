# Specifica: Valutazione Fiere - AI Analysis & Evaluation

## Panoramica

Sistema di valutazione automatica delle fiere utilizzando LLM per analizzare fattibilità partecipazione e ROI.

## 1. Workflow Valutazione

### 1.1 Trigger Valutazione

**Condizioni**:
- Fiera ha stato "in_valutazione"
- Sono presenti allegati (PDF strategia, preventivi)
- Impostazioni Ollama configurate

**Endpoint**: POST /api/fairs/{fair_id}/evaluate

### 1.2 Preparazione Context

**Dati Fiera**:
- Nome, URL, descrizione
- Location, venue, date
- Expected visitors, exhibitors
- Stand cost, target segments
- Dati scraped da web

**Dati Aziendali**:
- Strategia aziendale (da settings)
- Budget disponibile
- Obiettivi marketing

**Allegati**:
- PDF strategia aziendale
- Preventivi fornitori
- Documenti tecnici

## 2. Analisi con LLM

### 2.1 Prompt Structure

```
COMPANY STRATEGY:
{strategy_prompt}

FAIR DATA:
- Name: {fair.name}
- URL: {fair.url}
- Description: {fair.description}
- Location: {fair.location}
- Dates: {fair.dates}
- Expected Visitors: {fair.expected_visitors}
- Exhibitors: {fair.exhibitors_count}
- Stand Cost: {fair.stand_cost}
- Target Segments: {fair.target_segments}

ATTACHMENTS CONTENT:
{extracted_text_from_attachments}

Based on company strategy and fair data, evaluate:
1. RECOMMENDATION: RECOMMENDED / NOT_RECOMMENDED / EVALUATE_FURTHER
2. RATIONALE: 2-3 sentence explanation
3. ROI_ASSESSMENT: low / medium / high
4. COST_ESTIMATE: suggested budget range
5. RISKS: potential risks identified
6. OPPORTUNITIES: key opportunities
```

### 2.2 Output Parsing

**Formato Atteso**:
```json
{
  "recommendation": "RECOMMENDED",
  "rationale": "La fiera presenta alto potenziale ROI...",
  "roi_assessment": "high",
  "cost_estimate": {
    "min_budget": 15000,
    "max_budget": 25000,
    "currency": "EUR"
  },
  "risks": ["Alta competizione", "Stagione non ottimale"],
  "opportunities": ["Nuovo mercato", "Networking strategico"]
}
```

### 2.3 Fallback Analysis

**Se LLM non disponibile**:
- Algoritmo euristico basato su:
  - Dimensioni fiera (visitatori/espositori)
  - Costo stand vs budget
  - Allineamento settore
  - Stagionalità

## 3. Salvataggio Risultati

### 3.1 Campi Database

```sql
ALTER TABLE fairs ADD COLUMN
  recommendation TEXT,
  rationale TEXT,
  roi_assessment JSON,
  cost_estimate JSON,
  evaluation_date TIMESTAMP
```

### 3.2 Aggiornamento Stato

**Dopo valutazione**:
- Se RECOMMENDED → stato rimane "in_valutazione" (decisione manuale)
- Se NOT_RECOMMENDED → può passare a "rifiutata"
- Se EVALUATE_FURTHER → richiede revisione manuale

## 4. Interfaccia Utente

### 4.1 Pagina Valutazione

**Elementi**:
- Riepilogo dati fiera
- Pulsante "Avvia Valutazione"
- Spinner durante elaborazione
- Risultati formattati:
  - Badge raccomandazione (verde/rosso/giallo)
  - Testo rationale
  - Metriche ROI
  - Range costi
  - Liste rischi/opportunità

### 4.2 Notifiche

**WebSocket Events**:
- evaluation_started
- evaluation_progress (con %)
- evaluation_completed
- evaluation_error

## 5. Gestione Errori

### 5.1 Errori LLM
- Timeout connessione
- Risposta malformata
- Modello non disponibile

**Fallback**: Algoritmo locale con flag "AI not available"

### 5.2 Errori Allegati
- File corrotti
- Testo non estratto
- PDF protetti

**Gestione**: Skip allegato, log warning, continua valutazione

## 6. Ottimizzazioni Performance

### 6.1 Caching
- Risultati valutazione cache per 24h
- Evita rivalutazioni duplicate

### 6.2 Async Processing
- Valutazione in background
- Progress tracking
- Cancellazione possibile

### 6.3 Rate Limiting
- Max 5 valutazioni simultanee per utente
- Timeout 5 minuti per valutazione

## 7. Metriche e Analytics

### 7.1 Tracking
- Tempo medio valutazione
- Accuratezza raccomandazioni (feedback utente)
- Tasso successo (fiere approvate vs rifiutate)

### 7.2 Report
- Dashboard valutazioni
- Trend raccomandazioni
- ROI realizzato vs previsto

## 8. Sicurezza

### 8.1 Validazione Input
- Sanitizzazione prompt
- Limite dimensione allegati
- Validazione JSON output

### 8.2 Audit Trail
- Logging tutte le valutazioni
- Tracciamento decisioni
- Backup risultati

---

**Autore**: Team Development
**Versione**: 1.0.0
**Stato**: Approved
**Ultimo Aggiornamento**: 2026-04-20