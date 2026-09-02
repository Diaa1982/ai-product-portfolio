from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Restaurant


EXTRACTION_PROMPT = """Transform the supplied restaurant description, reviews, and image captions into
one Restaurant object. Use only supplied evidence. Do not infer dietary or halal status without an
explicit statement. Preserve uncertainty in descriptions, normalize tags to lowercase, and return
strictly schema-valid structured data."""


def extract_restaurant(payload: dict, image_paths: list[str] | None = None) -> Restaurant:
    """OpenAI structured extraction when configured; deterministic validated mapping otherwise."""
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI

            client = OpenAI()
            content: list[dict] = [{"type": "input_text", "text": json.dumps(payload)}]
            for path in image_paths or []:
                import base64
                mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
                encoded = base64.b64encode(Path(path).read_bytes()).decode()
                content.append({"type": "input_image", "image_url": f"data:{mime};base64,{encoded}"})
            response = client.responses.parse(
                model=os.getenv("RESTAURANT_AI_MODEL", "gpt-5.6"),
                input=[{"role": "system", "content": EXTRACTION_PROMPT},
                       {"role": "user", "content": content}],
                text_format=Restaurant,
            )
            return response.output_parsed
        except ImportError as exc:
            raise RuntimeError("Install the openai extra to use model-backed extraction") from exc
    return Restaurant.model_validate(payload)

