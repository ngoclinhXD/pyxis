#!/usr/bin/env bash
set -e

pip install pyinstaller
pip install -r requirements.txt -q

pyinstaller \
  --onedir \
  --name pyxis \
  --collect-all llama_cpp \
  --collect-all psutil \
  --collect-all prompt_toolkit \
  -y \
  run.py

rm -rf build/ pyxis.spec
mkdir -p dist/models
cp scripts/Run-Pyxis.sh dist/
chmod +x dist/Run-Pyxis.sh

echo ""
echo "Done. Distribute the dist/ folder:"
echo "  dist/Run-Pyxis.sh       — run to open Pyxis in terminal"
echo "  dist/pyxis/pyxis        — run directly: ./pyxis/pyxis"
echo "  dist/models/            — drop .gguf files here"
