from pathlib import Path


def list_models(models_dir: str | Path = "models") -> list[Path]:
    return sorted(Path(models_dir).glob("*.gguf"))


def resolve_model(name_or_index: str, models_dir: str | Path = "models") -> Path:
    models = list_models(models_dir)
    if not models:
        raise FileNotFoundError(f"No .gguf files found in '{models_dir}'")

    # numeric index
    if name_or_index.isdigit():
        idx = int(name_or_index) - 1
        if not (0 <= idx < len(models)):
            raise ValueError(f"Index {name_or_index} out of range (1–{len(models)})")
        return models[idx]

    # exact or partial filename match
    needle = name_or_index.lower()
    matches = [m for m in models if needle in m.name.lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(m.name for m in matches)
        raise ValueError(f"Ambiguous model name '{name_or_index}' matches: {names}")
    raise FileNotFoundError(f"No model matching '{name_or_index}' in '{models_dir}'")
