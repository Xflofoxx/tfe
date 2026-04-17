# TFE - Trade Fair Evaluator

## Obiettivo
Valutare fiere commerciali per decidere se partecipare, analizzando dati da web con AI.

## Stack
- Backend: FastAPI + SQLite + SQLAlchemy
- Frontend: Bootstrap 5
- AI: Ollama (llama3.2) + ChatGPT/Copilot

## Modello Dati

### Fair
- id, name, year, duration_days
- url, description
- location, venue, address
- dates (JSON array)
- sector, organizer, frequency, edition
- expected_visitors, exhibitors_count, stand_cost
- status (in_valutazione, approvata, in_gestione, conclusa, rifiutata)
- tags (m:n con Tag)
- web_sources, extraction_regions

### Tag
- id, name, color, category
- fairs (m:n)

### Contact (m:n con Fair)
- id, name, email, phone, company, role

### FairAnalysis, OfferComponent, CommercialProposal
- come da schema originale

## Flusso Principale
1. Inserisci URL nella pagina "Nuova Fiera"
2. Genera Prompt AI (clicca "Genera")
3. Copia il prompt e incollalo in ChatGPT/Copilot
4. Incolla il JSON risultato e clicca "Estrai Dati"
5. I campi vengono compilati automaticamente
6. Salva

## Bulk Import
1. Passa più URL separati da newline
2. Il sistema genera un prompt multiplo
3. Riceve JSON array e crea tutte le fiere

## API

### Fiere
- `POST /api/fairs` - Crea singola
- `POST /api/fairs/bulk` - Crea multiple da URL
- `GET /api/fairs` - Lista
- `PUT /api/fairs/{id}` - Aggiorna

### Tag
- `GET /api/tags` - Lista
- `POST /api/tags` - Crea/ottieni (deduplicazione)
- `POST /api/tags/bulk` - Crea multipli

### Calendario
- `GET /calendar` - Vista annuale con colori per stato

## UI Pages
- `/` - Dashboard
- `/fairs` - Lista fiere
- `/fairs/new` - Nuova fiera + AI extraction
- `/fairs/{id}` - Dettaglio fiera
- `/calendar` - Calendario annuale
- `/settings` - Impostazioni Ollama