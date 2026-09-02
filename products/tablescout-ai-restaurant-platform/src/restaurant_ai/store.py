from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from pydantic import TypeAdapter, ValidationError

from .models import Restaurant


class KnowledgeBase:
    """Validated JSON knowledge base with atomic writes and append-only audit events."""

    def __init__(self, path: str | Path, audit_path: str | Path = "audit/events.jsonl"):
        self.path = Path(path)
        self.audit_path = Path(audit_path)

    def load(self) -> list[Restaurant]:
        if not self.path.exists():
            return []
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return TypeAdapter(list[Restaurant]).validate_python(payload)

    def get(self, restaurant_id: str) -> Restaurant | None:
        return next((r for r in self.load() if r.id == restaurant_id), None)

    def validate(self) -> tuple[bool, list[str]]:
        try:
            records = self.load()
            ids = [r.id for r in records]
            duplicates = sorted({x for x in ids if ids.count(x) > 1})
            return (not duplicates, [f"duplicate id: {x}" for x in duplicates])
        except (ValidationError, json.JSONDecodeError) as exc:
            return False, [str(exc)]

    def replace_all(self, records: Iterable[Restaurant], actor: str = "system") -> None:
        validated = TypeAdapter(list[Restaurant]).validate_python(list(records))
        ids = [r.id for r in validated]
        if len(ids) != len(set(ids)):
            raise ValueError("Restaurant IDs must be unique")
        self._atomic_write([r.model_dump(mode="json") for r in validated])
        self._audit("replace_all", actor, {"count": len(validated)})

    def upsert(self, record: Restaurant, actor: str, expected_updated_at: datetime | None = None) -> None:
        records = self.load()
        current = next((r for r in records if r.id == record.id), None)
        if expected_updated_at and current and current.updated_at != expected_updated_at:
            raise RuntimeError("Concurrent update detected; reload before writing")
        record.updated_at = datetime.now(timezone.utc)
        updated = [record if r.id == record.id else r for r in records]
        if current is None:
            updated.append(record)
        self.replace_all(updated, actor=actor)
        self._audit("upsert", actor, {"restaurant_id": record.id, "created": current is None})

    def _atomic_write(self, payload: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix="restaurants-", suffix=".json", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=False)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, self.path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    def _audit(self, action: str, actor: str, detail: dict) -> None:
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        event = {"timestamp": datetime.now(timezone.utc).isoformat(), "action": action,
                 "actor": actor, "detail": detail}
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

