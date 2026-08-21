import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="AI Product Portfolio API",
    version="0.1.0",
    description="Registry API for governed AI products.",
)


def registry_path() -> Path:
    configured = os.getenv("PRODUCT_REGISTRY_PATH", "products/registry.json")
    return Path(configured)


def load_registry() -> dict:
    path = registry_path()
    if not path.exists():
        raise RuntimeError(f"Product registry not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "synthetic_data_only": True}


@app.get("/products")
def list_products() -> dict:
    return load_registry()


@app.get("/products/{product_id}")
def get_product(product_id: str) -> dict:
    registry = load_registry()
    normalized = product_id.upper()
    for product in registry["products"]:
        if product["id"].upper() == normalized or product["slug"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
