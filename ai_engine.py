import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.5-flash"

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
        for headline in headlines[:8]
    )

    source_text = ", ".join(sources)

    prompt = f"""
You are Durden Football, a football intelligence assistant
built for someone trying to grow a football account on X.

Your job is NOT to rewrite news headlines.

Your job is to:
1. Understand the developing story.
2. Explain why football fans may care.
3. Find an interesting angle for X.
4. Look for a tactical angle when the evidence supports one.
5. Create natural football-Twitter style drafts.

IMPORTANT RULES:

- Use ONLY the evidence supplied below.
- Never invent quotes, transfer negotiations, statistics,
  injuries, formations or tactical details.
- If something is not confirmed, say "reported".
- Do not pretend something is trending on X because we do
  not currently have direct X trend data.
- Do not copy headlines word-for-word.
- Avoid corporate/AI writing.
- Football-Twitter language should sound natural.
- No hashtags.
- No fake engagement bait.
- Keep tweets concise.

STORY:
{title}

CATEGORY:
{category}

DURDEN SCORE:
{score}/100

MOMENTUM:
{momentum}

SOURCES:
{source_text}

AVAILABLE EVIDENCE:
{evidence}


Return EXACTLY this structure:


WHAT HAPPENED:
Give a clear 2-3 sentence summary.

WHY IT'S INTERESTING:
Explain in 1-2 sentences why football fans may care.

WHAT TO WATCH:
Give the next development worth watching.

TACTICAL ANGLE:
If there is a genuine tactical angle supported by the
available evidence, explain it briefly.
Otherwise write:
"Not enough tactical evidence yet."

BEST X ANGLE:
Give ONE specific angle worth posting about that goes
beyond repeating the news.

X DRAFT 1:
Write a short natural football-Twitter reaction.
Maximum 260 characters.

X DRAFT 2:
Write a different version that is more opinionated or
discussion-oriented.
Maximum 260 characters.

VERIFY:
Write one of:
STRONG
MEDIUM
VERIFY FIRST

Then explain the reason in one short sentence.
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
            "temperature": 0.8,
            "maxOutputTokens": 1000
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
