import json
import os

MEMORY_FILE = "live_memory.json"


def load_live_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_live_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2, ensure_ascii=False)


def detect_live_changes(matches):
    old_memory = load_live_memory()

    new_memory = {}
    changes = []

    for match in matches:
        key = match["link"] or match["title"]

        current_state = (
            match["title"]
            + " | "
            + match["description"]
        )

        new_memory[key] = current_state

        if key not in old_memory:
            continue

        if old_memory[key] != current_state:
            changes.append(match)

    save_live_memory(new_memory)

    return changes