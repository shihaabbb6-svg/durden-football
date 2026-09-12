import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    f"v1beta/models/{GEMINI_MODEL}:generateContent"
)


def generate_ai_content(
    title,
    category,
    score,
    momentum,
    sources,
    cluster
):
    if not GEMINI_API_KEY:
        return None

    headlines = []

    for story in cluster:
        headline = story.get("title", "").strip()

        if headline and headline not in headlines:
            headlines.append(headline)

    evidence = "\n".join(
        f"- {headline}"
        for headline in headlines[:6]
    )

    source_text = ", ".join(sources)

    prompt = f"""
You are the football intelligence and X content assistant
for Durden Football.

Analyse ONLY the information supplied below.

Do not invent transfers, quotes, statistics, injuries,
tactical details or confirmations.

If something is only reported, describe it as reported.

STORY:
{title}

CATEGORY:
{category}

TREND SCORE:
{score}

MOMENTUM:
{momentum}

SOURCES:
{source_text}

HEADLINES:
{evidence}

Return exactly this structure:

WHAT HAPPENED:
2-3 short sentences explaining the development.

WHY IT MATTERS:
2-3 short sentences explaining why football fans may care.

BEST ANGLE:
One interesting angle that goes beyond simply repeating
the headline. Do not invent facts.

X DRAFT:
Write one short natural football-Twitter post.
It should sound human, opinion-friendly and conversational.
Do not make it sound like a news bot.
Do not use hashtags.
Do not copy the headline word-for-word.
Do not invent information.
Keep it under 260 characters.

VERIFY:
Say either STRONG, MEDIUM or VERIFY FIRST, followed by
one short reason.
"""

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 700
        }
    }

    try:
        response = requests.post(
            GEMINI_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return (
            data["candidates"][0]
            ["content"]["parts"][0]["text"]
            .strip()
        )

    except Exception as error:
        print("Gemini error:", error)
        return None
