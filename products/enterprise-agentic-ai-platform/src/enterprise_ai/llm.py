from __future__ import annotations

import json
from typing import Any

from .config import Settings


class ModelGateway:
    """Provider-neutral chat gateway with a deterministic offline mode."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def _model(self):
        provider = self.settings.model_provider.lower()
        if provider == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(model=self.settings.model_name, temperature=0.2)
        if provider == "watsonx":
            from langchain_ibm import ChatWatsonx

            return ChatWatsonx(
                model_id=self.settings.model_name,
                url=self.settings.watsonx_url,
                project_id=self.settings.watsonx_project_id,
                params={"temperature": 0.2, "max_new_tokens": 1200},
            )
        return None

    def invoke(self, system: str, user: str) -> str:
        model = self._model()
        if model is None:
            return self._deterministic(user)
        response = model.invoke(
            [("system", system), ("human", user)]
        )
        return str(response.content)

    def invoke_json(self, system: str, user: str) -> dict[str, Any]:
        text = self.invoke(system, user)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if start >= 0 and end > start:
                return json.loads(text[start : end + 1])
            return {"summary": text, "recommendations": [], "risks": []}

    @staticmethod
    def _deterministic(user: str) -> str:
        preview = " ".join(user.split())[:500]
        return json.dumps(
            {
                "summary": f"Offline analysis completed for: {preview}",
                "recommendations": [
                    "Validate the business baseline and target outcome.",
                    "Confirm data ownership, quality, access, and retention controls.",
                    "Pilot with human oversight and measurable acceptance criteria.",
                ],
                "risks": [
                    "Unverified data quality",
                    "Unclear accountability or decision rights",
                ],
                "confidence": 0.65,
            }
        )

