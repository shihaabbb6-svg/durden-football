import feedparser


LIVE_FEED = "https://gioscore.com/rss/live.xml"


def collect_live_matches():
    feed = feedparser.parse(LIVE_FEED)

    matches = []

    for entry in feed.entries:
        matches.append({
            "title": entry.get("title", ""),
            "description": entry.get("description", ""),
            "link": entry.get("link", "")
        })

    return matches