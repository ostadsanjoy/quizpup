import os, json
PRELOADED_DECKS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "preloaded_decks.json"), encoding="utf-8"))