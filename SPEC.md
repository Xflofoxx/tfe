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
- GET /api/fairs/{id}/analyses - Lista analisi fiera
- POST /api/fairs/{id}/analyses - Crea analisi
- GET /api/fairs/{id}/analyses/{analysis_id}
- DELETE /api/fairs/{id}/analyses/{analysis_id} - Elimina analisi

### Componenti Offerta
- GET /api/fairs/{id}/components - Lista componenti
- POST /api/fairs/{id}/components - Aggiungi componente
- PUT /api/fairs/{id}/components/{comp_id}
- DELETE /api/fairs/{id}/components/{comp_id}

### Contatti Referenti
- GET /api/fairs/{id}/contacts - Lista contatti riferimento
- POST /api/fairs/{id}/contacts - Aggiungi contatto riferimento
- DELETE /api/fairs/{id}/contacts/{contact_id}

### Allegati
- POST /api/fairs/{id}/attachments - Aggiungi allegato
- DELETE /api/fairs/{id}/attachments/{att_idx} - Rimuovi allegato

### Notifiche
- GET /api/notifications/stream - SSE notifiche
- GET /api/notifications - Ultime 20 notifiche

### Cartella Rete
- POST /api/scan-network-folder - Scansiona cartella SharePoint
- POST /api/sync-from-network-folder - Sincronizza da cartella configurata

### Impostazioni
- GET/POST /api/settings
- GET /api/settings/ollama-status

### Report
- POST /api/fairs/{id}/report - Genera report PDF/HTML

## Flusso
1. Crea fiera da URL o da scansione cartella SharePoint
2. "Raccogli Dati" -> estrae da web + allegati -> Ollama o algoritmo locale
3. Ollama genera JSON con dati + riassunto 500+ parole
4. Crea analisi multiple con parametri diversi
5. Definisci componenti offerta (stand, marketing, etc.)
6. Aggiungi contatti referenti
7. "Valuta" - confronta con strategia marketing
8. Genera report PDF/HTML

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

## UI
- Material Design coerente
- Toast notifications in alto a destra
- Dashboard con notifiche push e attività recenti
- Form allineati creazione/dettaglio
- Lista fiere con colonna anno separata
- ordinamento per nome, anno, data, location, settore