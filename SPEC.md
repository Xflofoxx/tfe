# Valutatore Fiere - Specifiche

## Obiettivo
Valutare fiere commerciali per decidere se partecipare, analizzando dati da web e allegati con AI.

## Stack
- Backend: FastAPI + SQLite + SQLAlchemy
- Frontend: Bootstrap 5 + Material Design
- AI: Ollama (llama3.2) + algoritmo locale fallback

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
- scraped_data, historical_data, ROI_assessment, cost_estimate

### Contact (m:n con Fair)
- id, name, email, phone, company, role
- linkedin, notes
- fairs (relazione)

### CommercialProposal
- id, fair_id, name
- file_path, file_name
- total_amount, stand_size, stand_location
- services (JSON)
- status: ricevuta, in_trattativa, accettata, rifiutata
- notes, received_at, expires_at

### FairAnalysis
- id, fair_id, name
- parameters (JSON): parametri analisi
- result (JSON): risultato analisi
- summary: riassunto testuale
- created_at

### OfferComponent
- id, fair_id, name
- category: stand, marketing, visibilita, logistica, servizi
- description
- quantity, unit_price, total_price
- notes
- created_at

### Settings
- ollama_url, ollama_model
- strategy_prompt, strategy_pdf
- default_network_path

## API Endpoints

### Fiere
- POST /api/fairs - Crea fiera
- GET /api/fairs - Lista fiere (con year)
- GET /api/fairs/{id} - Dettaglio
- PUT /api/fairs/{id} - Aggiorna
- DELETE /api/fairs/{id} - Elimina

### Scraping e Analisi
- POST /api/scrape-url - Raccogli dati (web + allegati -> AI/Locale)
- POST /api/fairs/{id}/analyze - Analizza allegati (async con BackgroundTasks)
- POST /api/fairs/{id}/evaluate - Valuta con AI

### Analisi Multipla
- GET/POST/DELETE /api/fairs/{id}/analyses

### Componenti Offerta
- GET/POST/PUT/DELETE /api/fairs/{id}/components

### Contatti Referenti
- GET/POST/DELETE /api/fairs/{id}/contacts

### Proposte Commerciali
- GET/POST /api/fairs/{id}/proposals - Lista/Carica proposte
- GET /api/fairs/{id}/proposals/{proposal_id}
- DELETE /api/fairs/{id}/proposals/{proposal_id}

### Allegati (Legacy)
- POST /api/fairs/{id}/attachments - Aggiungi allegato
- DELETE /api/fairs/{id}/attachments/{att_idx}

### Notifiche
- GET /api/notifications/stream - SSE notifiche
- GET /api/notifications

### Cartella Rete
- POST /api/scan-network-folder
- POST /api/sync-from-network-folder

### Impostazioni
- GET/POST /api/settings
- GET /api/settings/ollama-status

### Report
- POST /api/fairs/{id}/report

## Flusso
1. Crea fiera da URL o da scansione cartella SharePoint
2. "Raccogli Dati" -> estrae da web + allegati -> Ollama o algoritmo locale
3. Ollama genera JSON con dati + riassunto 500+ parole
4. Carica proposte commerciali (PDF) -> estrazione automatica importi, dimensioni stand
5. Crea analisi multiple con parametri diversi
6. Definisci componenti offerta (stand, marketing, etc.)
7. Aggiungi contatti referenti
8. "Valuta" - confronta con strategia marketing
9. Genera report PDF/HTML

## Componenti Offerta
Ogni componente ha:
- name: nome (es. "Stand 20mq", "Inserzione catalogo")
- category: stand|marketing|visibilita|logistica|servizi
- description: descrizione dettagliata
- quantity: quantità
- unit_price: prezzo unitario
- total_price: prezzo totale (calcolato)
- notes: note

Totale offerta = somma total_price componenti

## Proposte Commerciali
Il sistema estrae automaticamente da PDF:
- total_amount: importo totale proposta
- stand_size: dimensione stand (mq)
- stand_location: posizione (angolo, centro, etc.)

## UI
- Material Design coerente
- Scheda fiera: header espanso, stats row, accordion collapsible
- Toast notifications in alto a destra
- Dashboard con notifiche push e attività recenti
- Lista fiere con colonna anno separata