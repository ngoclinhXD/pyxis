# Pyxis

Chat with local GGUF models (Gemma, Llama, etc.) entirely in your terminal — no internet required.

> Named after Pyxis, the compass constellation.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> **macOS (Apple Silicon):** `llama-cpp-python` will compile with Metal support automatically. For GPU acceleration on other platforms see the [llama-cpp-python docs](https://github.com/abetlen/llama-cpp-python).

## Add a model

Drop any `.gguf` file into the `models/` folder:

```
models/
  gemma-2b-it.Q4_K_M.gguf
  llama-3-8b-instruct.Q5_K_M.gguf
```

You can find quantized models on [Hugging Face](https://huggingface.co/models?library=gguf).

## Usage

```bash
# Interactive model picker
pyxis

# Skip the picker
pyxis -m gemma
pyxis -m 1          # by index number

# Options
pyxis --ctx 8192                        # larger context window
pyxis --system "You are a pirate."      # custom system prompt
pyxis --models-dir ~/my-models          # use a different folder
```

### Chat commands

| Command  | Action                          |
|----------|---------------------------------|
| `/reset` | Clear conversation history      |
| `/help`  | Show available commands         |
| `/exit`  | Quit (Ctrl-D / Ctrl-C also work)|

## Building a standalone executable

Requires building natively on each platform (cross-compilation is not supported).

**macOS (Apple Silicon)**
```bash
pip install -r requirements-dev.txt
bash scripts/build_mac.sh
```

For Intel Macs, edit `build_mac.sh` and change `--target-architecture arm64` to `x86_64`.

**Windows**
```bat
scripts\build_win.bat
```

The build produces a `dist/` folder — this is what you distribute:

```
dist/
├── pyxis                  (or pyxis.exe on Windows)
├── Run-Pyxis.command      (or Run-Pyxis.bat on Windows)
└── models/
```

**Two ways to launch:**
- **Double-click** `dist/Run-Pyxis.command` (Mac) / `dist/Run-Pyxis.bat` (Windows) — opens a terminal window automatically.
- **From terminal:** `./dist/pyxis` (or `./dist/pyxis.exe`)

**Models:** drop `.gguf` files into `dist/models/`. The `models/` at the project root is for development only (when running via `pip install -e .`).

> **macOS Gatekeeper:** first run on another Mac may be blocked. Right-click → Open, or run once: `xattr -dr com.apple.quarantine dist/`
