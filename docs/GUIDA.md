# Guida operativa

## Preparazione locale

Installa le dipendenze come nel README e lancia `python scripts/prepara.py`.
La cartella `private/` riceve master IT/EN, prove, aggiornamenti, scorecard,
preferenze, tracker vuoto, configurazione dei controlli e configurazione Canva.
I file già presenti vengono lasciati intatti. Salva gli originali in
`private/originali/` e copia i fatti confermati nei master. Non compilare i modelli
pubblici con dati reali. Mantieni un backup separato.

La configurazione neutra non impone contatti, aziende o titoli. Per controllarli,
modifica `private/controlli.json`: `obbligatori` è una lista di stringhe letterali
da trovare anche nel master; `titoli_esperienze` contiene i titoli originali in
ordine cronologico inverso; `link_obbligatori` contiene URL esatti. Nessuna regex.
`max_pagine` vale 1 e `quota_alta` 0.35. La configurazione non prova la verità dei dati.

## Dall'annuncio al CV

Avvia `$cv-e-lavori` in Codex o `/cv-e-lavori` in Claude Code e incolla URL o testo.
La skill usa gli strumenti web dell'assistente, non uno scraper Python.
Se il link richiede login o non è leggibile, incolla il testo; non serve una chiave API.
Confronta la mappa `requisiti.csv` con le fonti prima di approvare il CV.
Il separatore è `;`, le colonne esatte sono
`requisito;priorita;stato;parole_cv;prova`, da 1 a 12 righe.
`must` indica un requisito esplicito, `nice` una preferenza o un'inferenza dichiarata.
Per dimostrato e trasferibile serve una prova; per gli altri stati i termini in
`parole_cv` non devono comparire nel CV. È un controllo lessicale, non semantico.

Salva ogni candidatura in `private/candidature/<nome-scelto>/`, con nomi nuovi
per le revisioni. Da terminale, ad esempio:

```sh
python scripts/genera_cv.py private/candidature/esempio/CV.md private/candidature/esempio/CV-v1.pdf
python scripts/verifica_pdf.py private/candidature/esempio/CV-v1.pdf private/candidature/esempio/controllo-v1
python scripts/verifica_cv.py private/candidature/esempio/CV-v1.pdf private/candidature/esempio/requisiti.csv --master private/master-it.md --config private/controlli.json
```

Apri ogni PNG del controllo e confronta testo, date, contatti, titoli e metriche
con il master. `esito.json` può contenere metadati del PDF reale: resta privato.
Il secondo lettore `pdftotext` è opzionale e deve essere nel PATH; l'assenza è un
avviso esplicito, un errore del lettore è bloccante. ReportLab produce il PDF;
pypdf e PDFium lo aprono, PDFium estrae il testo per i controlli e rende le pagine.
I font base coprono il testo latino Windows-1252; altri caratteri sono rifiutati
invece di produrre glifi mancanti. Per alfabeti diversi usa il tuo layout Canva
e verifica il PDF. I documenti scansionati non sono supportati.

## Canva, lingue e materiali aggiuntivi

Configura un template di tua disponibilità in `private/canva.json`.
Non è incluso un template pubblico; non occorre accedere al template dell'autore.
Segui la [procedura Canva](../.agents/skills/cv-e-lavori/references/canva.md):
copia, modifica, anteprima, approvazione, esportazione e controllo PDF.
Se manca il connettore o l'accesso, usa la versione a una colonna e dichiara il limite.
Per annunci inglesi usa master EN; non tradurre titoli o livelli in modo da cambiarne il senso.
Cover letter e colloqui si richiedono separatamente: fonti e limiti sono gli stessi.
Aggiorna il tracker solo per lavoro reale, stato preparata; inviata solo su conferma.

## Errori e riproduzione

Input assente, CSV malformato o configurazione errata: correggi prima di continuare.
Dipendenze assenti: installa `requirements.txt` nell'ambiente isolato.
File PDF esistente o cartella controllo esistente: usa un nome nuovo.
Per riprodurre la demo in una cartella nuova:

```sh
python scripts/demo.py --output runtime/demo-nuova
python scripts/demo.py --check
python scripts/release_check.py
```

`--check` rigenera in una directory temporanea e confronta testo Markdown, PDF,
PNG e riepilogo stabile con gli artefatti distribuiti. Per PNG confronta ogni pixel
e metadato, per gli altri file ogni byte. Non sovrascrive la demo.
Le versioni dipendenze sono fissate; cambiare font, librerie o rendering può
cambiare i byte. I risultati pubblicati distinguono i controlli locali da quelli CI.
