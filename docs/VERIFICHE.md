# Verifiche della distribuzione

Data: 14 novembre 2026. Test su dati sintetici, senza credenziali personali o
chiamate a pagamento. Le ricevute dettagliate locali e l'inventario privato non
sono inclusi nel repository.

## Ambiente e risultati locali

- Windows x64, Python 3.14.0; installazione in ambiente virtuale dedicato e seconda
  installazione pulita senza cache su copia dei soli 49 file pubblici: superate.
  `pip check` superato; inizializzazione crea 9 modelli e al secondo passaggio
  non sovrascrive nulla. Avvio rapido eseguito fino alla demo e ai controlli.
- ReportLab 4.5.1, pypdf 6.11.0, pypdfium2 5.15.0, Pillow 13.0.0,
  charset-normalizer 3.5.2. Dipendenze fissate in requirements.txt.
- 30 test automatici superati, nessun test saltato. PDF generati e aperti realmente.
- Demo rigenerata: Markdown, PDF, PNG, JSON e README identici ai 5 artefatti distribuiti.
- Una pagina, 3 requisiti, 2 obbligatori dimostrati presenti anche nella parte alta.
- Secondo lettore pdftotext 4.00 (Xpdf) eseguito aggiungendolo al PATH: nessun errore o avviso.
  Provata anche l'assenza: avviso esplicito, non una falsa attestazione di doppia lettura.
- Anteprima PNG della demo vista: testo leggibile, nessun taglio, sovrapposizione o
  glifo mancante. Metadati neutri, nessun XMP, allegato, commento o modulo.

## Riproduzione

```sh
python -m pip install -r requirements.txt
python -m pip check
python -m unittest discover -s tests -v
python scripts/demo.py --check
python scripts/release_check.py --staged
gitleaks dir . --redact
gitleaks git . --log-opts="--all" --redact
```

La verifica di release confronta l'indice con PUBLIC_FILES.txt, controlla i link
locali, i metadati dei binari e alcuni percorsi identificativi. Non è un rilevatore
universale di dati personali. Una revisione mirata separata controlla identità e
personalizzazioni del progetto sorgente, senza pubblicare i valori cercati.
Gitleaks 8.30.1 viene verificato con il checksum ufficiale, senza allowlist aggiunte.
La revisione mirata dei 49 file non ha trovato le personalizzazioni identificative
del sorgente. Impronte dei 90 file originali esaminati invariate. Link locali validi;
i riferimenti pubblici sono stati controllati via HTTP prima della pubblicazione.

## CI e limiti delle prove

Il [workflow](../.github/workflows/verify.yml) esegue installazione, test, demo e
manifest su Windows/Linux con Python 3.12, 3.13 e 3.14; un job separato controlla
file e intera nuova cronologia con Gitleaks. Gli esiti effettivi sono nella
[pagina GitHub Actions](https://github.com/Flavio2702/cv-su-misura/actions/workflows/verify.yml).
La presenza del workflow non è da sola prova di successo: controllare il run del commit.

Assenza di dipendenze e fallimenti del secondo lettore sono simulati; il rendering
PDF principale è reale. Gli scenari AI/Canva sono [revisioni di procedura](SCENARI.md),
non prove live. Non verificati: qualità delle risposte di modelli diversi, login,
copia/modifica/export live Canva, comportamento di ATS o selezionatori reali.
Nessun supporto DOCX/OCR da collaudare: non era presente nel progetto sorgente.
