#!/bin/sh
# Headless Chrome print of generated HTML to PDF.
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cd "$(dirname "$0")/out" && for f in *.html; do "$C" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="${f%.html}.pdf" "$f"; done
