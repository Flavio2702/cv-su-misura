# Dipendenze e avvisi

Il repository non include sorgenti o binari delle dipendenze: vengono installati
da PyPI nell'ambiente locale. Le loro licenze restano quelle dei rispettivi
autori. La licenza Apache del progetto non le sostituisce. Versioni e licenze
sono state confrontate con i metadati dei pacchetti installati.

| Componente | Versione | Licenza dichiarata | Fonte primaria |
| --- | --- | --- | --- |
| ReportLab | 4.5.1 | BSD, dettagli nel license.txt del pacchetto | [ReportLab](https://www.reportlab.com/opensource/) |
| pypdf | 6.11.0 | BSD-3-Clause | [Licenza](https://github.com/py-pdf/pypdf/blob/main/LICENSE) |
| pypdfium2 | 5.15.0 | BSD-3-Clause / Apache-2.0; ulteriori licenze dipendenze | [Licenze e PDFium](https://github.com/pypdfium2-team/pypdfium2#licensing) |
| Pillow | 13.0.0 | MIT-CMU | [Licenza](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| charset-normalizer | 3.5.2 | MIT | [Licenza](https://github.com/jawah/charset_normalizer/blob/master/LICENSE) |

pypdfium2 distribuisce PDFium e componenti con propri avvisi: conservarli se si
ridistribuiscono i pacchetti o un eseguibile. Consultare i file LICENSE del wheel,
non presumere che tutto PDFium sia coperto dalla sola licenza del wrapper.
ReportLab contiene risorse di font con avvisi propri; la demo usa Helvetica base
del PDF e non distribuisce un file di font separato.

Strumenti di verifica, non incorporati: Python (PSF), Git (GPL-2.0), Gitleaks 8.30.1
([MIT](https://github.com/gitleaks/gitleaks/blob/master/LICENSE)). Il lettore
pdftotext è opzionale e può provenire da [Xpdf](https://www.xpdfreader.com/)
oppure [Poppler](https://poppler.freedesktop.org/): verificare la licenza della
distribuzione installata; nessun suo binario è incluso qui. GitHub Actions checkout e
setup-python sono [MIT](https://github.com/actions/checkout/blob/main/LICENSE)
e [MIT](https://github.com/actions/setup-python/blob/main/LICENSE); nel workflow
sono fissati a revisioni upstream. Nessuna azione di terzi riceve dati personali.

Canva, Codex e Claude Code sono servizi/prodotti separati, con proprie condizioni.
Nessun loro account, abbonamento, marchio grafico o template è incluso nella licenza
del progetto. Gli esempi biografici e l'annuncio sono inventati per la demo.
