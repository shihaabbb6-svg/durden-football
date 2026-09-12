import requests


STATSBOMB_BASE = (
    "https://raw.githubusercontent.com/"
    "hudl/open-data/master/data"
)


def get_competitions():
    url = f"{STATSBOMB_BASE}/competitions.json"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        return response.json()

    except Exception as error:
        print("StatsBomb competitions error:", error)
        return []


def get_matches(competition_id, season_id):
    url = (
        f"{STATSBOMB_BASE}/matches/"
        f"{competition_id}/{season_id}.json"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        return response.json()

    except Exception as error:
        print("StatsBomb matches error:", error)
        return []


def get_events(match_id):
    url = (
        f"{STATSBOMB_BASE}/events/"
        f"{match_id}.json"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        return response.json()

    except Exception as error:
        print("StatsBomb events error:", error)
        return []


def analyse_match_events(events):
    analysis = {
        "passes": {},
        "shots": {},
        "goals": {},
        "pressures": {},
        "carries": {}
    }

    for event in events:

        team = (
            event.get("team", {})
            .get("name", "Unknown")
        )

        event_type = (
            event.get("type", {})
            .get("name", "")
        )

        if team not in analysis["passes"]:
            analysis["passes"][team] = 0
            analysis["shots"][team] = 0
            analysis["goals"][team] = 0
            analysis["pressures"][team] = 0
            analysis["carries"][team] = 0

        if event_type == "Pass":
            analysis["passes"][team] += 1

        elif event_type == "Shot":
            analysis["shots"][team] += 1

            outcome = (
                event.get("shot", {})
                .get("outcome", {})
                .get("name", "")
            )

            if outcome == "Goal":
                analysis["goals"][team] += 1

        elif event_type == "Pressure":
            analysis["pressures"][team] += 1

        elif event_type == "Carry":
            analysis["carries"][team] += 1

    return analysis
