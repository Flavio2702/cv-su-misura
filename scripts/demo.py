"""Rigenera la demo sintetica senza servizi esterni né sovrascritture."""
import argparse
import json
import tempfile
from pathlib import Path
from genera_cv import genera
from verifica_pdf import verifica as verifica_pdf
from verifica_cv import verifica as verifica_cv

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ('CV.md', 'CV.pdf', 'anteprima.png', 'controlli.json', 'README.md')


def build(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    cv = ROOT / 'examples/risposta-sintetica.md'
    (destination / 'CV.md').write_bytes(cv.read_bytes())
    genera(cv, destination / 'CV.pdf')
    with tempfile.TemporaryDirectory() as tmp:
        rendering = Path(tmp) / 'render'
        pdf = verifica_pdf(destination / 'CV.pdf', rendering)
        if pdf['pagine'] != 1:
            raise ValueError('La demo deve avere una pagina')
        (destination / 'anteprima.png').write_bytes((rendering / 'pagina-001.png').read_bytes())
    checks = verifica_cv(destination / 'CV.pdf', ROOT / 'examples/requisiti.csv',
                         ROOT / 'examples/master.md', ROOT / 'examples/controlli.json')
    if checks['errori']:
        raise ValueError('Controlli demo non superati')
    stable = {key: checks[key] for key in ('pagine', 'requisiti', 'must_dimostrati', 'coperti', 'in_alto', 'errori', 'esito', 'limite')}
    stable.update(metadati=pdf['metadati'], xmp_presente=pdf['xmp_presente'], allegati=pdf['allegati'],
                  ai='Risposta sintetica predisposta; nessuna chiamata live',
                  secondo_lettore='Opzionale; esito effettivo nel log di esecuzione',
                  controllo_visivo='Richiede revisione umana; vedere docs/VERIFICHE.md')
    (destination / 'controlli.json').write_text(json.dumps(stable, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    (destination / 'README.md').write_text('''# Demo sintetica: da un annuncio al CV

Persona, organizzazioni, date e risultati sono interamente inventati.
La fase di adattamento è una **risposta sintetica predisposta**, non una chiamata
live a un modello. PDF, PNG e controlli sono generati davvero dal progetto.

1. [Annuncio](../examples/annuncio.md): catalogazione e schede descrittive obbligatorie.
2. [Master](../examples/master.md): le evidenze disponibili, prima della selezione.
3. [Mappa requisiti/prove](../examples/requisiti.csv): due dimostrati, uno da verificare.
4. [CV risultante](CV.md) e [PDF](CV.pdf): stessi fatti, punti selezionati per il ruolo.
5. [Controlli eseguiti](controlli.json): pagine, copertura lessicale e metadati.

La proposta porta in alto catalogazione e schede, elimina due punti meno pertinenti
e mantiene titoli, date e formazione. Non attribuisce il taglio laser, non documentato.
Fit qualitativo favorevole sui due obbligatori; niente punteggio senza scorecard
configurata. Retribuzione e seniority restano domande aperte. Nessuna candidatura inviata.

![Anteprima del CV inventato](anteprima.png)

Riproduci con `python scripts/demo.py --check` dalla radice. La CI confronta gli
artefatti con una nuova generazione, senza credenziali e senza aggiornare tracker.
La qualità delle risposte AI e Canva live non è dimostrata da questo esempio.
''', encoding='utf-8', newline='\n')
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'demo'
            checks = build(folder)
            for name in ARTIFACTS:
                if (folder / name).read_bytes() != (ROOT / 'demo' / name).read_bytes():
                    raise SystemExit('Demo diversa: ' + name)
        print('Demo riproducibile: 5 artefatti identici.')
    else:
        checks = build(args.output)
        print('Demo generata in una nuova directory.')
    print(json.dumps(checks, ensure_ascii=False))


if __name__ == '__main__':
    main()
