# Specifica: Gestione Fiere - CRUD Operations

## Panoramica

Modulo per la gestione completa del ciclo di vita delle fiere attraverso operazioni CRUD (Create, Read, Update, Delete).

## 1. Creazione Fiera

### 1.1 Endpoint: POST /api/fairs

**Input**:
```json
{
  "fair_url": "https://example.com/fair",
  "company_website": "https://company.com",
  "company_linkedin": "https://linkedin.com/company",
  "fair_email": "info@fair.com"
}
```

**Elaborazione**:
1. Validazione URL
2. Generazione UUID univoco
3. Derivazione nome fiera dall'URL
4. Creazione record con stato "in_valutazione"
5. Inizializzazione campi vuoti

**Output**:
```json
{
  "id": "uuid-string",
  "name": "Nome Fiera Derivato",
  "url": "https://example.com/fair",
  "status": "in_valutazione",
  "created_at": "2026-04-20T10:00:00Z"
}
```

### 1.2 Creazione Bulk

**Endpoint**: POST /api/fairs/bulk

**Input**:
```json
{
  "urls": [
    "https://fair1.com",
    "https://fair2.com"
  ]
}
```

**Output**: Array di oggetti fiera creati

## 2. Lettura Fiere

### 2.1 Lista Fiere

**Endpoint**: GET /api/fairs

**Parametri Query**:
- `skip`: numero elementi da saltare (default: 0)
- `limit`: numero elementi da restituire (default: 50, max: 100)
- `status`: filtro per stato
- `search`: ricerca testuale su nome/url

**Output**:
```json
{
  "fairs": [...],
  "total": 150,
  "skip": 0,
  "limit": 50
}
```

### 2.2 Dettaglio Fiera

**Endpoint**: GET /api/fairs/{fair_id}

**Output**: Oggetto fiera completo con tutti i campi popolati

## 3. Aggiornamento Fiera

### 3.1 Endpoint: PUT /api/fairs/{fair_id}

**Input**: Oggetto parziale con campi da aggiornare

**Validazioni**:
- Stato può solo avanzare nel workflow
- URL deve essere valida se fornita
- Campi numerici devono essere >= 0

**Workflow Stati**:
```
in_valutazione → approvata → in_gestione → conclusa
                 ↓
               rifiutata
```

**Transizioni Consentite**:
- in_valutazione → approvata | rifiutata
- approvata → in_gestione
- in_gestione → conclusa

## 4. Eliminazione Fiera

### 4.1 Soft Delete

**Endpoint**: DELETE /api/fairs/{fair_id}

**Elaborazione**:
- Imposta flag `archived = "yes"`
- Mantiene record per audit trail
- Non appare più nelle liste normali

### 4.2 Hard Delete (Admin Only)

**Endpoint**: DELETE /api/fairs/{fair_id}?hard=true

**Elaborazione**:
- Rimozione fisica dal database
- Cancellazione file allegati
- Logging operazione

## 5. Modello Dati Fiera

| Campo | Tipo | Obbligatorio | Descrizione |
|-------|------|--------------|-------------|
| id | String (UUID) | ✅ | Chiave primaria |
| name | String | ✅ | Nome fiera |
| url | String | ✅ | URL sito ufficiale |
| description | Text | ❌ | Descrizione fiera |
| status | String | ✅ | Stato workflow |
| created_at | DateTime | ✅ | Data creazione |
| updated_at | DateTime | ✅ | Data ultimo aggiornamento |
| archived | String | ✅ | Flag archiviazione ("yes"/"no") |

## 6. Validazioni

### 6.1 URL Validation
- Deve essere URL valido (http/https)
- Deve essere raggiungibile (opzionale, con timeout)
- Deve essere univoco nel sistema

### 6.2 Nome Derivazione
- Da URL: rimuovi protocolli, estensioni, caratteri speciali
- Fallback: "Fiera [ID]" se derivazione fallisce

### 6.3 Stato Workflow
- Validazione transizioni consentite
- Logging cambiamenti stato
- Notifiche utente su cambiamenti importanti

## 7. Error Handling

### 7.1 Codici Errore
- 400: Dati input invalidi
- 404: Fiera non trovata
- 409: Conflitto (URL duplicata)
- 422: Transizione stato non consentita

### 7.2 Logging
- Tutte le operazioni CRUD loggate
- Errori con stack trace completo
- Audit trail per modifiche critiche

## 8. Performance

### 8.1 Ottimizzazioni
- Indici su campi query frequenti (status, created_at)
- Paginazione obbligatoria per liste
- Cache per fiere popolari (future)

### 8.2 Limiti
- Max 1000 fiere per utente/organizzazione
- Rate limiting: 100 richieste/minuto per CRUD

---

**Autore**: Team Development
**Versione**: 1.0.0
**Stato**: Approved
**Ultimo Aggiornamento**: 2026-04-20