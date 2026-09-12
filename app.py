import os
import requests

from collector import (
    collect_bbc,
    collect_football365,
    collect_caughtoffside,
    collect_news_trends
)

from content_engine import get_content_opportunity
from ai_engine import generate_ai_content
from live_collector import collect_live_matches
from live_memory import detect_live_changes

from trend_detector import calculate_cluster_score
from story_cluster import cluster_stories, same_story

from trend_memory import (
    should_alert,
    remember_alert
)


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "816355804"


def send_telegram_message(message):
    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(
            url,
            data=data,
            timeout=10
        )

        return response

    except Exception as error:
        print("Telegram error:", error)
        return None


print("\nDURDEN FOOTBALL V3")
print("==================")
print("\nCollecting football intelligence...")


# =========================
# COLLECT
# =========================

stories = (
    collect_bbc()
    + collect_football365()
    + collect_caughtoffside()
)

news_trends = collect_news_trends()

print(f"Stories collected: {len(stories)}")
print(f"Momentum stories: {len(news_trends)}")


# =========================
# CLUSTER
# =========================

clusters = cluster_stories(stories)

print(f"Story clusters: {len(clusters)}")
print("\nDURDEN TREND ANALYSIS:\n")

alerts = []


# =========================
# ANALYSE
# =========================

for cluster in clusters:

    score = calculate_cluster_score(cluster)

    sources = sorted({
        story["source"]
        for story in cluster
    })

    source_count = len(sources)
    trend_publishers = 0

    # -------------------------
    # NEWS MOMENTUM
    # -------------------------

    for trend in news_trends:

        if same_story(
            cluster[0]["title"],
            trend["title"]
        ):
            trend_publishers = max(
                trend_publishers,
                trend.get("publishers", 0)
            )

    if trend_publishers >= 2:
        score += 15

    if trend_publishers >= 5:
        score += 15

    # -------------------------
    # MOMENTUM
    # -------------------------

    momentum = "Normal"

    if trend_publishers >= 2:
        momentum = "Rising"

    if trend_publishers >= 5:
        momentum = "High"

    # -------------------------
    # CONFIDENCE
    # -------------------------

    confidence = "LOW"

    if source_count >= 2:
        confidence = "MEDIUM"

    if source_count >= 3:
        confidence = "HIGH"

    title = cluster[0]["title"]

    print(
        f"[{score}] "
        f"[{source_count} sources] "
        f"[{momentum}] "
        f"{title}"
    )

    # -------------------------
    # ALERT FILTER
    # -------------------------

    if score < 50:
        continue

    if source_count < 2:
        continue

    if not should_alert(title, score):
        continue

    # -------------------------
    # CLASSIFY
    # -------------------------

    text = " ".join(
        story["title"].lower()
        for story in cluster
    )

    category = "Football News"

    if any(word in text for word in [
        "transfer",
        "sign",
        "signs",
        "signed",
        "deal",
        "bid",
        "contract",
        "agreement"
    ]):
        category = "Transfer"

    if any(word in text for word in [
        "injury",
        "injured",
        "ruled out"
    ]):
        category = "Injury"

    if any(word in text for word in [
        "red card",
        "sent off",
        "suspended"
    ]):
        category = "Match Incident"

    if any(word in text for word in [
        "sacked",
        "manager",
        "coach"
    ]):
        category = "Manager"

    # -------------------------
    # CONTENT INTELLIGENCE
    # -------------------------

    content = get_content_opportunity(
        title,
        category,
        score,
        momentum,
        sources,
        cluster
    )
        # -------------------------
    # GEMINI AI ANALYSIS
    # -------------------------

    ai_content = generate_ai_content(
        title,
        category,
        score,
        momentum,
        sources,
        cluster
    )

    angles_text = "\n".join(
        f"• {angle}"
        for angle in content["angles"]
    )

    # -------------------------
    # BUILD USEFUL ALERT
    # -------------------------

      # -------------------------
    # BUILD USEFUL ALERT
    # -------------------------

    if ai_content:
        alert = (
            f"🚨 TREND: {score}/100 | {momentum.upper()}\n\n"
            f"{title}\n\n"
            f"🤖 DURDEN AI INTELLIGENCE\n\n"
            f"{ai_content}\n\n"
            f"🔎 SIGNAL DATA\n"
            f"Category: {category}\n"
            f"Confidence: {confidence}\n"
            f"Independent Sources: {source_count}\n"
            f"Sources: {', '.join(sources)}\n"
            f"Publishers Tracking: {trend_publishers}"
        )

    else:
        # Fallback if Gemini is unavailable
        alert = (
            f"🚨 TREND: {score}/100 | {momentum.upper()}\n\n"
            f"{title}\n\n"
            f"📌 WHAT'S HAPPENING\n"
            f"{content['context']}\n\n"
            f"⚽ WHY IT MATTERS\n"
            f"{content['why']}\n\n"
            f"📈 CONTENT OPPORTUNITY: "
            f"{content['opportunity']}\n\n"
            f"💡 POST ANGLES\n"
            f"{angles_text}\n\n"
            f"🔎 {content['verification']}\n"
            f"Sources: {', '.join(sources)}"
        )
    alerts.append({
        "message": alert,
        "title": title,
        "score": score
    })


# =========================
# STRONGEST FIRST
# =========================

alerts.sort(
    key=lambda item: item["score"],
    reverse=True
)


# =========================
# TELEGRAM TREND RADAR
# =========================

if alerts:

    selected_alerts = alerts[:5]

    telegram_message = (
        "🚨 DURDEN FOOTBALL INTELLIGENCE\n\n"
        + "\n\n────────────\n\n".join(
            alert["message"]
            for alert in selected_alerts
        )
    )

    response = send_telegram_message(
        telegram_message
    )

    if response and response.ok:

        print(
            f"\nSent {len(selected_alerts)} "
            f"trend(s) to Telegram."
        )

        for alert in selected_alerts:
            remember_alert(
                alert["title"],
                alert["score"]
            )

    else:
        print("\nTelegram delivery failed.")

else:
    print(
        "\nNo new strong trends worth alerting."
    )


# =========================
# LIVE MATCH RADAR
# =========================

print("\nChecking live matches...")

live_matches = collect_live_matches()

print(
    f"Live matches found: {len(live_matches)}"
)

live_changes = detect_live_changes(
    live_matches
)

if live_changes:

    live_alerts = []

    for match in live_changes[:10]:

        live_alert = (
            f"⚡ LIVE MATCH UPDATE\n\n"
            f"{match['title']}"
        )

        if match["description"]:
            live_alert += (
                f"\n\n{match['description']}"
            )

        live_alerts.append(live_alert)

    live_message = (
        "🔴 DURDEN LIVE RADAR\n\n"
        + "\n\n────────────\n\n".join(
            live_alerts
        )
    )

    response = send_telegram_message(
        live_message
    )

    if response and response.ok:
        print(
            f"Sent {len(live_alerts)} "
            f"live update(s)."
        )
    else:
        print(
            "Live Telegram delivery failed."
        )

else:
    print(
        "No new live match changes."
    )


print("\nDurden scan complete.")
