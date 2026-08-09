# har2pdf

Rebuild a paginated e-book as a single PDF from a captured HAR file.

> [!NOTE]
> har2pdf targets an undocumented reader endpoint that was mapped by observation. The format can change without warning, and a given capture only stays usable for as long as its session nonce is valid.

## Features

- 📄 **HAR to PDF:** Reconstructs the full page sequence from one capture and writes a single PDF.
- 🔑 **Nonce-based ordering:** Recovers page order from the per-title nonce in the bootstrap response.
- 🖼️ **Pillow decoding:** Decodes each page image through Pillow, including newer WebP builds.
- 🎞️ **Video-aware:** Skips interleaved MP4 entries in titles that embed video.
- 🔍 **Adjustable resolution:** Sets the PDF render resolution with `--dpi`, defaulting to 300.
- 💾 **Image retention:** Writes the extracted page images alongside the PDF with `--keep-images`.

## Requirements

- Python 3.11 or newer.

## Installation

From the project root:

```bash
pip install .
```

This installs the dependencies (`pypdf>=5`, `pillow>=11`) and the `har2pdf` command.

## Usage

```bash
har2pdf CAPTURE.har -o OUTPUT.pdf
```

The capture must include the bootstrap response (`/api/v3/session`); it carries the per-title nonce used to order pages, so a capture started mid-session cannot be processed.

Set a different render resolution and keep the extracted images:

```bash
har2pdf CAPTURE.har -o OUTPUT.pdf --dpi 200 --keep-images
```

With `--keep-images`, each page is written next to the output as `OUTPUT.0000.jpg`, `OUTPUT.0001.jpg`, and so on.

## Options

| Argument | Description | Default |
| --- | --- | --- |
| `capture` | HAR file that includes the bootstrap response. | required |
| `-o`, `--output` | Path of the PDF to write. | required |
| `--dpi` | Render resolution. | `300` |
| `--keep-images` | Keep the extracted page images. | off |

## Limitations

- 🕒 **Nonce expiry:** The nonce rotates roughly every 24 hours, so an old capture cannot be re-processed.
- 🚪 **Bootstrap required:** Captures started after the `/api/v3/session` response are unusable.
- 📐 **WebP spreads:** Pages served as WebP on newer reader builds decode correctly, but the page-size heuristic mis-detects spreads.
- ⚠️ **Undocumented endpoint:** No public documentation exists for the endpoint; behavior was derived by observation and may break without warning.

## License

MIT. See [LICENSE](./LICENSE).
