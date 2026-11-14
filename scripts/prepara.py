"""Crea l'area privata senza sovrascrivere alcun file già presente."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepara(root=ROOT):
    root = Path(root)
    private = root / 'private'
    private.mkdir(exist_ok=True)
    created = 0
    mapping = {'master-it.md': 'templates/master.md', 'master-en.md': 'templates/master.md',
               **{name: 'templates/' + name for name in
                  ('prove.md', 'aggiornamenti.md', 'preferenze.md', 'scorecard.md', 'tracker.csv')},
               'controlli.json': 'config/controlli.example.json',
               'canva.json': 'config/canva.example.json'}
    for name, source in mapping.items():
        try:
            with (private / name).open('xb') as stream:
                stream.write((root / source).read_bytes())
            created += 1
        except FileExistsError:
            pass
    return created


if __name__ == '__main__':
    print(f'Area privata pronta: {prepara()} nuovi modelli; file esistenti conservati.')
