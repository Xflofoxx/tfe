# Specifica: Pagina Dettaglio Fiere - Fair Detail View

## Panoramica

Interfaccia dettagliata per visualizzazione e gestione singola fiera con tabs, azioni e analytics.

## 1. URL e Routing

### 1.1 URL Pattern

**/fairs/{fair_id}**

**Parametri**:
- fair_id: UUID della fiera
- tab: tab attivo (opzionale)

### 1.2 Redirects

- Fiera non esistente → 404
- Permessi insufficienti → 403
- Fiera eliminata → Lista fiere

## 2. Layout Pagina

### 2.1 Header

**Informazioni principali**:
- Nome fiera (H1)
- Stato (badge: Draft/Published/Archived)
- Data creazione/modifica
- Proprietario/creatore

**Azioni rapide**:
- Edit
- Duplicate
- Delete
- Export
- Share

### 2.2 Navigation Tabs

**Tabs principali**:
1. **Overview** - Riepilogo generale
2. **Proposals** - Lista proposte associate
3. **Analytics** - Statistiche e insights
4. **Settings** - Configurazione fiera
5. **History** - Cronologia modifiche

## 3. Tab: Overview

### 3.1 Summary Cards

**Metriche chiave**:
- Numero proposte: 24
- Valore totale: €2.4M
- Media punteggio: 7.8/10
- Status distribuzione

### 3.2 Quick Stats

**Grafici mini**:
- Trend proposte (line chart)
- Distribuzione punteggi (bar chart)
- Tag più frequenti (word cloud)

### 3.3 Recent Activity

**Timeline**:
- Ultime proposte aggiunte
- Modifiche punteggi
- Commenti AI
- Azioni utente

## 4. Tab: Proposals

### 4.1 Lista Proposte

**Table columns**:
- Checkbox (bulk select)
- Nome azienda
- Punteggio totale
- Status (Approved/Pending/Rejected)
- Data aggiunta
- Tags principali

**Features**:
- Sortable columns
- Filter by status/tag
- Search by company name
- Pagination (50/page)

### 4.2 Azioni Bulk

**Toolbar**:
- Select all/none
- Approve selected
- Reject selected
- Export selected
- Delete selected

### 4.3 Proposal Cards

**Modal/Expand view**:
- Dettagli completi proposta
- Punteggio breakdown
- AI analysis
- Comments/notes

## 5. Tab: Analytics

### 5.1 Charts Section

**Grafici principali**:
- **Score Distribution**: Istogramma punteggi
- **Tag Frequency**: Bar chart tag più usati
- **Proposal Timeline**: Line chart andamento temporale
- **Geographic Distribution**: Map/chart ubicazioni

### 5.2 Insights AI

**Sezione insights**:
- Top performing proposals
- Common patterns
- Recommendations
- Risk factors

### 5.3 Export Analytics

**Opzioni export**:
- PDF report completo
- CSV dati grezzi
- JSON per integrazioni
- PowerPoint presentation

## 6. Tab: Settings

### 6.1 Fair Configuration

**Campi editabili**:
- Nome fiera
- Descrizione
- Data inizio/fine
- Budget disponibile
- Criteri valutazione

### 6.2 Evaluation Criteria

**Configurazione punteggi**:
- Pesi categorie
- Scale punteggi (1-10, 1-5, etc.)
- Thresholds automatici
- Custom fields

### 6.3 Permissions

**Access control**:
- View permissions
- Edit permissions
- Delete permissions
- Share settings

## 7. Tab: History

### 7.1 Activity Log

**Cronologia completa**:
- Data/ora
- Utente
- Azione
- Dettagli modifica
- Valori precedenti/nuovi

**Filtri**:
- By user
- By action type
- Date range
- Proposal specific

### 7.2 Version Control

**Snapshots**:
- Save current state
- Compare versions
- Restore previous state
- Export version history

## 8. Azioni Globali

### 8.1 Floating Action Button

**Menu rapido**:
- Add proposal
- Generate report
- Share fair
- Quick edit

### 8.2 Keyboard Shortcuts

**Shortcuts**:
- Ctrl+S: Save changes
- Ctrl+E: Edit mode
- Ctrl+F: Search proposals
- Esc: Close modals

## 9. Responsive Design

### 9.1 Desktop (>1024px)

- Full tabs layout
- Multi-column tables
- Side panels

### 9.2 Tablet (768-1024px)

- Collapsed sidebar
- Stacked cards
- Touch-optimized

### 9.3 Mobile (<768px)

- Bottom tabs
- Single column
- Swipe gestures
- Simplified views

## 10. API Integration

### 10.1 Get Fair Detail

**GET /api/fairs/{fair_id}**

**Response**:
```json
{
  "id": "uuid",
  "name": "Tech Fair 2024",
  "status": "published",
  "proposals_count": 24,
  "total_value": 2400000,
  "avg_score": 7.8,
  "created_at": "2024-01-15T10:00:00Z",
  "tabs": {
    "overview": {...},
    "proposals": [...],
    "analytics": {...}
  }
}
```

### 10.2 Update Fair

**PUT /api/fairs/{fair_id}**

**Input**: Partial update object

### 10.3 Bulk Operations

**POST /api/fairs/{fair_id}/bulk**

**Operations**: approve, reject, delete, export

## 11. Performance Optimization

### 11.1 Lazy Loading

- Tab content loaded on demand
- Infinite scroll for proposals
- Progressive image loading

### 11.2 Caching

- Fair data cache (5min)
- Analytics cache (1h)
- Static assets CDN

### 11.3 Database Queries

- Optimized joins
- Index usage
- Query result caching

## 12. Testing

### 12.1 Unit Tests

- Component rendering
- API calls
- State management
- Error handling

### 12.2 Integration Tests

- Full user workflows
- Data loading
- Bulk operations
- Responsive behavior

### 12.3 Performance Tests

- Load times
- Memory usage
- Network requests
- Database queries

---

**Autore**: Team Development
**Versione**: 1.0.0
**Stato**: Approved
**Ultimo Aggiornamento**: 2026-04-20