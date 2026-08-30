from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from .config import Settings


class MultimodalAnalyzer:
    """Image understanding adapter with an OpenAI vision path and safe fallback."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def analyze(self, image_path: str, question: str) -> str:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(path)
        if self.settings.model_provider.lower() != "openai":
            return (
                f"Image registered for analysis: {path.name} "
                f"({path.stat().st_size} bytes). Configure MODEL_PROVIDER=openai "
                "for semantic vision analysis."
            )
        from langchain_openai import ChatOpenAI

        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        model = ChatOpenAI(model=self.settings.model_name, temperature=0)
        response = model.invoke(
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{encoded}"},
                        },
                    ],
                }
            ]
        )
        return str(response.content)

