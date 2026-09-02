from __future__ import annotations

from .models import Restaurant


SAMPLE_RESTAURANTS = [
    {
        "id": "saffron-table", "name": "Saffron Table",
        "description": "Contemporary Persian dining with charcoal kebabs, fragrant rice and a calm terrace.",
        "cuisines": ["Persian", "Middle Eastern"], "neighborhood": "Downtown",
        "location": {"latitude": 25.1972, "longitude": 55.2744}, "price_band": "$$$",
        "dietary": ["halal", "vegetarian", "gluten-free"], "ambience": ["romantic", "terrace", "quiet"],
        "menu": [{"name": "Saffron Chicken", "description": "Charcoal chicken, saffron rice, barberries", "price": 92,
                  "dietary": ["halal", "gluten-free"], "image_caption": "golden saffron rice with charcoal chicken"}],
        "reviews": [{"rating": 4.8, "text": "Elegant but relaxed; the saffron rice and service were excellent.",
                     "sentiment": 0.9, "aspects": {"food": 0.95, "service": 0.9}}],
    },
    {
        "id": "green-fork", "name": "Green Fork Kitchen",
        "description": "Bright plant-forward café serving seasonal bowls, vegan desserts and specialty coffee.",
        "cuisines": ["Vegan", "Healthy"], "neighborhood": "Business Bay",
        "location": {"latitude": 25.185, "longitude": 55.267}, "price_band": "$$",
        "dietary": ["vegan", "vegetarian", "dairy-free", "gluten-free"], "ambience": ["casual", "bright", "laptop-friendly"],
        "menu": [{"name": "Harvest Bowl", "description": "Quinoa, roasted squash, greens and tahini", "price": 58,
                  "dietary": ["vegan", "gluten-free"], "image_caption": "colorful quinoa bowl with roasted vegetables"}],
        "reviews": [{"rating": 4.5, "text": "Fresh bowls and clear allergen labels; busy around lunch.",
                     "sentiment": 0.75, "aspects": {"food": 0.85, "ambience": 0.55}}],
    },
    {
        "id": "marina-ember", "name": "Marina Ember",
        "description": "Waterfront steak and seafood restaurant focused on open-fire cooking and sunset views.",
        "cuisines": ["Steakhouse", "Seafood"], "neighborhood": "Dubai Marina",
        "location": {"latitude": 25.0805, "longitude": 55.1403}, "price_band": "$$$$",
        "dietary": ["halal", "gluten-free"], "ambience": ["waterfront", "luxury", "romantic"],
        "menu": [{"name": "Fire-Grilled Sea Bass", "description": "Sea bass, lemon, herbs and grilled vegetables", "price": 165,
                  "dietary": ["halal", "gluten-free"], "image_caption": "grilled sea bass with lemon beside marina view"}],
        "reviews": [{"rating": 4.7, "text": "Memorable sunset view and excellent fish, though it is expensive.",
                     "sentiment": 0.8, "aspects": {"food": 0.9, "value": 0.2}}],
    },
    {
        "id": "napoli-corner", "name": "Napoli Corner",
        "description": "Neighborhood pizzeria with wood-fired Neapolitan pies, handmade pasta and quick service.",
        "cuisines": ["Italian", "Pizza"], "neighborhood": "Jumeirah",
        "location": {"latitude": 25.221, "longitude": 55.255}, "price_band": "$$",
        "dietary": ["vegetarian"], "ambience": ["family-friendly", "casual", "lively"],
        "menu": [{"name": "Margherita", "description": "Tomato, fior di latte and basil", "price": 52,
                  "dietary": ["vegetarian"], "image_caption": "wood-fired margherita pizza with blistered crust"}],
        "reviews": [{"rating": 4.6, "text": "Proper airy crust, friendly staff and good value for families.",
                     "sentiment": 0.85, "aspects": {"food": 0.9, "value": 0.8}}],
    },
]


def records() -> list[Restaurant]:
    return [Restaurant.model_validate(item) for item in SAMPLE_RESTAURANTS]

