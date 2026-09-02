import json
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from restaurant_ai.agents import RecommendationCrew
from restaurant_ai.models import Dietary, Restaurant, UserPreferences
from restaurant_ai.retrieval import MultimodalRetriever
from restaurant_ai.sample_data import records
from restaurant_ai.store import KnowledgeBase


class PlatformTests(unittest.TestCase):
    def test_sample_data_validates_and_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb = KnowledgeBase(Path(tmp) / "restaurants.json", Path(tmp) / "audit.jsonl")
            kb.replace_all(records(), actor="test")
            ok, errors = kb.validate()
            self.assertTrue(ok, errors)
            self.assertEqual(len(kb.load()), 4)

    def test_hard_filter_excludes_non_vegan(self):
        prefs = UserPreferences(query="fresh lunch", dietary=[Dietary.vegan])
        hits = MultimodalRetriever(records()).search(prefs)
        self.assertEqual([h.restaurant.id for h in hits], ["green-fork"])

    def test_crew_returns_grounded_output_and_trace(self):
        prefs = UserPreferences(query="romantic halal dinner")
        recs, trace = RecommendationCrew(MultimodalRetriever(records())).recommend(prefs)
        self.assertTrue(recs)
        self.assertEqual(len(trace), 3)
        self.assertTrue(recs[0].evidence)

    def test_weights_must_sum_to_one(self):
        with self.assertRaises(ValidationError):
            UserPreferences(query="pizza", text_weight=0.9, image_weight=0.9)

    def test_rejects_extra_fields(self):
        payload = records()[0].model_dump(mode="json") | {"secret": "ignore me"}
        with self.assertRaises(ValidationError):
            Restaurant.model_validate(payload)


if __name__ == "__main__":
    unittest.main()

