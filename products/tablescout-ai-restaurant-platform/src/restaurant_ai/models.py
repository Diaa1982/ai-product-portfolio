from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PriceBand(str, Enum):
    budget = "$"
    moderate = "$$"
    premium = "$$$"
    luxury = "$$$$"


class Dietary(str, Enum):
    vegetarian = "vegetarian"
    vegan = "vegan"
    halal = "halal"
    gluten_free = "gluten-free"
    dairy_free = "dairy-free"


class GeoPoint(BaseModel):
    latitude: Annotated[float, Field(ge=-90, le=90)]
    longitude: Annotated[float, Field(ge=-180, le=180)]


class MenuItem(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=600)
    price: Annotated[float, Field(ge=0)]
    dietary: list[Dietary] = Field(default_factory=list)
    image_path: str | None = None
    image_caption: str | None = Field(default=None, max_length=500)


class Review(BaseModel):
    rating: Annotated[float, Field(ge=1, le=5)]
    text: str = Field(min_length=2, max_length=4000)
    sentiment: Annotated[float, Field(ge=-1, le=1)] = 0
    aspects: dict[str, Annotated[float, Field(ge=-1, le=1)]] = Field(default_factory=dict)


class Restaurant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]{2,63}$")
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=4000)
    cuisines: list[str] = Field(min_length=1)
    neighborhood: str = Field(min_length=2, max_length=120)
    location: GeoPoint
    price_band: PriceBand
    dietary: list[Dietary] = Field(default_factory=list)
    ambience: list[str] = Field(default_factory=list)
    menu: list[MenuItem] = Field(default_factory=list)
    reviews: list[Review] = Field(default_factory=list)
    active: bool = True
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("cuisines", "ambience")
    @classmethod
    def normalize_tags(cls, values: list[str]) -> list[str]:
        cleaned = {v.strip().lower() for v in values if v.strip()}
        return sorted(cleaned)

    @property
    def average_rating(self) -> float:
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 2) if self.reviews else 0

    def searchable_text(self) -> str:
        menu = " ".join(f"{m.name} {m.description} {m.image_caption or ''}" for m in self.menu)
        reviews = " ".join(r.text for r in self.reviews)
        return " ".join([
            self.name, self.description, " ".join(self.cuisines), self.neighborhood,
            " ".join(self.ambience), " ".join(x.value for x in self.dietary), menu, reviews,
        ])


class UserPreferences(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    cuisines: list[str] = Field(default_factory=list)
    dietary: list[Dietary] = Field(default_factory=list)
    max_price_band: PriceBand | None = None
    neighborhood: str | None = None
    occasion: str | None = None
    text_weight: Annotated[float, Field(ge=0, le=1)] = 0.65
    image_weight: Annotated[float, Field(ge=0, le=1)] = 0.35

    @field_validator("image_weight")
    @classmethod
    def weights_sum_to_one(cls, value: float, info):
        text_weight = info.data.get("text_weight", 0.65)
        if abs(text_weight + value - 1.0) > 1e-6:
            raise ValueError("text_weight and image_weight must sum to 1")
        return value


class Evidence(BaseModel):
    source: str
    excerpt: str
    score: float


class Recommendation(BaseModel):
    restaurant_id: str
    restaurant_name: str
    score: Annotated[float, Field(ge=0, le=1)]
    rationale: str
    tradeoffs: list[str]
    evidence: list[Evidence]
    policy_checks: list[str]

