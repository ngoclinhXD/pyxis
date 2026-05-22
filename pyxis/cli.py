import argparse
import sys

from .engine import ChatEngine
from .models import list_models, resolve_model


def _auto_ctx() -> int:
    import psutil
    gb = psutil.virtual_memory().total / (1024 ** 3)
    if gb < 8:
        return 1024
    elif gb < 16:
        return 2048
    return 4096


_HELP_TEXT = """\
Commands:
  /reset       Clear conversation history
  /model       Switch to a different model
  /model <n>   Switch to model by name or index
  /help        Show this message
  /exit        Quit  (Ctrl-D or Ctrl-C also work)

Input:
  Enter        — new line
  Alt+Enter    — send message
"""


def _make_session():
    from prompt_toolkit import PromptSession
    from prompt_toolkit.formatted_text import HTML
    placeholder = HTML('<ansibrightblack>Alt+Enter (Option+Enter) to send</ansibrightblack>')
    return PromptSession(multiline=True, placeholder=placeholder)


def _read(session, prompt_str: str = "> ") -> str:
    return session.prompt(prompt_str)


def _pick_model(models_dir: str) -> str:
    models = list_models(models_dir)
    if not models:
        print(f"No .gguf files found in '{models_dir}'.")
        print("Download a model and place it there, e.g.:")
        print("  models/gemma-2b-it.Q4_K_M.gguf")
        sys.exit(1)

    print("Available models:")
    for i, m in enumerate(models, 1):
        print(f"  [{i}] {m.name}")

    while True:
        try:
            choice = input("Pick a model (number or name): ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if not choice:
            continue
        try:
            return str(resolve_model(choice, models_dir))
        except (FileNotFoundError, ValueError) as e:
            print(f"  {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pyxis",
        description="Chat with a local GGUF model in your terminal.",
    )
    parser.add_argument("-m", "--model", help="Model filename, partial name, or index")
    parser.add_argument("--system", default=None, help="Override the system prompt")
    parser.add_argument("--ctx", type=int, default=None, help="Context window size (default: auto based on RAM)")
    parser.add_argument("--models-dir", default="models", help="Path to models folder (default: models)")
    args = parser.parse_args()

    model_path = (
        str(resolve_model(args.model, args.models_dir))
        if args.model
        else _pick_model(args.models_dir)
    )

    import os
    ctx = args.ctx if args.ctx is not None else _auto_ctx()
    model_name = os.path.basename(model_path)
    print(f"\nLoading {model_name} (ctx={ctx}) …")

    kwargs = {}
    if args.system:
        kwargs["system_prompt"] = args.system

    engine = ChatEngine(model_path, n_ctx=ctx, **kwargs)

    print("Ready. Alt+Enter to send, Enter for new line. /help for commands.\n")

    session = _make_session()

    while True:
        try:
            user_input = _read(session).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input == "/exit":
            break
        elif user_input == "/help":
            print(_HELP_TEXT)
            continue
        elif user_input == "/reset":
            engine.reset()
            print("Conversation reset.\n")
            continue
        elif user_input == "/model" or user_input.startswith("/model "):
            arg = user_input[len("/model"):].strip()
            if arg:
                try:
                    new_path = str(resolve_model(arg, args.models_dir))
                except (FileNotFoundError, ValueError) as e:
                    print(f"  {e}\n")
                    continue
            else:
                new_path = _pick_model(args.models_dir)
            import os as _os
            print(f"Loading {_os.path.basename(new_path)} (ctx={ctx}) …")
            engine = ChatEngine(new_path, n_ctx=ctx, **kwargs)
            print("Done.\n")
            continue
        elif user_input.startswith("/"):
            print(f"Unknown command '{user_input}'. Type /help for commands.\n")
            continue

        try:
            for token in engine.stream_reply(user_input):
                print(token, end="", flush=True)
            print("\n")
        except KeyboardInterrupt:
            print("\n[interrupted]\n")
            engine.reset()
