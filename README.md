# IDLM ICML Poster

This repository contains the editable ICML poster for:

**IDLM: Inverse-distilled Diffusion Language Models**

## Main Files

- `outputs/idlm_icml_poster.html` - editable poster source.
- `outputs/idlm_icml_poster_36x60.pdf` - exported 36in x 60in poster PDF.
- `outputs/idlm_icml_poster_full_preview.png` - full poster preview image.
- `outputs/idlm_project_qr.png` - QR code pointing to the IDLM project page.
- `outputs/idlm-factorization-large-step.gif` and `outputs/idlm-factorization-small-steps.gif` - blog-inspired visual assets used in the poster.
- `work/` - supporting extracted materials, scripts, paper/code snapshots, and source assets used to build the poster.

## Preview Locally

From the repository root:

```bash
cd outputs
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8000/idlm_icml_poster.html
```

The poster is sized for `60in x 36in`.

## Export PDF

On macOS with Google Chrome installed:

```bash
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --headless=new \
  --disable-gpu \
  --no-first-run \
  --no-default-browser-check \
  --allow-file-access-from-files \
  --print-to-pdf=outputs/idlm_icml_poster_36x60.pdf \
  --no-pdf-header-footer \
  file://"$PWD"/outputs/idlm_icml_poster.html
```

## Notes

The poster is intentionally a single HTML file with local image/GIF assets, so collaborators can edit the text, layout, colors, and figures directly without installing a frontend framework.
