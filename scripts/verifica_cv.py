"""Controlli euristici del CV: non certificano verità, fit o compatibilità ATS.

Derivato dal verificatore del progetto locale; configurazione e validazione
degli input generalizzate per la distribuzione pubblica.
"""
import argparse
import csv
import json
import logging
import re
import shutil
import subprocess
from pathlib import Path
try:
    import pypdfium2 as pdfium
    from pypdf import PdfReader
except ImportError:
    raise SystemExit('Dipendenze PDF mancanti: python -m pip install -r requirements.txt')
logging.getLogger('pypdf').setLevel(logging.CRITICAL)

DEFAULT = {'max_pagine': 1, 'quota_alta': 0.35, 'obbligatori': [],
           'titoli_esperienze': [], 'link_obbligatori': [],
           'vietati': ['[DA ', '[INSERIRE', 'filecite', '**', "Note d’uso", "Note d'uso"]}
STATI = {'dimostrato', 'trasferibile', 'da_verificare', 'mismatch'}
NUMERO = r'\d+(?:[.,]\d+)*%?'
LIVELLI = r'\b(A1|A2|B1|B2|C1|C2|fluente|fluent|bilingue|bilingual|intermedio|intermediate)\b'


def trova(termine, testo):
    return re.search(r'(?<!\w)' + re.escape(termine.strip()) + r'(?!\w)', testo, re.I)


def configurazione(path=None):
    config = {k: v.copy() if isinstance(v, list) else v for k, v in DEFAULT.items()}
    if path:
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        if not isinstance(data, dict) or set(data) - set(DEFAULT):
            raise ValueError('Configurazione non valida: campi sconosciuti')
        config.update(data)
    if type(config['max_pagine']) is not int or not 1 <= config['max_pagine'] <= 20:
        raise ValueError('max_pagine deve essere un intero tra 1 e 20')
    if type(config['quota_alta']) not in (int, float) or not 0 < config['quota_alta'] <= 1:
        raise ValueError('quota_alta deve essere compresa tra 0 (escluso) e 1')
    for key in ('obbligatori', 'titoli_esperienze', 'link_obbligatori', 'vietati'):
        if not isinstance(config[key], list) or any(not isinstance(x, str) or not x.strip() for x in config[key]):
            raise ValueError(f'{key}: serve una lista di testi non vuoti')
    return config


def leggi_requisiti(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, delimiter=';')
        expected = ['requisito', 'priorita', 'stato', 'parole_cv', 'prova']
        if reader.fieldnames != expected:
            raise ValueError('Colonne CSV attese: ' + ';'.join(expected))
        rows = list(reader)
    if not 1 <= len(rows) <= 12:
        raise ValueError('Inserire da 1 a 12 requisiti')
    seen = set()
    for index, row in enumerate(rows, 2):
        if set(row) != set(expected) or any(value is None for value in row.values()):
            raise ValueError(f'CSV malformato alla riga {index}')
        row.update({key: value.strip() for key, value in row.items()})
        if not row['requisito'] or row['requisito'].casefold() in seen:
            raise ValueError(f'Requisito vuoto o duplicato alla riga {index}')
        seen.add(row['requisito'].casefold())
        if row['priorita'] not in {'must', 'nice'} or row['stato'] not in STATI:
            raise ValueError(f'Priorità o stato non valido alla riga {index}')
        terms = [x.strip() for x in row['parole_cv'].split(',')]
        if not all(terms):
            raise ValueError(f'parole_cv vuoto o malformato alla riga {index}')
        if row['stato'] in {'dimostrato', 'trasferibile'} and not row['prova']:
            raise ValueError(f'Manca la prova alla riga {index}')
    return rows


