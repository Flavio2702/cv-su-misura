import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import genera_cv
import verifica_cv
import verifica_pdf
import prepara
from pypdf import PdfReader, PdfWriter


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.master = ROOT / 'examples/master.md'
        self.cv = ROOT / 'examples/risposta-sintetica.md'
        self.rows = verifica_cv.leggi_requisiti(ROOT / 'examples/requisiti.csv')

    def check_text(self, text, config=None):
        return verifica_cv.controlla_testo(text, self.master.read_text(encoding='utf-8'), self.rows,
                                         config or verifica_cv.configurazione())

    def test_real_generation_preserves_source_and_text(self):
        digest = hashlib.sha256(self.cv.read_bytes()).digest()
        pdf = self.folder / 'cv.pdf'
        genera_cv.genera(self.cv, pdf)
        reader = PdfReader(pdf)
        self.assertEqual(len(reader.pages), 1)
        text = reader.pages[0].extract_text()
        for fact in ('Ada Campione', '240', '12', '2024', '2025', '2022', '2023', 'Diploma'):
            self.assertIn(fact, text)
        self.assertNotIn('taglio laser', text)
        self.assertEqual(digest, hashlib.sha256(self.cv.read_bytes()).digest())

    def test_metadata_and_no_attachments(self):
        pdf = self.folder / 'cv.pdf'
        genera_cv.genera(self.cv, pdf)
        reader = PdfReader(pdf)
        self.assertFalse(reader.metadata.author)
        self.assertEqual(reader.metadata.creator, 'cv-su-misura')
        self.assertIsNone(reader.xmp_metadata)
        self.assertFalse(reader.attachments)

    def test_no_overwrite_even_same_input(self):
        original = self.cv.read_bytes()
        with self.assertRaises(ValueError):
            genera_cv.genera(self.cv, self.cv)
        pdf = self.folder / 'cv.pdf'
        pdf.write_bytes(b'keep')
        with self.assertRaises(ValueError):
            genera_cv.genera(self.cv, pdf)
        self.assertEqual(pdf.read_bytes(), b'keep')
        self.assertEqual(self.cv.read_bytes(), original)

    def test_missing_input_no_output(self):
        target = self.folder / 'new.pdf'
        with self.assertRaises(OSError):
            genera_cv.genera(self.folder / 'missing.md', target)
        self.assertFalse(target.exists())

    def test_empty_incomplete_placeholder_unicode_rejected(self):
        for text in ('', '# Name', '# Name\nRole\nContact\n[DA CONFERMARE]',
                     '# Name\nRole\nContact\n[INSERIRE]', '# Name\nRole\nContact\n🚀'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                genera_cv.costruisci(text)

    def test_notes_do_not_enter_pdf(self):
        src = self.folder / 'source.md'
        src.write_text(self.cv.read_text(encoding='utf-8') + "\n## Note d'uso\nPRIVATE_SENTINEL", encoding='utf-8')
        pdf = self.folder / 'cv.pdf'
        genera_cv.genera(src, pdf)
        self.assertNotIn('PRIVATE_SENTINEL', PdfReader(pdf).pages[0].extract_text())

    def test_link_and_markup_validation(self):
        self.assertIn('&lt;script&gt;', genera_cv.inline('<script>'))
        for url in ('file:///tmp/file', 'javascript:alert', 'data:text/plain,x'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                genera_cv.inline('[link](' + url + ')')
        self.assertIn('href="https://example.invalid"', genera_cv.inline('[web](https://example.invalid)'))

    def test_neutral_and_personalized_config(self):
        neutral = verifica_cv.configurazione()
        personal = verifica_cv.configurazione(ROOT / 'examples/controlli.json')
        self.assertEqual(neutral['obbligatori'], [])
        self.assertIn('Ada Campione', personal['obbligatori'])
        neutral['obbligatori'].append('other')
        self.assertEqual(verifica_cv.configurazione()['obbligatori'], [])

    def test_bad_config(self):
        for data in ([], {'unknown': 1}, {'max_pagine': True}, {'max_pagine': 0},
                     {'quota_alta': 0}, {'quota_alta': 'x'}, {'obbligatori': 'name'},
                     {'obbligatori': ['']}, {'titoli_esperienze': [1]}):
            path = self.folder / 'config.json'
            path.write_text(json.dumps(data), encoding='utf-8')
            with self.subTest(data=data), self.assertRaises(ValueError):
                verifica_cv.configurazione(path)

    def test_malformed_json(self):
        path = self.folder / 'config.json'
        path.write_text('{', encoding='utf-8')
        with self.assertRaises(ValueError):
            verifica_cv.configurazione(path)

    def test_bad_csv(self):
        header = 'requisito;priorita;stato;parole_cv;prova\n'
        samples = ['', header, 'wrong\n1\n', header + 'a;must;dimostrato;term;\n',
                   header + 'a;must;trasferibile;term;\n', header + 'a;invalid;dimostrato;term;p\n',
                   header + 'a;must;invalid;term;p\n', header + 'a;must;dimostrato;term\n',
                   header + 'a;must;dimostrato;term;p;extra\n', header + 'a;must;dimostrato;;p\n',
                   header + 'a;must;dimostrato;term,;p\n', header + 'a;must;dimostrato;term;p\n' * 2,
                   header + ''.join(f'a{i};must;dimostrato;term;p\n' for i in range(13))]
        for value in samples:
            path = self.folder / 'r.csv'
            path.write_text(value, encoding='utf-8')
            with self.subTest(value=value), self.assertRaises(ValueError):
                verifica_cv.leggi_requisiti(path)

    def test_facts_and_coverage(self):
        result = self.check_text(self.cv.read_text(encoding='utf-8'))
        self.assertEqual(result['errori'], [])
        self.assertEqual(result['coperti'], 2)
        self.assertEqual(result['in_alto'], 2)

    def test_new_number_or_language_rejected(self):
        for suffix in ('\nRisultati 9999', '\nInglese C2', '\nInglese fluente'):
            with self.subTest(suffix=suffix):
                self.assertTrue(self.check_text(self.cv.read_text(encoding='utf-8') + suffix)['errori'])

    def test_unknown_skill_rejected(self):
        self.assertTrue(self.check_text(self.cv.read_text(encoding='utf-8') + '\nTaglio laser')['errori'])

    def test_mismatch_rejected(self):
        self.rows[-1]['stato'] = 'mismatch'
        self.assertTrue(self.check_text(self.cv.read_text(encoding='utf-8') + '\nTaglio laser')['errori'])

    def test_missing_demonstrated_requirement(self):
        text = self.cv.read_text(encoding='utf-8').replace('schede descrittive', 'schede')
        self.assertTrue(self.check_text(text)['errori'])

    def test_markers_rejected(self):
        self.assertTrue(self.check_text(self.cv.read_text(encoding='utf-8') + '\nfilecite')['errori'])

    def test_wrong_experience_order(self):
        config = verifica_cv.configurazione(ROOT / 'examples/controlli.json')
        config['titoli_esperienze'].reverse()
        self.assertTrue(self.check_text(self.cv.read_text(encoding='utf-8'), config)['errori'])

    def test_config_fact_must_be_in_master(self):
        config = verifica_cv.configurazione()
        config['obbligatori'] = ['Dottorato inventato']
        result = self.check_text(self.cv.read_text(encoding='utf-8') + '\nDottorato inventato', config)
        self.assertTrue(result['errori'])

    def test_documented_heuristic_limit(self):
        # Un numero esistente in una nuova frase può passare: questo limite è pubblico.
        result = self.check_text(self.cv.read_text(encoding='utf-8') + '\nCoordinato 240 sedi.')
        self.assertFalse(result['errori'])

    def test_render_and_no_absolute_source_path(self):
        pdf = self.folder / 'cv.pdf'
        genera_cv.genera(self.cv, pdf)
        out = self.folder / 'render'
        result = verifica_pdf.verifica(pdf, out)
        self.assertEqual(result['pagine'], 1)
        self.assertTrue((out / 'pagina-001.png').is_file())
        self.assertTrue((out / 'testo_estratto.txt').is_file())
        self.assertNotIn(str(self.folder), (out / 'esito.json').read_text(encoding='utf-8'))
        with self.assertRaises(ValueError):
            verifica_pdf.verifica(pdf, out)

    def test_pdf_empty_encrypted_and_malformed(self):
        empty = self.folder / 'empty.pdf'
        writer = PdfWriter()
        writer.add_blank_page(100, 100)
        writer.write(empty)
        with self.assertRaises(ValueError):
            verifica_pdf.verifica(empty, self.folder / 'blank')
        writer.encrypt('synthetic-password')
        locked = self.folder / 'locked.pdf'
        writer.write(locked)
        with self.assertRaises(ValueError):
            verifica_pdf.verifica(locked, self.folder / 'locked')
        bad = self.folder / 'bad.pdf'
        bad.write_bytes(b'not a pdf')
        with self.assertRaises(Exception):
            verifica_pdf.verifica(bad, self.folder / 'bad')

    def test_pdf_too_many_pages_and_missing_link(self):
        pdf = self.folder / 'cv.pdf'
        genera_cv.genera(self.cv, pdf)
        writer = PdfWriter()
        page = PdfReader(pdf).pages[0]
        writer.add_page(page)
        writer.add_page(page)
        doubled = self.folder / 'two.pdf'
        writer.write(doubled)
        config = self.folder / 'config.json'
        config.write_text(json.dumps({'link_obbligatori': ['https://example.invalid']}), encoding='utf-8')
        with patch('verifica_cv.shutil.which', return_value=None):
            result = verifica_cv.verifica(doubled, ROOT / 'examples/requisiti.csv', self.master, config)
        self.assertEqual(len(result['errori']), 2)

    def test_missing_second_reader(self):
        with patch('verifica_cv.shutil.which', return_value=None):
            errors, warnings = verifica_cv.secondo_lettore('unused', verifica_cv.configurazione())
        self.assertFalse(errors)
        self.assertIn('non eseguito', warnings[0])

    def test_second_reader_error_and_timeout(self):
        for error in (OSError(), subprocess.TimeoutExpired('tool', 30), subprocess.CalledProcessError(1, 'tool')):
            with self.subTest(error=type(error)), patch('verifica_cv.shutil.which', return_value='fake'), \
                 patch('verifica_cv.subprocess.run', side_effect=error):
                errors, _ = verifica_cv.secondo_lettore('unused', verifica_cv.configurazione())
                self.assertTrue(errors)

    def test_second_reader_success_and_bad_order(self):
        config = verifica_cv.configurazione(ROOT / 'examples/controlli.json')
        text = self.cv.read_bytes()
        with patch('verifica_cv.shutil.which', return_value='fake'), patch('verifica_cv.subprocess.run',
                return_value=subprocess.CompletedProcess('fake', 0, stdout=text)):
            self.assertFalse(verifica_cv.secondo_lettore('unused', config)[0])
            config['titoli_esperienze'].reverse()
            self.assertTrue(verifica_cv.secondo_lettore('unused', config)[0])

    def test_missing_pdf_dependencies(self):
        for script in ('genera_cv.py', 'verifica_cv.py', 'verifica_pdf.py'):
            result = subprocess.run([sys.executable, '-S', str(ROOT / 'scripts' / script)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'Dipendenze PDF mancanti', result.stderr)

    def test_initializer_is_idempotent(self):
        for name in ('templates', 'config'):
            shutil.copytree(ROOT / name, self.folder / name)
        self.assertEqual(prepara.prepara(self.folder), 9)
        master = self.folder / 'private/master-it.md'
        master.write_text('my private original', encoding='utf-8')
        self.assertEqual(prepara.prepara(self.folder), 0)
        self.assertEqual(master.read_text(), 'my private original')

    def test_git_exclusions(self):
        subprocess.run(['git', 'init', '-q', str(self.folder)], check=True, capture_output=True)
        shutil.copyfile(ROOT / '.gitignore', self.folder / '.gitignore')
        paths = ['private/master-it.md', 'runtime/control.json', 'candidature/cv.pdf',
                 'operativo/tracker.csv', 'sources/original.pdf', '.env', '.env.local',
                 '.venv/file', '__pycache__/x.pyc', 'backup.zip', 'run.log', 'db.sqlite']
        result = subprocess.run(['git', 'check-ignore', '-z', '--stdin'], input=('\0'.join(paths) + '\0').encode(),
                                capture_output=True, cwd=self.folder, check=True)
        self.assertEqual(set(result.stdout.decode().strip('\0').split('\0')), set(paths))
        for path in ('.env.example', 'demo/CV.pdf', 'examples/master.md'):
            result = subprocess.run(['git', 'check-ignore', path], cwd=self.folder, capture_output=True)
            self.assertEqual(result.returncode, 1)

    def test_skill_entrypoints_match(self):
        self.assertEqual((ROOT / '.agents/skills/cv-e-lavori/SKILL.md').read_bytes(),
                         (ROOT / '.claude/skills/cv-e-lavori/SKILL.md').read_bytes())


if __name__ == '__main__':
    unittest.main()
