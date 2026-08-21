import unittest

from src.portfolio_api.main import health


class ApiSmokeTests(unittest.TestCase):
    def test_health_exposes_governance_flags(self) -> None:
        result = health()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["product_count"], 18)
        self.assertTrue(result["synthetic_data_only"])


if __name__ == "__main__":
    unittest.main()
