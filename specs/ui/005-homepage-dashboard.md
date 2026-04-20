# Specifica: Home Page - Dashboard Principale

## Panoramica

Dashboard principale dell'applicazione che fornisce overview completo dello stato fiere e metriche chiave.

## 1. Layout Generale

### 1.1 Header

**Elementi**:
- Logo/Brand TFE
- Navigation menu (collapse su mobile)
- User menu (profilo, logout)
- Notifications bell (con badge count)

### 1.2 Sidebar Navigation (Opzionale)

**Menu Items**:
- Dashboard (active)
- Fiere
- Calendario
- Tag
- Impostazioni
- Manutenzione

## 2. Metriche Principali (KPIs)

### 2.1 Cards Superiori

**4 Cards principali**:

1. **Totale Fiere**
   - Numero totale fiere nel sistema
   - Trend (+/- vs mese precedente)
   - Icon: calendar

2. **Fiere Attive**
   - Fiere in stato "in_gestione"
   - Sottotitolo: "Da gestire questo mese"
   - Icon: play-circle

3. **Budget Totale**
   - Somma costi stand fiere approvate
   - Formattato in €/$
   - Icon: euro/dollar

4. **ROI Medio**
   - Media valutazioni ROI
   - Badge: Alto/Medio/Basso
   - Icon: trending-up

### 2.2 Calcolo Metriche

**Query Database**:
```sql
-- Totale fiere
SELECT COUNT(*) FROM fairs WHERE archived = 'no'

-- Fiere attive
SELECT COUNT(*) FROM fairs WHERE status = 'in_gestione' AND archived = 'no'

-- Budget totale
SELECT SUM(stand_cost) FROM fairs WHERE status IN ('approvata', 'in_gestione', 'conclusa')

-- ROI medio
SELECT AVG(
  CASE
    WHEN roi_assessment->>'assessment' = 'high' THEN 3
    WHEN roi_assessment->>'assessment' = 'medium' THEN 2
    ELSE 1
  END
) FROM fairs WHERE roi_assessment IS NOT NULL
```

## 3. Grafici e Visualizzazioni

### 3.1 Distribuzione Stati Fiere

**Tipo**: Donut Chart

**Dati**:
- in_valutazione: count, %
- approvata: count, %
- in_gestione: count, %
- conclusa: count, %
- rifiutata: count, %

**Colori**:
- in_valutazione: giallo
- approvata: verde
- in_gestione: blu
- conclusa: grigio
- rifiutata: rosso

### 3.2 Trend Mensile

**Tipo**: Line Chart

**Dati**: Numero fiere create per mese (ultimi 12 mesi)

**Features**:
- Tooltip con valori esatti
- Zoom su periodi
- Export PNG/PDF

### 3.3 Top Settori

**Tipo**: Bar Chart Orizzontale

**Dati**: Top 10 settori per numero fiere

**Calcolo**:
```sql
SELECT t.name, COUNT(ft.fair_id) as count
FROM tags t
JOIN fair_tags ft ON t.id = ft.tag_id
WHERE t.category = 'sector'
GROUP BY t.id, t.name
ORDER BY count DESC
LIMIT 10
```

## 4. Liste Rapide

### 4.1 Fiere Recenti

**Titolo**: "Fiere Recenti"

**Colonne**:
- Nome fiera (link a dettaglio)
- Stato (badge colorato)
- Data creazione
- Azioni (quick actions)

**Azioni**:
- 👁️ View details
- ✏️ Edit
- 🗑️ Archive

### 4.2 Fiere da Valutare

**Titolo**: "Da Valutare"

**Filtro**: status = 'in_valutazione' AND allegati presenti

**Azioni Prioritarie**:
- 🚀 Avvia valutazione
- 📎 Gestisci allegati

### 4.3 Prossime Scadenze

**Titolo**: "Prossime Fiere"

**Calcolo**:
- Fiere con date future
- Ordinate per data più vicina
- Max 5 elementi

## 5. Azioni Rapide

### 5.1 Pulsanti Principali

**Posizione**: Top right dell'header

1. **+ Nuova Fiera**
   - Link: /fairs/new
   - Icon: plus-circle
   - Primary button

2. **Import Excel**
   - Link: /import
   - Icon: upload
   - Secondary button

### 5.2 Quick Actions Menu

**Dropdown con**:
- Esporta dati
- Pulisci database (admin)
- Aggiorna statistiche
- Refresh dashboard

## 6. Notifiche e Alert

### 6.1 System Alerts

**Tipi**:
- **Info**: "5 fiere da valutare"
- **Warning**: "Budget superato per 2 fiere"
- **Error**: "Errore sincronizzazione dati"

### 6.2 User Notifications

**WebSocket Integration**:
- Nuove fiere create
- Valutazioni completate
- Errori sistema
- Reminder scadenze

## 7. Responsive Design

### 7.1 Desktop (>1024px)

- Layout 3 colonne
- Sidebar sempre visibile
- Cards full width

### 7.2 Tablet (768-1024px)

- Layout 2 colonne
- Sidebar collassabile
- Cards adattive

### 7.3 Mobile (<768px)

- Single column
- Header hamburger menu
- Cards stacked
- Swipe gestures per navigazione

## 8. Performance

### 8.1 Lazy Loading

- Grafici caricato on-demand
- Liste paginate
- Immagini lazy load

### 8.2 Caching

- Metriche cache per 5 minuti
- Grafici cache per 1 ora
- Liste cache per 1 minuto

### 8.3 Real-time Updates

- WebSocket per notifiche
- Auto-refresh metriche (opzionale)
- Background sync dati

## 9. Personalizzazione

### 9.1 User Preferences

- Layout preferito (cards/list)
- Metriche da mostrare
- Periodo default grafici
- Tema (light/dark)

### 9.2 Dashboard Config

- Ordinamento widgets
- Visibilità sezioni
- Custom KPIs
- Export layout

## 10. Analytics Integration

### 10.1 Tracking Eventi

- page_view: dashboard
- interaction: chart_click, filter_apply
- conversion: new_fair_created, evaluation_started

### 10.2 Performance Metrics

- Load time dashboard
- User engagement (time on page)
- Feature usage (clicks per section)

---

**Autore**: Team UX/UI
**Versione**: 1.0.0
**Stato**: Approved
**Ultimo Aggiornamento**: 2026-04-20