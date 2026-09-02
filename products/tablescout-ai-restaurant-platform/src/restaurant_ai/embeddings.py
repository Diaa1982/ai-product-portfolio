from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image


class LocalMultimodalEmbedder:
    """Dependency-light demo embeddings. Replace with production embedding models behind this API."""

    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    def text(self, value: str) -> np.ndarray:
        vector = np.zeros(self.dimensions, dtype=np.float32)
        tokens = re.findall(r"[\w'-]+", value.lower())
        for token in tokens:
            digest = hashlib.blake2b(token.encode(), digest_size=8).digest()
            index = int.from_bytes(digest[:4], "little") % self.dimensions
            sign = 1 if digest[4] % 2 else -1
            vector[index] += sign * (1 + math.log1p(len(token)))
        return self._normalize(vector)

    def image(self, path: str | Path) -> np.ndarray:
        image = Image.open(path).convert("RGB").resize((32, 32))
        pixels = np.asarray(image, dtype=np.float32) / 255.0
        features: list[float] = []
        for channel in range(3):
            hist, _ = np.histogram(pixels[:, :, channel], bins=32, range=(0, 1), density=True)
            features.extend(hist.tolist())
            features.extend([pixels[:, :, channel].mean(), pixels[:, :, channel].std()])
        vector = np.zeros(self.dimensions, dtype=np.float32)
        vector[: min(len(features), self.dimensions)] = features[: self.dimensions]
        return self._normalize(vector)

    @staticmethod
    def cosine(left: np.ndarray, right: np.ndarray) -> float:
        if not left.any() or not right.any():
            return 0.0
        return float(np.clip(np.dot(left, right), -1, 1))

    @staticmethod
    def _normalize(vector: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vector)
        return vector / norm if norm else vector

