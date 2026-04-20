# Specifica: Sistema Tag Avanzato

## Obiettivo
Sistema completo di categorizzazione delle fiere con tag gerarchici, analytics, AI e deduplicazione automatica.

## Modello Dati

### Tag
- id: Integer (PK, autoincrement)
- name: String (unique, nullable=False)
- color: String (default="#3b82f6")
- category_id: Integer (FK a TagCategory)
- tag_type: String ('user' o 'system', default='user')
- usage_count: Integer (default=0)
- ai_confidence: Float (per tag generati da AI)
- created_by: Integer (user ID che ha creato il tag)
- created_at: String
- updated_at: String

### TagCategory
- id: Integer (PK, autoincrement)
- name: String (nullable=False, unique)
- description: Text
- color: String (default="#3b82f6")
- icon: String (fontawesome icon name)
- parent_id: Integer (FK self per gerarchie)
- created_at: String

### TagAnalytics
- id: Integer (PK, autoincrement)
- tag_id: Integer (FK a Tag)
- fair_id: String (FK a Fair, nullable)
- action: String ('added', 'removed', 'suggested', 'merged')
- timestamp: String

## Funzionalità Core

### 1. Categorizzazione Gerarchica
- Categorie principali: sector, visitor_profile, product_category
- Sottocategorie illimitate (parent/child relationship)
- Icone e colori personalizzabili per categoria

### 2. Tag Types
- **User**: Creati manualmente dagli utenti
- **System**: Generati automaticamente dal sistema/AI
- AI confidence score per tag suggeriti

### 3. Analytics e Tracking
- Usage count per tag
- Storico azioni (added/removed/suggested/merged)
- Tracking per fiera specifica

### 4. Deduplicazione Intelligente
- Normalizzazione automatica (lowercase, trim)
- Merge manuale di duplicati
- Prevenzione creazione duplicati

## API

### Tag CRUD
- `GET /api/tags` - Lista tag con filtri (category, type, search)
- `POST /api/tags` - Crea tag (deduplicazione automatica)
- `PUT /api/tags/{id}` - Aggiorna tag
- `DELETE /api/tags/{id}` - Elimina tag
- `POST /api/tags/merge` - Unisci tag duplicati
- `POST /api/tags/bulk` - Crea multipli tag

### Categorie
- `GET /api/tag-categories` - Lista categorie (con gerarchia)
- `POST /api/tag-categories` - Crea categoria
- `PUT /api/tag-categories/{id}` - Aggiorna categoria

### Analytics
- `GET /api/tags/{id}/analytics` - Storico tag
- `GET /api/fairs/{id}/tag-analytics` - Analytics per fiera

## UI

### /tags - Gestione Tag
- **Tabs per categoria** con struttura gerarchica
- **CRUD completo** con preview colori
- **Merge tool** per duplicati
- **Bulk operations** per categorie
- **Search e filtri** avanzati

### Scheda Fiera
- **Multi-select categorizzati** (Settori | Profili | Categorie)
- **Tag chips** con colori
- **Auto-complete** intelligente
- **Tag suggeriti da AI** con confidence score

### Analytics Dashboard
- **Usage statistics** per tag
- **Trending tags** nel tempo
- **Tag distribution** per categoria

## Workflow AI Integration

### Tag Suggestion
1. Durante creazione/aggiornamento fiera
2. Analisi testo (description, sector, etc.)
3. Generazione tag candidati con confidence
4. Presentazione suggerimenti all'utente

### Auto-categorization
1. Pattern recognition su dati esistenti
2. Creazione tag system automatici
3. Aggiornamento usage_count

## Test Cases

### Funzionalità Core
- ✅ Creazione tag con categoria
- ✅ Deduplicazione automatica
- ✅ Merge manuale duplicati
- ✅ Gerarchia categorie
- ✅ Analytics tracking

### Integration
- ✅ Multi-select in scheda fiera
- ✅ AI tag suggestion
- ✅ Bulk operations
- ✅ Search e filtri

### Performance
- ✅ Query ottimizzate con indici
- ✅ Caching per categorie frequenti
- ✅ Bulk operations efficienti
- Filtro fiere per tag
- Deduplicazione