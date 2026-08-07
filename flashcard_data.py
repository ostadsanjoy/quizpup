import os
import json

_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "preloaded_decks.json")

with open(_JSON_PATH, "r", encoding="utf-8") as f:
    PRELOADED_DECKS = json.load(f)