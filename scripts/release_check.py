"""Verifica manifest, link locali e binari pubblici. Non sostituisce Gitleaks."""
import argparse
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote
from pypdf import PdfReader
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT, staged=False):
    root = Path(root)
    names = (root / 'PUBLIC_FILES.txt').read_text(encoding='utf-8').splitlines()
    if names != sorted(set(names)):
        raise ValueError('Manifest non ordinato o duplicato')
    if staged:
        tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
        if sorted(x for x in tracked if x) != names:
            raise ValueError('Indice Git diverso dal manifest revisionato')
        # Il contenuto verificato sul disco deve essere esattamente quello nell’indice.
        subprocess.run(['git', 'diff', '--exit-code', '--', '.'], cwd=root, check=True, capture_output=True)
    for name in names:
        path = root / name
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('File mancante o percorso non ammesso')
        if any(part in {'private', 'runtime', 'candidature', 'sources', 'operativo', '.venv', '.git'} for part in Path(name).parts):
            raise ValueError('Directory privata nel manifest')
        if path.suffix.lower() in {'.zip', '.docx', '.db', '.log', '.pyc', '.exe'} or path.name == '.env':
            raise ValueError('Tipo di file non ammesso')
        if path.suffix == '.pdf':
            reader = PdfReader(path)
            if reader.metadata.author or reader.xmp_metadata or reader.attachments:
                raise ValueError('Metadati o allegati non ammessi nella demo')
            if any(key in reader.trailer['/Root'] for key in ('/OpenAction', '/AA', '/AcroForm')):
                raise ValueError('Azioni o moduli non ammessi nella demo')
            text = '\n'.join(p.extract_text() or '' for p in reader.pages)
            if 'Ada Campione' not in text:
                raise ValueError('PDF non riconosciuto come demo')
            for page in reader.pages:
                for item in page.get('/Annots') or []:
                    obj = item.get_object()
                    if obj.get('/Subtype') != '/Link' or obj.get('/Contents') or obj.get('/T'):
                        raise ValueError('Annotazione non ammessa')
                    action = obj.get('/A').get_object()
                    if action.get('/S') != '/URI' or action.get('/URI') != 'mailto:ada@example.invalid':
                        raise ValueError('Link PDF non previsto')
            continue
        if path.suffix == '.png':
            with Image.open(path) as image:
                if image.getexif() or image.info:
                    raise ValueError('Metadati immagine non previsti')
            with Image.open(path) as image:
                image.verify()
            continue
        text = path.read_text(encoding='utf-8')
        if re.search(r'(?i)[A-Z]:\\Users\\|[/]Users[/]|[/]home[/][^/\s]+[/]', text):
            raise ValueError('Percorso personale in un file pubblico')
        if path.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in link or link.startswith(('mailto:', '#')):
                    continue
                target = (path.parent / unquote(link.split('#')[0])).resolve()
                if not target.is_relative_to(root.resolve()) or not target.exists():
                    raise ValueError(f'Link locale non valido in {name}: {link}')
    return len(names)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    print(f'Verificati {check(staged=args.staged)} file pubblici; link e binari conformi.')
