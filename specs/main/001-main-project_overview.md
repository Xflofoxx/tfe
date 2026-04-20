# TFE - Trade Fair Evaluator

## Obiettivo
Valutare fiere commerciali per decidere se partecipare, analizzando dati da web con AI.

## Stack
- Backend: FastAPI + SQLite + SQLAlchemy
- Frontend: Bootstrap 5
- AI: Ollama (llama3.2) + ChatGPT/Copilot

## Modello Dati

### Fair
- id (String, PK): UUID univoco
- name, year, duration_days
- url, description
- location, venue, address
- dates (JSON array)
- sector, organizer, frequency, edition
- expected_visitors, exhibitors_count, stand_cost
- status (in_valutazione, approvata, in_gestione, conclusa, rifiutata)
- tags (m:n con Tag)
- web_sources, extraction_regions
- folder_path, network_path (per sincronizzazione)
- target_segments, sources (JSON)
- company_website, company_linkedin, fair_email
- gallery, attachments, contacts (JSON)
- scraped_data, historical_data, ROI_assessment, cost_estimate
- recommendation, rationale
- report_pdf_path, report_html_path
- exhibitor_countries, visitor_profile, product_categories, key_features (JSON)
- instagram, facebook, tiktok
- ai_analysis_enabled, ai_last_updated
- previous_editions (JSON)
- archived
- contact_list (relazione m:n con Contact)

### Tag
- id, name, color, category_id (FK a TagCategory)
- tag_type ('user' o 'system')
- usage_count, ai_confidence
- created_by, created_at, updated_at
- category_obj (relazione con TagCategory)

### TagCategory
- id, name, description, color, icon
- parent_id (per categorie gerarchiche)
- created_at
- parent, children, tags (relazioni)

### TagAnalytics
- id, tag_id, fair_id, action, timestamp
- tag, fair (relazioni)

### Contact (m:n con Fair)
- id, name, email, phone, company, role
- linkedin, notes, created_at
- fairs (relazione m:n via fair_contacts)

### CommercialProposal
- id, fair_id, name, file_path, file_name
- total_amount, stand_size, stand_location, services (JSON)
- status, notes, received_at, expires_at
- fair (relazione)

### FairAnalysis
- id, fair_id, name, parameters, result, summary, created_at
- fair (relazione)

### OfferComponent
- id, fair_id, name, category, description
- quantity, unit_price, total_price, notes, created_at
- fair (relazione)

### Settings
- Configurazioni AI (ollama_url, model, timeout, fallback)
- Strategia aziendale (strategy_prompt, pdf_path, objectives, markets, budget, criteria)
- Preferenze UI (theme, compact_mode, notifications, language)
- Impostazioni sistema (upload_size, cache_ttl, concurrency, etc.)
- Integrazioni (webhooks, api_keys)

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
- `GET /api/fairs` - Lista fiere
- `GET /api/fairs/{id}` - Dettaglio fiera
- `PUT /api/fairs/{id}` - Aggiorna fiera
- `DELETE /api/fairs/{id}` - Elimina fiera
- `POST /api/fairs/{id}/attachments` - Upload allegati
- `POST /api/fairs/{id}/analyze` - Analisi AI della fiera

### Analisi Fiere
- `GET /api/fairs/{id}/analyses` - Lista analisi
- `POST /api/fairs/{id}/analyses` - Crea analisi
- `DELETE /api/fairs/{id}/analyses/{analysis_id}` - Elimina analisi

### Componenti Offerta
- `GET /api/fairs/{id}/components` - Lista componenti
- `POST /api/fairs/{id}/components` - Crea componente
- `PUT /api/fairs/{id}/components/{comp_id}` - Aggiorna componente
- `DELETE /api/fairs/{id}/components/{comp_id}` - Elimina componente

### Contatti
- `GET /api/fairs/{id}/contacts` - Lista contatti fiera
- `POST /api/fairs/{id}/contacts` - Aggiungi contatto
- `DELETE /api/fairs/{id}/contacts/{contact_id}` - Rimuovi contatto

### Proposte Commerciali
- `POST /api/fairs/{id}/proposals` - Upload proposta
- `GET /api/fairs/{id}/proposals` - Lista proposte
- `DELETE /api/fairs/{id}/proposals/{proposal_id}` - Elimina proposta

### Tag
- `GET /api/tags` - Lista tag
- `POST /api/tags` - Crea/ottieni tag (deduplicazione)
- `PUT /api/tags/{id}` - Aggiorna tag
- `DELETE /api/tags/{id}` - Elimina tag
- `POST /api/tags/merge` - Unisci tag duplicati
- `POST /api/tags/bulk` - Crea tag multipli
- `GET /api/tags/analytics` - Analytics globali tag
- `GET /api/tags/{id}/analytics` - Analytics tag specifico

### Impostazioni
- `GET /api/settings` - Ottieni impostazioni
- `PUT /api/settings` - Aggiorna impostazioni

### Tag
- `GET /api/tags` - Lista tag
- `POST /api/tags` - Crea/ottieni tag (deduplicazione)
- `PUT /api/tags/{id}` - Aggiorna tag
- `DELETE /api/tags/{id}` - Elimina tag
- `POST /api/tags/merge` - Unisci tag duplicati
- `POST /api/tags/bulk` - Crea tag multipli

### Categorie Tag
- `GET /api/tag-categories` - Lista categorie
- `POST /api/tag-categories` - Crea categoria
- `PUT /api/tag-categories/{id}` - Aggiorna categoria

### Impostazioni
- `GET /api/settings` - Ottieni impostazioni
- `POST /api/settings` - Aggiorna impostazioni
- `POST /api/settings/reset` - Reset impostazioni
- `GET /api/settings/ollama-status` - Stato Ollama

### Notifiche
- `GET /api/notifications/stream` - Stream notifiche
- `GET /api/notifications` - Lista notifiche

### Upload e File
- `POST /api/upload-strategy` - Carica strategia aziendale
- `POST /api/extract-pdf` - Estrai testo da PDF
- `POST /api/upload-pdf` - Carica PDF generico
- `POST /api/fairs/{id}/attachments` - Allegati fiera

### Sincronizzazione
- `POST /api/scan-network-folder` - Scansiona cartella rete
- `POST /api/sync-from-network-folder` - Sincronizza da rete

### Calendario
- `GET /calendar` - Vista annuale con colori per stato

## UI Pages
- `/` - Dashboard
- `/fairs` - Lista fiere
- `/fairs/new` - Nuova fiera + AI extraction
- `/fairs/{id}` - Dettaglio fiera
- `/calendar` - Calendario annuale
- `/settings` - Impostazioni Ollama