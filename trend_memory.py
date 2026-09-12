import json
import os
import time

MEMORY_FILE = "trend_memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2)


def story_key(title):
    return title.lower().strip()


def should_alert(title, score):
    memory = load_memory()
    key = story_key(title)

    if key not in memory:
        return True

    previous_score = memory[key]["score"]

    # Alert again only if story becomes much stronger
    if score >= previous_score + 20:
        return True

    return False


def remember_alert(title, score):
    memory = load_memory()

    memory[story_key(title)] = {
        "score": score,
        "time": int(time.time())
    }

    save_memory(memory)