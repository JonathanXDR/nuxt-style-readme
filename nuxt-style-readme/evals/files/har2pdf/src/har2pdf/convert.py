"""Rebuild the page sequence from a capture and write the PDF."""

import base64
import json
from io import BytesIO
from pathlib import Path

from PIL import Image
from pypdf import PdfWriter

BOOTSTRAP_PATH = "/api/v3/session"


def convert(capture: str, output: str, *, dpi: int = 300, keep_images: bool = False) -> None:
    with open(capture, encoding="utf-8") as f:
        entries = json.load(f)["log"]["entries"]
    nonce = _bootstrap_nonce(entries)
    pages = _ordered_pages(entries, nonce)
    writer = PdfWriter()
    for index, image_bytes in enumerate(pages):
        image = Image.open(BytesIO(image_bytes))
        if keep_images:
            Path(output).with_suffix(f".{index:04d}.jpg").write_bytes(image_bytes)
        page_pdf = BytesIO()
        image.save(page_pdf, format="PDF", resolution=dpi)
        writer.append(page_pdf)
    with open(output, "wb") as f:
        writer.write(f)


def _bootstrap_nonce(entries: list) -> str:
    for entry in entries:
        if BOOTSTRAP_PATH in entry["request"]["url"]:
            return json.loads(entry["response"]["content"]["text"])["nonce"]
    raise SystemExit("The capture does not include the bootstrap response, so page order cannot be recovered.")


def _ordered_pages(entries: list, nonce: str) -> list:
    pages = []
    for entry in entries:
        # Titles with embedded video interleave MP4 entries, which are not pages.
        if entry["response"]["content"].get("mimeType", "").startswith("video/"):
            continue
        if "/page/" not in entry["request"]["url"]:
            continue
        body = base64.b64decode(entry["response"]["content"]["text"])
        pages.append((_page_index(entry["request"]["url"], nonce), body))
    pages.sort(key=lambda item: item[0])
    return [body for _, body in pages]


def _page_index(url: str, nonce: str) -> int:
    token = url.rsplit("/", 1)[-1]
    return int(token, 16) ^ int(nonce, 16)
