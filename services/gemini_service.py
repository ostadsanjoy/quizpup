import os
import time
import threading
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_GEMINI_API_KEY_HERE")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_LITE = 'gemini-3.1-flash-lite'
MODEL_HEAVY = 'gemini-2.5-flash'
HEAVY_TEXT_CHAR_THRESHOLD = 15000
GEMINI_RPM_TARGET = 10

_gemini_window_lock = threading.Lock()
_gemini_window_start = [time.monotonic()]
_gemini_window_count = [0]


def pick_model(is_hardest=False, char_count=0):
    if is_hardest:
        return MODEL_HEAVY
    if char_count and char_count > HEAVY_TEXT_CHAR_THRESHOLD:
        return MODEL_HEAVY
    return MODEL_LITE


def _wait_for_rate_slot():
    while True:
        with _gemini_window_lock:
            now = time.monotonic()
            elapsed = now - _gemini_window_start[0]
            if elapsed >= 60:
                _gemini_window_start[0] = now
                _gemini_window_count[0] = 0
                elapsed = 0
            if _gemini_window_count[0] < GEMINI_RPM_TARGET:
                _gemini_window_count[0] += 1
                return
            sleep_time = 60 - elapsed
        time.sleep(sleep_time)


def call_gemini(**kwargs):
    last_error = None
    for attempt in range(3):
        _wait_for_rate_slot()
        try:
            return ai_client.models.generate_content(**kwargs)
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                last_error = e
                time.sleep(15 * (attempt + 1))
                continue
            raise
    raise last_error