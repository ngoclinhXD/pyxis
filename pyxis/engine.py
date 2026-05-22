from pathlib import Path
from typing import Iterator

from llama_cpp import Llama

_DEFAULT_SYSTEM = "You are a helpful assistant."


class ChatEngine:
    def __init__(
        self,
        model_path: str | Path,
        system_prompt: str = _DEFAULT_SYSTEM,
        n_ctx: int = 4096,
        n_gpu_layers: int = -1,
    ) -> None:
        self._llm = Llama(
            model_path=str(model_path),
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=False,
        )
        self._system_prompt = system_prompt
        self._messages: list[dict] = [{"role": "system", "content": system_prompt}]

    def stream_reply(self, user_text: str) -> Iterator[str]:
        self._messages.append({"role": "user", "content": user_text})
        stream = self._llm.create_chat_completion(
            messages=self._messages,
            stream=True,
        )
        collected = []
        for chunk in stream:
            delta = chunk["choices"][0]["delta"].get("content", "")
            if delta:
                collected.append(delta)
                yield delta
        self._messages.append({"role": "assistant", "content": "".join(collected)})

    def reset(self) -> None:
        self._messages = [{"role": "system", "content": self._system_prompt}]
