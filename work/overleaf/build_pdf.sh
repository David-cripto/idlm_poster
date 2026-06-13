#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEXBIN="$HOME/Library/TinyTeX/bin/universal-darwin"

export PATH="$TEXBIN:$PATH"
cd "$ROOT"

latexmk -pdf -interaction=nonstopmode -synctex=1 "${1:-main_arxiv.tex}"
