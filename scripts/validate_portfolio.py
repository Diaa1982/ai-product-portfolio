import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "products" / "registry.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    products = data.get("products", [])
    if len(products) != 18:
        fail(f"expected 18 products, found {len(products)}")

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
        "category",
        "documents",
        "readiness",
    }
    categories = set()
    for product in products:
        missing = required - set(product)
        if missing:
            fail(f"{product.get('id', 'UNKNOWN')} missing fields: {sorted(missing)}")

        readme = ROOT / product["documents"]["product_readme"]
        checklist = ROOT / product["documents"]["go_live_checklist"]
        group = ROOT / "groups" / product["category"]["slug"] / "README.md"
        for path in (readme, checklist, group):
            if not path.exists():
                fail(f"missing linked document: {path.relative_to(ROOT)}")

        categories.add(product["category"]["slug"])
        if product["data_policy"] != "synthetic-only":
            fail(f"{product['id']} violates baseline synthetic-only policy")
        if product["production_ready"] is not False:
            fail(f"{product['id']} must not be marked production-ready in baseline")
        if product["readiness"]["go_live_ready"] is not False:
            fail(f"{product['id']} must not be marked go-live ready")

    if len(categories) != 5:
        fail(f"expected 5 portfolio categories, found {len(categories)}")

    print(f"Validated {len(products)} product packages across {len(categories)} categories.")


if __name__ == "__main__":
    main()
