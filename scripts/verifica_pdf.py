"""Estrae il testo e renderizza tutte le pagine di un PDF testuale."""

import argparse
import json
import logging
from pathlib import Path

try:
    from pypdf import PdfReader
    import pypdfium2 as pdfium
except ImportError:
    raise SystemExit('Dipendenze PDF mancanti: python -m pip install -r requirements.txt')
logging.getLogger('pypdf').setLevel(logging.CRITICAL)


def verifica(source: Path, output: Path) -> dict:
    if not source.is_file():
        raise ValueError(f"PDF non trovato: {source}")
    if output.exists():
        raise ValueError("La destinazione deve essere una directory nuova")

    reader = PdfReader(source)
    if reader.is_encrypted:
        raise ValueError("PDF protetto: fornire una copia leggibile")
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    if not pages or any(not text for text in pages):
        raise ValueError("PDF senza pagine o con pagine senza testo estraibile")

    output.mkdir(parents=True, exist_ok=False)
    with pdfium.PdfDocument(str(source)) as document:
        if len(document) != len(pages):
            raise ValueError("Numero di pagine incoerente tra lettura e rendering")
        for index in range(len(document)):
            page = document[index]
            bitmap = page.render(scale=1.5)
            try:
                picture = bitmap.to_pil()
                try:
                    picture.save(output / f"pagina-{index + 1:03d}.png")
                finally:
                    picture.close()
            finally:
                bitmap.close()
                page.close()

    (output / "testo_estratto.txt").write_text("\n\n".join(pages), encoding="utf-8")
    result = {"pagine": len(pages),
              "metadati": dict(reader.metadata or {}),
              "xmp_presente": reader.xmp_metadata is not None,
              "allegati": len(reader.attachments),
              "caratteri_per_pagina": [len(text) for text in pages],
              "controllo_automatico": "superato", "controllo_visivo": "da eseguire"}
    (output / "esito.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(verifica(args.pdf, args.output), ensure_ascii=False))
    except Exception as error:
        parser.exit(1, f"Verifica PDF fallita ({type(error).__name__}): controllare input e destinazione.\n")
