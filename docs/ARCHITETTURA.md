# Architettura e scelte

```text
Link/testo annuncio + profilo locale
  → assistente: fit, requisiti/prove, proposta Markdown
  → revisione umana
  → Canva su copia oppure genera_cv.py
  → PDF → verifica_pdf.py (testo + PNG + metadati)
        → verifica_cv.py (euristiche + CSV + config + master)
  → revisione visiva e dei fatti → tracker locale
```

La skill è istruzione operativa; gli script non generano prosa AI e non fanno
chiamate web. Non esistono API key, database, dashboard o server nel runtime.
I due entrypoint per assistenti contengono la stessa skill: i test ne verificano
l'allineamento. I riferimenti dettagliati sono condivisi nella versione Codex.

I tre script derivano dal progetto sorgente. La personalizzazione del verificatore
è stata spostata in JSON locale; il generatore mantiene struttura e stili a una
colonna, aggiungendo metadati neutri, validazione dei link e scrittura esclusiva.
L'estrattore mantiene pypdf e PDFium; non scrive più il percorso assoluto nel report.
La validazione CSV precede i controlli; i messaggi sui fatti non ripetono i valori.

La demo usa una risposta sintetica predisposta: seleziona punti documentati nel
master inventato. Serve a verificare il tratto Markdown → PDF → controlli, non a
misurare la qualità di un modello. I test negativi mutano solo dati sintetici.
L'assenza di un SDK AI/Canva è una caratteristica del progetto, non una funzionalità
rimossa per la pubblicazione. Le procedure del connettore restano disponibili.
