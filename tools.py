"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re
import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.
    """
    listings = load_listings()
    query_words = set(description.lower().split())
    if not query_words:
        return []

    scored = []
    for item in listings:
        if max_price is not None and item.get("price", 0) > max_price:
            continue
        
        if size is not None:
            item_size = str(item.get("size", "")).lower()
            sizes = [s.strip() for s in item_size.replace("/", " ").split()]
            if size.lower() not in sizes:
                continue

        text = f"{item.get('title', '')} {item.get('description', '')} {item.get('category', '')}".lower()
        score = sum(1 for w in query_words if w in text)
        
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    limit = getattr(config, "SEARCH_RESULT_LIMIT", 10)
    return [item for _, item in scored[:limit]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    """
    items = wardrobe.get("items", [])
    if not items:
        prompt = (
            f"Give general styling advice and outfit ideas for this item: "
            f"{new_item.get('title', 'Item')} ({new_item.get('description', '')}). "
            f"Category: {new_item.get('category', 'unknown')}."
        )
    else:
        wardrobe_list = "\n".join(
            f"- {item.get('title', 'Item')} ({item.get('category', 'unknown')})" 
            for item in items
        )
        prompt = (
            f"Suggest one or two outfits combining this new thrifted item "
            f"({new_item.get('title', 'Item')} - {new_item.get('description', '')}) "
            f"with these pieces the user already owns:\n{wardrobe_list}"
        )
        
    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.
    """
    if not outfit or not outfit.strip():
        return "Outfit details are needed to generate a fit card."

    title = new_item.get("title", "thrift find")
    price = new_item.get("price", "a great price")
    platform = new_item.get("platform", "online")

    prompt = (
        f"Write a short social media caption (2 to 4 sentences) for this thrift find. "
        f"Item: {title}, Price: ${price}, Platform: {platform}. "
        f"Outfit context: {outfit}. "
        "Make it sound like a real person posting about their find, mention the price and platform once each, and capture a specific vibe."
    )

    return generate(prompt)