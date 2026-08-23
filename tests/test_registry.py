import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProductRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(
            (ROOT / "products" / "registry.json").read_text(encoding="utf-8")
        )

    def test_expected_product_count(self) -> None:
        self.assertEqual(len(self.registry["products"]), 18)

    def test_ids_and_slugs_are_unique(self) -> None:
        products = self.registry["products"]
        self.assertEqual(len({p["id"] for p in products}), len(products))
        self.assertEqual(len({p["slug"] for p in products}), len(products))

    def test_baseline_is_synthetic_and_not_production_ready(self) -> None:
        for product in self.registry["products"]:
            self.assertEqual(product["data_policy"], "synthetic-only")
            self.assertFalse(product["production_ready"])

    def test_each_product_has_readme(self) -> None:
        for product in self.registry["products"]:
            path = ROOT / "products" / product["slug"] / "README.md"
            self.assertTrue(path.exists(), path)


if __name__ == "__main__":
    unittest.main()
