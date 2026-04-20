# Specifica: Creazione Nuova Fiera - UI/UX Flow

## Panoramica

Interfaccia utente per la creazione guidata di nuove fiere con supporto AI per estrazione automatica dati.

## 1. Pagina Creazione Fiera

### 1.1 URL: /fairs/new

**Layout**:
- Header: "Nuova Fiera"
- Form principale con tabs/steps
- Sidebar: Aiuto e suggerimenti

### 1.2 Step 1: Informazioni Base

**Campi**:
- **URL Fiera** (required)
  - Input text con validazione URL
  - Placeholder: "https://www.fieraitalia.it"
  - Auto-complete da cronologia

- **Sito Azienda** (optional)
  - Input text
  - Placeholder: "https://www.azienda.com"

- **LinkedIn Azienda** (optional)
  - Input text con validazione LinkedIn URL

- **Email Contatto** (optional)
  - Input email con validazione

**Validazioni Client**:
- URL deve iniziare con http:// o https://
- Email deve avere formato valido
- LinkedIn deve contenere "linkedin.com"

## 2. Step 2: Analisi AI (Opzionale)

### 2.1 Generazione Prompt

**Pulsante**: "Genera Prompt AI"

**Elaborazione**:
1. Validazione URL presente
2. Generazione prompt strutturato
3. Copia negli appunti automatica

**Prompt Generato**:
```
Analizza la pagina web della fiera: {url}

Estrai le seguenti informazioni in formato JSON:
{
  "name": "nome ufficiale fiera",
  "description": "descrizione 2-3 frasi",
  "location": "città",
  "venue": "nome centro fieristico",
  "dates": ["data1", "data2"],
  "sector": "settore merceologico",
  "expected_visitors": numero,
  "exhibitors_count": numero,
  "stand_cost": numero,
  "organizer": "nome organizzatore",
  "frequency": "annuale/biennale",
  "edition": "numero edizione",
  "target_segments": ["segmento1", "segmento2"],
  "key_features": ["feature1", "feature2"]
}
```

### 2.2 Estrazione Dati

**Campo**: "JSON Risposta AI"

**Textarea** con:
- Placeholder: "Incolla qui il JSON da ChatGPT/Copilot"
- Validazione JSON
- Pulsante "Estrai Dati"

**Elaborazione**:
1. Parse JSON
2. Mappatura campi form
3. Popolamento automatico campi
4. Feedback successo/errore

## 3. Step 3: Dettagli Fiera

### 3.1 Campi Popolati Automaticamente

**Da AI/Scraping**:
- Nome fiera
- Descrizione
- Location/Venue
- Date
- Settore
- Visitatori/Espositori
- Costo stand

**Campi Manuali Aggiuntivi**:
- **Contatti**
  - Email fiera
  - Telefono
  - Sito web

- **Social Media**
  - Instagram
  - Facebook
  - TikTok

- **Dettagli Logistici**
  - Indirizzo completo
  - Trasporti
  - Parcheggio

### 3.2 Tag Categorizzati

**Tabs per Categoria**:
- **Settori**: selezione multipla
- **Profili Visitatori**: selezione multipla
- **Categorie Prodotto**: selezione multipla

**UI Pattern**:
- Chips selezionati
- Ricerca/filter
- Creazione tag inline (+ pulsante)

## 4. Step 4: Allegati

### 4.1 Upload Area

**Drop Zone** con:
- Drag & drop
- Click to browse
- Multiple files
- Preview thumbnails

**Tipi Supportati**:
- PDF (strategia, preventivi)
- Excel (dati aggiuntivi)
- Immagini (gallery)
- Documenti Word

### 4.2 Gestione File

**Per ogni file**:
- Nome originale
- Dimensione
- Tipo MIME
- Pulsante rimuovi
- Status upload (pending/uploading/complete/error)

**Validazioni**:
- Max 10 file per fiera
- Max 50MB per file
- Tipi permessi: pdf, xlsx, docx, jpg, png

## 5. Salvataggio e Creazione

### 5.1 Pulsante "Crea Fiera"

**Stati**:
- Disabled se campi obbligatori mancanti
- Loading durante salvataggio
- Success con redirect a dettaglio
- Error con messaggi specifici

### 5.2 Elaborazione Backend

1. **Validazione** campi obbligatori
2. **Creazione** record fiera
3. **Upload** file allegati
4. **Estrazione** testo da PDF
5. **Commit** transazione
6. **Redirect** a /fairs/{id}

### 5.3 Feedback Utente

**Success Toast**:
- "Fiera creata con successo!"
- Link "Vai al dettaglio"

**Error Handling**:
- Campi invalidi evidenziati
- Messaggi errore specifici
- Possibilità retry

## 6. Ottimizzazioni UX

### 6.1 Progressive Enhancement

- Form funziona senza JavaScript
- JavaScript aggiunge interattività
- Graceful degradation

### 6.2 Performance

- Lazy loading componenti pesanti
- Debounced validazioni
- Upload chunked per file grandi

### 6.3 Accessibility

- Labels ARIA completi
- Keyboard navigation
- Screen reader support
- High contrast mode

## 7. Analytics e Tracking

### 7.1 Eventi Tracked

- form_start
- ai_prompt_generated
- ai_data_extracted
- file_uploaded
- fair_created
- errors (con tipo)

### 7.2 Metriche UX

- Completion rate per step
- Tempo medio creazione
- Tasso successo AI extraction
- Errori più comuni

## 8. Mobile Responsiveness

### 8.1 Layout Mobile

- Single column
- Tabs diventano accordion
- Touch-friendly controls
- Optimized keyboard

### 8.2 Progressive Web App

- Installabile
- Offline capability (draft save)
- Push notifications (future)

---

**Autore**: Team UX/UI
**Versione**: 1.0.0
**Stato**: Approved
**Ultimo Aggiornamento**: 2026-04-20