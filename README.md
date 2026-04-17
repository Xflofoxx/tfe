# TFE - Trade Fair Evaluator

## Descrizione

Applicazione web per valutare se partecipare a fiere commerciali. Il flusso principale usa AI (ChatGPT/Copilot) per estrarre i dati dalla pagina web della fiera.

## Funzionalità

### Creazione Fiera (Flusso AI)
1. Inserisci URL della fiera nella pagina "Nuova Fiera"
2. Clicca "Genera" → copia il prompt
3. Incolla il prompt in ChatGPT/Copilot
4. Copia il JSON risultato
5. Incolla nel campo "Estrai Dati" e clicca "Estrai"
6. I campi vengono compilati automaticamente

### Import Multiplo
- Usa `/api/fairs/bulk` con più URL
- L'AI genera un array JSON e crea tutte le fiere

### Tag
- Tag personalizzabili con colori
- Deduplicazione automatica su creazione

### Calendario
- Vista annuale con fiere colorate per stato
- Mostra sovrapposizioni

### Stati Fiera
- in_valutazione, approvata, in_gestione, conclusa, rifiutata

## Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: SQLite + SQLAlchemy
- **Frontend**: Bootstrap 5

## Installazione

```bash
pip install -r requirements.txt
python -m uvicorn src.fair_evaluator.main:app --reload --port 8000
```

## API

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/fairs` | GET | Lista fiere |
| `/api/fairs` | POST | Crea fiera singola |
| `/api/fairs/bulk` | POST | Crea più fiere da URL |
| `/api/tags` | GET | Lista tag |
| `/api/tags` | POST | Crea/ottieni tag |
| `/api/tags/bulk` | POST | Crea più tag |

## Pagine

- `/` - Dashboard
- `/fairs` - Lista fiere
- `/fairs/new` - Nuova fiera (+ AI extraction)
- `/fairs/{id}` - Dettaglio fiera
- `/calendar` - Calendario annuale
- `/settings` - Impostazioni Ollama