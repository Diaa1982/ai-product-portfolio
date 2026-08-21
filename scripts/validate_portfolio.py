import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "products" / "registry.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    products = data.get("products", [])
    if not products:
        fail("product registry is empty")

    ids = [item["id"] for item in products]
    slugs = [item["slug"] for item in products]
    if len(ids) != len(set(ids)):
        fail("duplicate product IDs")
    if len(slugs) != len(set(slugs)):
        fail("duplicate product slugs")

    required = {
        "id",
        "slug",
        "name",
        "maturity",
        "classification",
        "data_policy",
        "production_ready",
    }
    for product in products:
        missing = required - set(product)
        if missing:
            fail(f"{product.get('id', 'UNKNOWN')} missing fields: {sorted(missing)}")
        readme = ROOT / "products" / product["slug"] / "README.md"
        if not readme.exists():
            fail(f"missing product README: {readme.relative_to(ROOT)}")
        if product["data_policy"] != "synthetic-only":
            fail(f"{product['id']} violates baseline synthetic-only policy")
        if product["production_ready"] is not False:
            fail(f"{product['id']} must not be marked production-ready in baseline")

    print(f"Validated {len(products)} product packages.")


if __name__ == "__main__":
    main()
