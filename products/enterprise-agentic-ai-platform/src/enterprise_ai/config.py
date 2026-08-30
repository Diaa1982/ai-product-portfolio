from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    model_provider: str = "deterministic"
    model_name: str = "gpt-4.1-mini"
    openai_api_key: str | None = None
    watsonx_apikey: str | None = None
    watsonx_project_id: str | None = None
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    knowledge_dir: Path = Path("data/knowledge")
    vector_dir: Path = Path("data/vector_store")
    audit_log: Path = Path("data/audit.jsonl")
    execution_log: Path = Path("data/executions.jsonl")
    use_case_config: Path = Path("config/use_cases.yaml")
    human_approval_required: bool = True
    high_risk_threshold: int = 70

    def load_use_cases(self) -> dict:
        with self.use_case_config.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)["use_cases"]


@lru_cache
def get_settings() -> Settings:
    return Settings()

