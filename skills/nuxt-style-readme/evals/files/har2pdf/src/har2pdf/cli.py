"""Entry point for the `har2pdf` command.

Usage: har2pdf CAPTURE.har -o OUTPUT.pdf [--dpi 300] [--keep-images]
"""

import argparse

from .convert import convert


def main() -> int:
    parser = argparse.ArgumentParser(prog="har2pdf")
    parser.add_argument("capture", help="HAR file that includes the bootstrap response")
    parser.add_argument("-o", "--output", required=True, help="path of the PDF to write")
    parser.add_argument("--dpi", type=int, default=300, help="render resolution")
    parser.add_argument("--keep-images", action="store_true", help="keep the extracted page images")
    args = parser.parse_args()
    convert(args.capture, args.output, dpi=args.dpi, keep_images=args.keep_images)
    return 0
