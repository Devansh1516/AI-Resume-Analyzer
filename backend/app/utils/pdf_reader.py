from __future__ import annotations

import fitz


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Read all text from a PDF using PyMuPDF."""

    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError("The uploaded file could not be read as a valid PDF.") from exc

    text_parts: list[str] = []
    for page in document:
        text_parts.append(page.get_text("text"))

    document.close()
    return "\n".join(text_parts).strip()
