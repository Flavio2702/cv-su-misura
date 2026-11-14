# Capacità → implementazione → verifica

Le capacità assistite sono procedure per un modello con strumenti. La revisione
di uno scenario non equivale a un test live dell'assistente o del servizio.

| Capacità del progetto sorgente | Distribuzione riutilizzabile | Evidenza e limite |
| --- | --- | --- |
| Annuncio tramite URL o testo | Skill, passo 1 | Scenari 1–2; nessuno scraper automatico |
| Fit, esclusioni, punteggio e dati contrattuali | Skill + scorecard locale | Scenari 3–4; criteri neutri, nessuna inferenza legale |
| Aggiornamenti confermati e fonti IT/EN | Modelli locali + regole skill | Scenari 5–6; revisione umana |
| Mappa requisiti/prove | CSV validato da verifica_cv.py | Test CSV, stati, requisito obbligatorio, demo |
| Domande mirate, selezione e riformulazione | Skill + adattamento.md | Scenari 5–7; qualità AI non misurata |
| CV Markdown | Proposta assistita + fixture sintetica | Demo consultabile, sorgente invariato nei test |
| PDF a una colonna | genera_cv.py, logica e stili conservati | Generazione reale, testo, metadati, link, no sovrascrittura |
| Canva su copia, impaginazione e export | canva.json locale + procedura mantenuta | Scenari 8–11; nessun template privato, nessun collaudo live |
| Estrazione e anteprima PDF | verifica_pdf.py, pypdf/PDFium | Test rendering reale, file vuoti/protetti/malformati, PNG visto |
| Numeri, livelli, termini e ordine esperienze | verifica_cv.py + JSON locale | Test positivi/negativi; limite semantico dimostrato da test |
| Secondo lettore | pdftotext da PATH | Lettura locale reale; assenza, timeout, errore e ordine simulati |
| Tracker e preferenze permanenti | Modelli + regole skill | Scenari 12–13; nessuna scrittura remota o invio automatico |
| Cover letter, mini-caso e colloqui | Skill, sezione su richiesta | Scenario 14; procedure, non generatore Python |
| Isolamento dei dati e configurazioni | prepara.py, gitignore, manifest | Test esclusioni/idempotenza, audit file, Gitleaks |
| Servizi AI, modelli, credenziali assenti | Fallback espliciti nella skill | Scenari 2, 8–11, 15; nessun SDK API nel progetto sorgente |
| Formati DOCX o OCR | Non presenti nel progetto sorgente | Non introdotti; nessuna capacità rimossa |

La copertura conserva i formati Markdown, CSV, PDF, PNG e JSON. Le procedure di
cover letter e colloquio restano testuali. Non sono promessi dashboard, hosting,
nuove integrazioni o esiti professionali. Risultati: [VERIFICHE.md](VERIFICHE.md).
