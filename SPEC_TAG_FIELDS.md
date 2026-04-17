# Specifica: Tag per Settore, Profilo Visitatori e Categorie Prodotto

## Obiettivo
Trasformare i campi `settore`, `profilo visitatori` e `categorie prodotto` delle fiere in tag, con:
- Possibilità di creare/gestire tag da una schermata dedicata
- Colori personalizzabili
- Selezionemultipla dalla scheda fiera
- Deduplicazione automatica (stessi nomi = stesso tag)

## Modello Dati

### Tag esistenti (già presente)
- id, name, color, category, created_at

### Nuovo: TagCategory (enum)
- `sector` - settore merceologico
- `visitor_profile` - profilo visitatori  
- `product_category` - categorie prodotto

### Fair: modificare campi esistenti
- `sector` → rimuovere, usare `tags` (many-to-many) con category filter
- `visitor_profile` → rimuovere, usare `tags` con category filter
- `product_categories` → rimuovere, usare `tags` con category filter

## API

### GET /api/tags?category=sector
Ritorna solo tag di una categoria

### POST /api/tags
Aggiungi `category` al body

### PUT /api/fairs/{id}
Aggiornare `tag_ids` (lista)

## UI

### /tags - Gestione Tag
- Tab per categoria (Settori | Profili | Categorie)
- CRUD tag con colori
- Merge duplicati

### Scheda Fiera
- Select multipla per settore
- Select multipla per profilo  
- Select multipla per categorie

## Test
- Creazione tag con category
- Selezione multipla nella scheda
- Filtro fiere per tag
- Deduplicazione