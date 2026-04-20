# Specifica: Servizi Core - AI e Web Scraping

## Panoramica

Servizi backend per integrazione AI (Ollama) e estrazione dati web.

## 1. Servizio Ollama (ollama.py)

### 1.1 OllamaClient Class

**Metodi**:
- `__init__(base_url)`: Inizializzazione client
- `chat(model, prompt)`: Invio prompt e ricezione risposta

**Configurazione**:
- URL base: configurabile via settings
- Timeout: 120 secondi default
- Modello: llama3.2 default

**Error Handling**:
- Ritorna None su errori di connessione
- Logging errori console

## 2. Servizio Ingest (ingest.py)

### 2.1 Web Scraping Multi-Method

**Metodi di Fetch**:
1. **Curl**: Per siti statici
   - User-Agent realistico
   - Timeout 30 secondi
   - Follow redirects

2. **Playwright**: Per siti JavaScript-heavy
   - Headless browser
   - Wait for network idle
   - Timeout 30 secondi

**Fallback Strategy**:
1. Prova curl
2. Se fallisce, prova Playwright
3. Se entrambi falliscono, ritorna stringa vuota

### 2.2 Content Processing

**Estrazione Dati**:
- HTML parsing con BeautifulSoup
- Estrazione: title, meta, H1/H2, links, main text
- Rimozione elementi non rilevanti (script, style, nav)

**Output**: Testo pulito per analisi AI

## 3. Integrazione con API

### 3.1 Endpoint Analisi Fiera

**Trigger**: `POST /api/fairs/{id}/analyze`

**Workflow**:
1. Recupero URL fiera da database
2. Fetch contenuto con ingest service
3. Invio a Ollama con prompt strutturato
4. Parsing risposta JSON
5. Aggiornamento campi fiera

### 3.2 Bulk Analysis

**Trigger**: Creazione bulk fiere

**Workflow**:
1. Fetch multiplo URLs
2. Generazione prompt batch
3. Analisi singola risposta array
4. Creazione multiple fiere

## 4. Configurazione

### 4.1 Settings Integration

**Campi utilizzati**:
- `ollama_url`: Base URL servizio AI
- `ollama_model`: Modello da utilizzare
- `ollama_timeout`: Timeout richieste
- `ollama_fallback_enabled`: Abilita/disabilita fallback

### 4.2 Error Recovery

**Strategie**:
- Retry automatico su timeout
- Fallback a modello alternativo
- Logging errori per debugging
- Graceful degradation (continua senza AI)

## 5. Performance

### 5.1 Ottimizzazioni

**Caching**:
- Risultati fetch per 1 ora
- Risultati AI per 24 ore

**Concurrency**:
- Background jobs per analisi pesanti
- Pool di connessioni HTTP

**Rate Limiting**:
- Max 5 richieste simultanee per dominio
- Backoff esponenziale su errori 429

## 6. Testing

### 6.1 Unit Tests

**Ollama Service**:
- Mock risposte API
- Test timeout handling
- Test error recovery

**Ingest Service**:
- Mock HTTP responses
- Test parsing HTML
- Test fallback methods

### 6.2 Integration Tests

**End-to-End**:
- Creazione fiera con analisi AI
- Verifica popolamento campi
- Test bulk operations
</content>
<parameter name="filePath">c:\Sviluppo\TFE-Trade fair evaluator\specs\development\002-development-services.md