# Valutatore Fiere - Specifiche

## Obiettivo
Valutare fiere commerciali per decidere se partecipare, analizzando dati da web e allegati con AI.

## Stack
- Backend: FastAPI + SQLite + SQLAlchemy
- Frontend: Bootstrap 5 + Material Design
- AI: Ollama (llama3.2)

## Modello Dati

### Fair
- id, name, year (chiave composita name+year)
- url, description
- location, venue, address
- dates (JSON array)
- sector, organizer, frequency
- expected_visitors, exhibitors_count, stand_cost
- folder_path, network_path
- instagram, facebook, tiktok
- status (in_valutazione, approvata, in_gestione, conclusa, rifiutata)
- recommendation, rationale
- attachments, contacts (JSON)
- previous_editions (JSON)

### Contact (m:n)
- id, name, email, phone, company, role
- linkedin, notes
- fairs (relazione)

### Settings
- ollama_url, ollama_model
- strategy_prompt, strategy_pdf
- default_network_path

## API Endpoints
- POST /api/fairs - Crea fiera
- GET /api/fairs - Lista fiere
- GET /api/fairs/{id} - Dettaglio
- PUT /api/fairs/{id} - Aggiorna
- DELETE /api/fairs/{id} - Elimina
- POST /api/scrape-url - Raccogli dati (web + allegati -> AI)
- POST /api/fairs/{id}/analyze - Analizza allegati (async)
- POST /api/fairs/{id}/evaluate - Valuta con AI
- GET /api/notifications/stream - SSE notifiche
- GET/POST /api/settings

## Flusso
1. Crea fiera da URL
2. "Raccogli Dati" -> estrae da web + allegati -> Ollama
3. Ollama genera JSON con dati + riassunto 500+ parole
4. "Analizza" - estrae da allegati (PDF) in background
5. "Valuta" - confronta con strategia marketing
6. Genera report PDF/HTML

## UI
- Material Design coerente
- Toast notifications
- Form allineati creazione/dettaglio
- Lista fiere con filtri e ordinamento