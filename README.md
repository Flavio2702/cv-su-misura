# CV su misura

**Da un annuncio a un CV pertinente, con una prova dietro ogni affermazione.**

Progetto portfolio di **Flavio2702**: una skill per Codex e Claude Code che
accompagna l'adattamento del CV, più strumenti Python per generare e controllare PDF.
Incolli il link o il testo dell'annuncio; l'assistente confronta i requisiti con
il tuo profilo locale e prepara una proposta da rivedere.

Guarda la **[demo commentata](demo/README.md)**, il **[CV sintetico](demo/CV.md)**
o il **[PDF generato](demo/CV.pdf)**. Si consultano senza installazione.
La risposta testuale della demo è sintetica e predisposta: nessuna chiamata AI live.
Il PDF e i controlli sono eseguiti realmente dal codice.

## Il problema e le capacità dimostrate

Adattare un CV richiede scegliere evidenze pertinenti senza trasformare un requisito
dell'annuncio in una competenza mai posseduta. Il progetto separa la proposta
dell'assistente dai controlli ripetibili e rende visibili i punti da confermare.

- Mappa requisiti → prove, con stati dimostrato, trasferibile, da verificare e mismatch.
- Profilo e preferenze locali, CV italiano/inglese, scorecard e tracker delle candidature.
- Testo Markdown, PDF a una colonna e procedura Canva su una copia del proprio template.
- Controlli su numeri, livelli linguistici, termini, pagine, link e ordine delle esperienze.
- Cover letter e preparazione colloqui su richiesta, senza invii automatici.

Il portfolio mostra progettazione di procedure AI, configurazione riutilizzabile,
elaborazione PDF, test di errore e separazione dei dati privati. Non attribuisce
esperienze professionali o risultati di selezione all'autore.

## Prova locale in pochi comandi

Serve **Python 3.12–3.14**. Nessuna chiave e nessun account Canva per la demo.

```sh
git clone https://github.com/Flavio2702/cv-su-misura.git
cd cv-su-misura
python -m venv .venv
```

Attiva l'ambiente: Windows PowerShell `.venv/Scripts/Activate.ps1`;
macOS/Linux `source .venv/bin/activate`. Poi:

```sh
python -m pip install -r requirements.txt
python scripts/demo.py --check
python -m unittest discover -s tests -v
python scripts/prepara.py
```

`prepara.py` crea modelli vuoti in `private/` senza sovrascrivere quelli esistenti.
Inserisci lì il tuo master, le prove e le preferenze: [guida operativa](docs/GUIDA.md).
Apri il repository in Codex e richiama `$cv-e-lavori`, oppure `/cv-e-lavori` in
Claude Code, seguito dal link dell'annuncio. Se la skill non compare, riapri il
progetto e indica direttamente il suo file `SKILL.md`.

## Cosa è automatico e cosa richiede un assistente

Python genera e controlla i documenti. Lettura dell'annuncio, fit, riformulazione,
cover letter, colloqui e Canva sono procedure eseguite dall'assistente con i suoi
strumenti disponibili: **non un servizio autonomo né un client API incluso**.
Se il link non è accessibile serve il testo; se Canva manca resta il PDF locale.
Accesso, costi e trattamento dati di AI e Canva dipendono dai servizi scelti.

## Verifiche, limiti e privacy

I test non usano credenziali o servizi a pagamento. I controlli sui fatti sono
euristici: non rilevano ogni invenzione, scambio di numeri o cambio di significato.
Non garantiscono il superamento degli ATS o il successo della candidatura.
Il controllo visivo resta necessario; il generatore base supporta testo latino,
non OCR o impaginazioni DOCX. Canva e qualità AI non sono collaudati live.

I dati reali restano in cartelle ignorate da Git. Questo evita commit accidentali
in quei percorsi, **non impedisce l'invio ai servizi AI quando li usi**.
Non inserire documenti personali nelle issue. [Privacy e limiti](docs/PRIVACY.md).

- [Guida operativa](docs/GUIDA.md) e [architettura](docs/ARCHITETTURA.md)
- [Matrice capacità e verifiche](docs/COPERTURA.md)
- [Risultati effettivi dei test](docs/VERIFICHE.md) e [scenari assistiti](docs/SCENARI.md)
- [Provenienza e fonti](docs/PROVENIENZA.md), [dipendenze](THIRD_PARTY_NOTICES.md)

Sviluppato con assistenza AI (OpenAI Codex). [Apache License 2.0](LICENSE) per
i contributi originali concedibili, copyright 2026 Flavio2702; [NOTICE](NOTICE).
È un progetto dimostrativo, senza garanzie di titolarità assoluta o idoneità alla produzione.