def controlla_testo(testo, master, requisiti, config):
    errori, avvisi = [], []
    master = master.split("## Note d'uso")[0]
    for value in config['obbligatori']:
        if not trova(value, testo):
            errori.append('Dato obbligatorio assente')
        if not trova(value, master):
            errori.append('Configurazione obbligatoria non riscontrata nel master')
    section = re.search(r'ESPERIENZ[AE]|EXPERIENCE', testo, re.I)
    body = testo[section.end():] if section else ''
    positions = [body.casefold().find(x.casefold()) for x in config['titoli_esperienze']]
    if positions and (min(positions) < 0 or positions != sorted(positions)):
        errori.append('Titoli delle esperienze mancanti o in ordine diverso dalla configurazione')
    for title in config['titoli_esperienze']:
        if not trova(title, master):
            errori.append('Titolo configurato non riscontrato nel master')
    if set(re.findall(NUMERO, testo)) - set(re.findall(NUMERO, master)):
        errori.append('Numero assente dal master')
    if any(not trova(m[0], master) for m in re.finditer(LIVELLI, testo, re.I)):
        errori.append('Livello linguistico non documentato')
    if any(value.casefold() in testo.casefold() for value in config['vietati']):
        errori.append('Marcatore o testo vietato presente')
    zona_alta = testo[:int(len(testo) * config['quota_alta'])]
    coperti = in_alto = must_dim = 0
    for index, row in enumerate(requisiti, 1):
        terms = [x.strip() for x in row['parole_cv'].split(',')]
        presenti = [term for term in terms if trova(term, testo)]
        if row['stato'] in {'da_verificare', 'mismatch'}:
            if presenti:
                errori.append(f'Requisito {index}: affermazione non confermata presente')
            continue
        if row['stato'] == 'dimostrato' and row['priorita'] == 'must':
            must_dim += 1
            if presenti:
                coperti += 1
                if any(trova(term, zona_alta) for term in presenti):
                    in_alto += 1
                else:
                    avvisi.append(f'Requisito {index}: evidenza solo nella parte bassa')
            else:
                errori.append(f'Requisito {index}: obbligatorio dimostrato assente dal CV')
        elif not presenti:
            avvisi.append(f'Requisito {index}: termine non presente')
    return {'errori': errori, 'avvisi': avvisi, 'must_dimostrati': must_dim,
            'coperti': coperti, 'in_alto': in_alto}


def secondo_lettore(pdf, config):
    exe = shutil.which('pdftotext')
    if not exe:
        return [], ['pdftotext assente: secondo lettore non eseguito']
    try:
        result = subprocess.run([exe, '-enc', 'UTF-8', str(pdf), '-'], capture_output=True, timeout=30, check=True)
    except (OSError, subprocess.SubprocessError):
        return ['Secondo lettore fallito: documento non verificato'], []
    text = result.stdout.decode('utf-8', 'replace')
    if not text.strip():
        return ['Secondo lettore: nessun testo'], []
    positions = [text.casefold().rfind(x.casefold()) for x in config['titoli_esperienze']]
    invalid = any(not trova(x, text) for x in config['obbligatori'])
    if positions and (min(positions) < 0 or positions != sorted(positions)):
        invalid = True
    return (['Secondo lettore: dati o ordine non coerenti'] if invalid else []), []


def verifica(pdf, requisiti, master, config=None):
    config = configurazione(config)
    rows = leggi_requisiti(requisiti)
    master_text = Path(master).read_text(encoding='utf-8')
    if not master_text.strip():
        raise ValueError('Master vuoto')
    reader = PdfReader(pdf)
    if reader.is_encrypted or not reader.pages:
        raise ValueError('PDF vuoto o protetto')
    with pdfium.PdfDocument(str(pdf)) as document:
        pages = []
        for index in range(len(document)):
            page = document[index]
            try:
                textpage = page.get_textpage()
                try:
                    pages.append(textpage.get_text_range())
                finally:
                    textpage.close()
            finally:
                page.close()
    if not pages or any(not text.strip() for text in pages):
        raise ValueError('PDF senza testo: OCR non supportato')
    text = '\n'.join(pages).replace('\r\n', '\n').replace('\ufffe', '-').replace('\x02', '-')
    result = controlla_testo(text, master_text, rows, config)
    if len(reader.pages) > config['max_pagine']:
        result['errori'].append('Numero di pagine superiore al limite configurato')
    links = []
    for page in reader.pages:
        for annotation in page.get('/Annots') or []:
            action = annotation.get_object().get('/A')
            if action:
                links.append(str(action.get_object().get('/URI', '')))
    for expected in config['link_obbligatori']:
        if expected not in links:
            result['errori'].append('Link obbligatorio assente')
    errors, warnings = secondo_lettore(pdf, config)
    result['errori'].extend(errors)
    result['avvisi'].extend(warnings)
    if not config['obbligatori'] and not config['titoli_esperienze']:
        result['avvisi'].append('Configurazione neutra: contatti e ordine esperienze non verificati')
    result.update(pagine=len(reader.pages), requisiti=len(rows),
                  esito='non superato' if result['errori'] else 'superato',
                  limite='Controllo euristico: revisione umana dei fatti necessaria')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf')
    parser.add_argument('requisiti')
    parser.add_argument('--master', required=True)
    parser.add_argument('--config')
    args = parser.parse_args()
    try:
        report = verifica(args.pdf, args.requisiti, args.master, args.config)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        raise SystemExit(bool(report['errori']))
    except Exception as error:
        parser.exit(1, f'Input non valido: {type(error).__name__}. Controllare PDF, CSV, master e configurazione.\n')
