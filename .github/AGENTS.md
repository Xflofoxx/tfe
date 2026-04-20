# Registered Agents

Questo documento registra gli agent custom creati per il progetto TFE.

## spec-code-alignment
**Profilo**: Agente per mantenere l'allineamento bidirezionale tra specifiche e codice.

**Ubicazione**: `.github/agents/spec-code-alignment.agent.md`

**Responsabilità**:
- Verifica che le specifiche siano la fonte di verità in `specs/`
- Assicura che il codice sia modificato in funzione delle specifiche esistenti
- Genera o aggiorna specifiche se il codice implementa comportamenti non ancora specificati
- Allinea issue GitHub alle specifiche corrispondenti

**Quando Usarlo**:
- Verificare coerenza tra specifiche e implementazione
- Creare specifiche per codice senza specifica corrispondente
- Allineare issue GitHub alle specifiche
- Mantenere traccia della spec per ogni pezzo di codice

**Workflow**:
1. Verifica specifiche in `specs/SPEC_INDEX.md`
2. Adatta codice alle specifiche, non il contrario
3. Se solo codice esiste (niente spec): crea nuova specifica
4. Mantieni nomi e struttura coerenti tra spec e code
5. Collega sempre issue GitHub alla specifica pertinente
6. Riporta: specifiche aggiornate/aggiunte, file toccati, issue allineati

---

## spec-code-developer
**Profilo**: Senior developer con 30+ anni di esperienza nello stack del progetto.

**Ubicazione**: `.github/agents/spec-code-developer.agent.md`

**Responsabilità**:
- Legge le specifiche in `specs/` come fonte di verità
- Implementa il codice allineandolo rigorosamente alle specifiche
- Rileva automaticamente cambiamenti nelle specifiche e aggiorna il codice
- Mantiene coerenza tra codice e specifiche durante lo sviluppo

**Tech Stack**:
- Backend: FastAPI, SQLAlchemy, SQLite, Python
- Frontend: Bootstrap 5, Vanilla JavaScript
- AI: Ollama (llama3.2), ChatGPT/Copilot integration
- Tools: ruff (linting), pytest (testing)

**Trigger Automatici**:
- Modifiche in `specs/` folder
- Issue GitHub con riferimenti a specifiche
- PR description che menziona allineamento delle specifiche
- Invocazione manuale con richiesta di implementazione

**Workflow**:
1. Legge SPEC_INDEX.md → Identifica specifiche rilevanti
2. Analizza impact → Trova file di codice da modificare
3. Implementa → Crea/aggiorna codice allineato
4. Valida → Verifica tutti i requisiti spec
5. Segnala → Riporta modifiche e allineamento raggiunto

**Convenzioni**:
- File organization allineata alle specifiche
- Type hints su tutte le funzioni Python
- Commenti legati alle specifiche di riferimento
- Test coverage per logica critica
- Messaggi commit che linkano le specifiche

---

## code-quality-enforcer
**Profilo**: Senior QA engineer con 25+ anni di esperienza che fixa automaticamente problemi di linting e best practices.

**Ubicazione**: `.github/agents/code-quality-enforcer.agent.md`

**Responsabilità**:
- Monitora continuamente il codebase per violazioni di linting
- Fixa automaticamente problemi comuni (ruff, import sorting, formatting)
- Applica standard di best practices Python (PEP 8, type hints)
- Rileva vulnerabilità di sicurezza e problemi di performance
- Mantiene metriche di qualità del codice

**Quando Usarlo**:
- Su ogni salvataggio file in VS Code
- Durante commit Git (pre-commit hooks)
- Su creazione PR
- In pipeline CI/CD
- Manualmente per audit completi

**Workflow Automatico**:
1. **Detection**: Scansiona codice per problemi di qualità
2. **Analysis**: Classifica problemi per rischio e complessità
3. **Fix**: Applica fix sicuri automaticamente, genera suggerimenti per fix complessi
4. **Validation**: Test post-fix e aggiorna metriche qualità
5. **Report**: Genera report qualità e raccomandazioni

**Fix Categories**:
- **Safe Auto-Fix**: Import sorting, formatting, unused imports
- **Review Required**: Refactoring complesso, API changes, performance optimization

**Tech Stack**:
- ruff (linting primario)
- mypy (type checking)
- bandit (security)
- safety (dependencies)
- black (formatting)

---

Creato: 2026-04-20
