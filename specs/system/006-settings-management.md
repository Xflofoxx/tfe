# Specifica: Gestione Impostazioni - System Configuration

## Panoramica

Modulo per la configurazione e gestione delle impostazioni di sistema, utente e integrazione AI.

## 1. Tipi di Impostazioni

### 1.1 Impostazioni Sistema

**Globali, gestite da admin**:
- Limiti upload (max file size, count)
- Timeout operazioni
- Rate limiting
- Feature flags

### 1.2 Impostazioni Utente

**Per utente/organizzazione**:
- Strategia aziendale
- Preferenze UI
- Notifiche
- Integrazioni esterne

### 1.3 Impostazioni AI

**Configurazione Ollama**:
- URL server
- Modello default
- Timeout richieste
- Fallback behavior

## 2. Interfaccia Impostazioni

### 2.1 Pagina: /settings

**Layout**: Tabs verticali

**Tabs**:
1. **AI & LLM**
2. **Strategia Aziendale**
3. **Preferenze UI**
4. **Sistema**
5. **Integrazioni**

## 3. Tab: AI & LLM

### 3.1 Configurazione Ollama

**Campi**:
- **Ollama URL**
  - Input: text
  - Default: http://localhost:11434
  - Validazione: URL raggiungibile

- **Modello AI**
  - Select dropdown
  - Opzioni: auto-detect da /api/tags
  - Default: llama3.2

- **Timeout (secondi)**
  - Input: number
  - Range: 10-300
  - Default: 120

### 3.2 Test Connessione

**Pulsante**: "Test Connessione"

**Elaborazione**:
1. Chiamata GET {url}/api/tags
2. Parsing risposta modelli disponibili
3. Aggiornamento select modello
4. Feedback: ✅ Connesso | ❌ Errore

### 3.3 Status AI

**Display realtime**:
- Stato connessione: Online/Offline
- Modello attivo
- Versione Ollama
- Modelli disponibili

## 4. Tab: Strategia Aziendale

### 4.1 Strategia Testuale

**Campo**: Textarea multilinea

**Contenuto**:
- Obiettivi aziendali
- Target mercato
- Budget disponibile
- Criteri partecipazione fiere

**Esempio**:
```
Azienda: Prodotti elettronici consumer
Obiettivi: Espansione mercato Europa, lancio nuovi prodotti
Budget annuale fiere: €500.000
Criteri: Min 5000 visitatori, settore tech/electronics
```

### 4.2 Upload PDF Strategia

**File Upload**:
- Tipo: PDF only
- Max size: 10MB
- Salvataggio: data/strategy/
- Estrazione automatica testo

### 4.3 Preview e Edit

**Modal/Tabs**:
- Edit testo
- Preview PDF
- Extracted text (read-only)

## 5. Tab: Preferenze UI

### 5.1 Tema

**Select**:
- Light (default)
- Dark
- Auto (system)

### 5.2 Layout Dashboard

**Opzioni**:
- Compact
- Comfortable
- Custom (drag&drop widgets)

### 5.3 Notifiche

**Toggles**:
- Email notifications
- Browser notifications
- Sound alerts
- Weekly reports

### 5.4 Lingua

**Select**:
- Italiano (default)
- English
- Español

### 6.1 Limiti Sistema

**Upload Settings**:
- Max upload size: 10MB (default)
- Max files per fair: 50 (default)
- Allowed file types: PDF, DOC, DOCX, XLS, XLSX, JPG, PNG

**Performance**:
- Cache TTL: 3600 secondi (default)
- Background jobs concurrency: 5 (default)
- Session timeout: 3600 secondi (default)

**Security**:
- Password policy: JSON config
- Audit logging: enabled/disabled
- API keys management

## 7. Tab: Integrazioni

### 7.1 Webhooks

**Configurazione**:
- Webhooks enabled: toggle
- Webhook URL: text input
- Webhook secret: password field
- Events: checkbox list (fair_created, fair_updated, analysis_completed)

### 7.2 API Keys

**Gestione**:
- Lista API keys attive
- Generate new key
- Revoke existing keys
- Key permissions (read, write, admin)

## 8. API Settings

### 8.1 Endpoints

```
GET    /api/settings           # Ottieni tutte le impostazioni
POST   /api/settings           # Aggiorna impostazioni
POST   /api/settings/reset     # Reset alle impostazioni default
GET    /api/settings/ollama-status  # Status connessione Ollama
```

### 8.2 Response Format

```json
{
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.2",
  "ollama_timeout": 120,
  "strategy_prompt": "...",
  "ui_theme": "light",
  "max_upload_size": 10485760,
  "webhooks_enabled": false,
  "api_keys": [...]
}
```

## 9. Database Schema

### Settings Table

