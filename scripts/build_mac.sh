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
  --target-architecture arm64 \
  -y \
  run.py

rm -rf build/ pyxis.spec
mkdir -p dist/models
cp scripts/Run-Pyxis.command dist/
chmod +x dist/Run-Pyxis.command

echo ""
echo "Done. Distribute the dist/ folder:"
echo "  dist/Run-Pyxis.command  — double-click in Finder to open Terminal"
echo "  dist/pyxis/pyxis        — run from terminal: ./pyxis/pyxis"
echo "  dist/models/            — drop .gguf files here"
