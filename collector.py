import requests
import feedparser


def collect_bbc():
    stories = []

    feed = feedparser.parse(
        "https://feeds.bbci.co.uk/sport/football/rss.xml"
    )

    for story in feed.entries[:20]:
        stories.append({
            "title": story.title,
            "source": "BBC",
            "type": "news"
        })

    return stories


def collect_football365():
    stories = []

    url = (
        "https://freenewsapi.ai/v1/search"
        "?host=www.football365.com"
        "&size=20"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        for article in data.get("results", []):
            stories.append({
                "title": article["title"],
                "source": "Football365",
                "type": "fast"
            })

    except Exception as error:
        print("Football365 error:", error)

    return stories


def collect_caughtoffside():
    stories = []

    feed = feedparser.parse(
        "https://www.caughtoffside.com/feed/"
    )

    for story in feed.entries[:20]:
        stories.append({
            "title": story.title,
            "source": "CaughtOffside",
            "type": "fast"
        })

    return stories


def collect_news_trends():
    stories = []

    url = (
        "https://freenewsapi.ai/v1/trends"
        "?category=sport"
        "&window=3h"
        "&min_publishers=2"
        "&sort=newest"
        "&size=30"
        "&headlines=2"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        for trend in data.get("results", []):
            stories.append({
                "title": trend.get("title", "Unknown story"),
                "source": "TrendEngine",
                "type": "trend",
                "publishers": trend.get("publishers", 0),
                "articles": trend.get("articles", 0)
            })

    except Exception as error:
        print("Trend Engine error:", error)

    return stories