```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    -- AI Settings
    ollama_url TEXT DEFAULT 'http://localhost:11434',
    ollama_model TEXT DEFAULT 'llama3.2',
    ollama_timeout INTEGER DEFAULT 120,
    ollama_fallback_enabled TEXT DEFAULT 'yes',

    -- Business Strategy
    strategy_prompt TEXT,
    strategy_pdf_path TEXT,
    business_objectives TEXT,
    target_markets JSON,
    annual_budget REAL,
    participation_criteria JSON,

    -- UI Preferences
    ui_theme TEXT DEFAULT 'light',
    ui_compact_mode TEXT DEFAULT 'no',
    notifications_enabled TEXT DEFAULT 'yes',
    email_notifications TEXT DEFAULT 'yes',
    language TEXT DEFAULT 'it',

    -- System Settings
    max_upload_size INTEGER DEFAULT 10485760,
    max_files_per_fair INTEGER DEFAULT 50,
    cache_ttl INTEGER DEFAULT 3600,
    background_jobs_concurrency INTEGER DEFAULT 5,
    password_policy JSON,
    session_timeout INTEGER DEFAULT 3600,
    audit_logging TEXT DEFAULT 'yes',

    -- Integrations
    webhooks_enabled TEXT DEFAULT 'no',
    webhook_url TEXT,
    webhook_secret TEXT,
    api_keys JSON,

    -- Legacy
    default_network_path TEXT
);
```

## 10. Validazione e Sicurezza

### 10.1 Input Validation

- **URL validation**: Per ollama_url, webhook_url
- **File size limits**: Controllo max_upload_size
- **JSON validation**: Per campi complessi (target_markets, api_keys, etc.)
- **Range checks**: Per timeout, concurrency, etc.

### 10.2 Permissions

- **Admin only**: Modifica impostazioni sistema
- **User level**: Preferenze UI, strategia aziendale
- **Audit logging**: Tutte le modifiche tracciate

## 11. Test Cases

### 11.1 Funzionalità Core
- ✅ Salvataggio impostazioni
- ✅ Reset impostazioni
- ✅ Validazione input
- ✅ Test connessione Ollama

### 11.2 Integration
- ✅ UI reflects settings changes
- ✅ API respects limits
- ✅ Webhooks fire on events
- ✅ File upload respects size limits

### 11.3 Security
- ✅ Input sanitization
- ✅ Permission checks
- ✅ Audit logging
- ✅ API key management

### 6.1 Limiti Upload

**Campi** (admin only):
- Max file size (MB): 1-100
- Max files per fiera: 1-50
- Allowed extensions: csv

### 6.2 Performance

**Settings**:
- Cache TTL (minutes)
- Database connection pool
- Background jobs concurrency

### 6.3 Sicurezza

**Options**:
- Password policy
- Session timeout
- API rate limiting
- Audit logging

## 7. Tab: Integrazioni

### 7.1 Webhooks

**Configurazione**:
- URL endpoint
- Eventi da notificare
- Auth token
- Retry policy

### 7.2 API Keys

**Gestione**:
- Genera nuove chiavi
- Revoca esistenti
- Scopes permessi
- Expiration date

### 7.3 Export/Import

**Backup settings**:
- Export JSON
- Import da file
- Reset to defaults

## 8. API Impostazioni

### 8.1 Get Settings

**GET /api/settings**

**Response**:
```json
{
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.2",
  "strategy_prompt": "Strategia aziendale...",
  "ui_theme": "light",
  "notifications_enabled": true
}
```

### 8.2 Update Settings

**POST /api/settings**

**Input**: Partial object

**Validazioni**:
- URL format
- Required fields
- Type checking

### 8.3 Reset Settings

**POST /api/settings/reset**

**Opzioni**:
- Reset all
- Reset category
- Reset to defaults

## 9. Persistence

### 9.1 Database Schema

```sql
CREATE TABLE settings (
  id INTEGER PRIMARY KEY,
  ollama_url TEXT,
  ollama_model TEXT,
  strategy_prompt TEXT,
  strategy_pdf_path TEXT,
  ui_theme TEXT DEFAULT 'light',
  notifications_enabled BOOLEAN DEFAULT true,
  language TEXT DEFAULT 'it',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9.2 File Storage

- PDF strategia: data/strategy/
- Backup settings: data/backups/
- Logs: data/logs/

## 10. Sicurezza

### 10.1 Autorizzazioni

- Admin: tutte le impostazioni
- User: solo proprie preferenze
- Guest: read-only settings pubblici

### 10.2 Validazione

- Input sanitization
- SQL injection prevention
- XSS protection
- CSRF tokens

### 10.3 Audit

- Logging tutte le modifiche
- Versioning settings
- Rollback capability

## 11. Testing

### 11.1 Unit Tests

- Validazione input
- Connessione AI
- File upload
- Database operations

### 11.2 Integration Tests

- End-to-end settings flow
- AI connectivity
- File processing
- UI updates

---

**Autore**: Team Development
**Versione**: 1.0.0
**Stato**: Approved
**Ultimo Aggiornamento**: 2026-04-20