from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .embeddings import LocalMultimodalEmbedder
from .models import PriceBand, Restaurant, UserPreferences


PRICE_ORDER = {PriceBand.budget: 1, PriceBand.moderate: 2, PriceBand.premium: 3, PriceBand.luxury: 4}


@dataclass
class SearchHit:
    restaurant: Restaurant
    text_score: float
    image_score: float
    fused_score: float


class MultimodalRetriever:
    def __init__(self, records: list[Restaurant], embedder: LocalMultimodalEmbedder | None = None):
        self.records = records
        self.embedder = embedder or LocalMultimodalEmbedder()
        self.text_vectors = {r.id: self.embedder.text(r.searchable_text()) for r in records}

    def search(self, prefs: UserPreferences, image_path: str | None = None, top_k: int = 5) -> list[SearchHit]:
        candidates = [r for r in self.records if self._passes_filters(r, prefs)]
        query_vector = self.embedder.text(prefs.query)
        image_query = self.embedder.image(image_path) if image_path else None
        hits: list[SearchHit] = []
        for restaurant in candidates:
            text_score = (self.embedder.cosine(query_vector, self.text_vectors[restaurant.id]) + 1) / 2
            image_score = self._best_image_score(restaurant, image_query) if image_query is not None else 0.5
            fused = prefs.text_weight * text_score + prefs.image_weight * image_score
            rating_bonus = min(restaurant.average_rating / 5, 1) * 0.08
            fused = min(1.0, fused * 0.92 + rating_bonus)
            hits.append(SearchHit(restaurant, text_score, image_score, fused))
        return sorted(hits, key=lambda h: (-h.fused_score, h.restaurant.name))[:top_k]

    def _best_image_score(self, restaurant: Restaurant, query: np.ndarray) -> float:
        paths = [m.image_path for m in restaurant.menu if m.image_path and Path(m.image_path).exists()]
        if not paths:
            # Do not compare vectors from incompatible modality spaces. Missing menu imagery is neutral.
            return 0.5
        return max((self.embedder.cosine(query, self.embedder.image(path)) + 1) / 2 for path in paths)

    @staticmethod
    def _passes_filters(record: Restaurant, prefs: UserPreferences) -> bool:
        if not record.active:
            return False
        if prefs.max_price_band and PRICE_ORDER[record.price_band] > PRICE_ORDER[prefs.max_price_band]:
            return False
        if prefs.neighborhood and prefs.neighborhood.lower() not in record.neighborhood.lower():
            return False
        if prefs.dietary and not set(prefs.dietary).issubset(set(record.dietary)):
            return False
        if prefs.cuisines and not {x.lower() for x in prefs.cuisines}.intersection(record.cuisines):
            return False
        return True
