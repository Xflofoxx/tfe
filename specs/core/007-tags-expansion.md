# Specifica: Espansione Sistema Tag - Advanced Tag Management

## Panoramica

Estensione del sistema tag con funzionalità avanzate per categorizzazione, gestione bulk e integrazione intelligente.

## 1. Architettura Tag

### 1.1 Struttura Gerarchica

**Tag Categories**:
- **Business**: Azienda, Settore, Dimensione
- **Product**: Tipo, Prezzo, Innovazione
- **Market**: Target, Geografia, Canale
- **Strategy**: Obiettivo, Budget, Timing

### 1.2 Tag Types

**System Tags** (auto-generated):
- AI-detected tags
- Calculated metrics
- Status indicators

**User Tags** (manual):
- Custom labels
- Project categories
- Priority levels

## 2. Interfaccia Gestione Tag

### 2.1 Pagina: /tags

**Layout**: Dashboard con sidebar

**Sezioni**:
1. **Tag Cloud** - Visualizzazione tutti tag
2. **Categories** - Gestione categorie
3. **Bulk Operations** - Azioni multiple
4. **Analytics** - Statistiche utilizzo

## 3. Tag Cloud

### 3.1 Visualizzazione

**Features**:
- Size by frequency
- Color by category
- Filter by type
- Search functionality

### 3.2 Interazioni

**Click tag**:
- Mostra proposte associate
- Statistiche utilizzo
- Related tags

**Hover**:
- Tooltip con info
- Usage count
- Created date

## 4. Gestione Categorie

### 4.1 CRUD Categorie

**Create Category**:
- Nome categoria
- Descrizione
- Colore (hex)
- Icona (fontawesome)

**Edit/Delete**:
- Modifica proprietà
- Merge categorie
- Delete con reassign

### 4.2 Category Hierarchy

**Struttura**:
```
Business
├── Company
│   ├── Size
│   └── Industry
└── Strategy
    ├── Goals
    └── Budget
```

## 5. Bulk Operations

### 5.1 Multi-Select

**Selezione**:
- Checkbox per tag singoli
- Select all per categoria
- Filter-based selection

### 5.2 Operazioni Bulk

**Azioni disponibili**:
- **Rename**: Cambia nome tag
- **Merge**: Unisci tag simili
- **Delete**: Rimuovi tag
- **Move**: Sposta tra categorie
- **Export**: Esporta lista

### 5.3 Batch Processing

**Progress tracking**:
- Progress bar
- Status updates
- Rollback capability
- Confirmation dialogs

## 6. Analytics Tag

### 6.1 Statistiche Utilizzo

**Metrics**:
- Tag più usati
- Tag per categoria
- Trend temporali
- Coverage per proposta

### 6.2 Tag Relationships

**Network analysis**:
- Tag co-occorrenze
- Correlation matrix
- Recommendation engine

### 6.3 Performance Insights

**Reports**:
- Tag effectiveness
- AI accuracy
- User adoption
- System performance

## 7. Integrazione AI

### 7.1 Auto-Tagging

**Configurazione**:
- Threshold confidence
- Category mapping
- Custom prompts
- Learning feedback

### 7.2 Tag Suggestions

**Smart suggestions**:
- Based on content
- Based on similar proposals
- Based on user history
- Contextual recommendations

### 7.3 Validation AI

**Quality control**:
- Accuracy metrics
- False positive detection
- User feedback loop
- Model retraining

## 8. API Tag Avanzate

### 8.1 Get Tag Analytics

**GET /api/tags/analytics**

**Response**:
```json
{
  "total_tags": 245,
  "categories": {
    "business": 89,
    "product": 67,
    "market": 45,
    "strategy": 44
  },
  "top_tags": [
    {"name": "tech", "count": 156},
    {"name": "startup", "count": 98}
  ],
  "usage_trend": [...]
}
```

### 8.2 Bulk Tag Operations

**POST /api/tags/bulk**

**Input**:
```json
{
  "operation": "merge",
  "tags": ["tag1", "tag2"],
  "target": "merged_tag"
}
```

### 8.3 Tag Recommendations

**GET /api/tags/recommend?proposal_id=123**

**Response**:
```json
{
  "suggested_tags": [
    {"tag": "innovation", "confidence": 0.95},
    {"tag": "tech", "confidence": 0.87}
  ],
  "reasoning": "Based on proposal content analysis"
}
```

## 9. Database Schema

### 9.1 Tag Categories

```sql
CREATE TABLE tag_categories (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  description TEXT,
  color TEXT,
  icon TEXT,
  parent_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (parent_id) REFERENCES tag_categories(id)
);
```

### 9.2 Enhanced Tags

```sql
CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  category_id INTEGER,
  tag_type TEXT DEFAULT 'user', -- 'user' or 'system'
  usage_count INTEGER DEFAULT 0,
  ai_confidence REAL,
  created_by INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES tag_categories(id),
  FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 9.3 Tag Analytics

```sql
CREATE TABLE tag_analytics (
  id INTEGER PRIMARY KEY,
  tag_id INTEGER,
  proposal_id INTEGER,
  action TEXT, -- 'added', 'removed', 'suggested'
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tag_id) REFERENCES tags(id),
  FOREIGN KEY (proposal_id) REFERENCES proposals(id)
);
```

## 10. Sicurezza e Performance

### 10.1 Autorizzazioni

- **Admin**: Gestione categorie, bulk operations
- **User**: CRUD tag propri, analytics read
- **AI**: Auto-tagging permissions

### 10.2 Caching

- Tag cloud cache (Redis)
- Analytics cache (1h TTL)
- Category hierarchy cache

### 10.3 Rate Limiting

- Bulk operations: 10/min
- API calls: 100/min per user
- AI suggestions: 50/min

## 11. Testing

### 11.1 Unit Tests

- Tag CRUD operations
- Category management
- Bulk operations logic
- Analytics calculations

### 11.2 Integration Tests

- Full tag workflow
- AI integration
- Performance under load
- Concurrent operations

### 11.3 E2E Tests

- Tag management UI
- Bulk operations flow
- Analytics dashboard
- Mobile responsiveness

---

**Autore**: Team Development
**Versione**: 1.0.0
**Stato**: Approved
**Ultimo Aggiornamento**: 2026-04-20