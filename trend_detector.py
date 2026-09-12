BREAKING_WORDS = {
    "breaking",
    "exclusive",
    "agrees",
    "agreed",
    "sign",
    "signs",
    "signed",
    "transfer",
    "deal",
    "bid",
    "injury",
    "injured",
    "sacked",
    "red card",
    "suspended",
    "confirmed",
    "official"
}


def calculate_cluster_score(cluster):
    score = 10

    unique_sources = {
        story["source"]
        for story in cluster
    }

    source_count = len(unique_sources)

    # Independent sources matter most
    if source_count >= 2:
        score += 30

    if source_count >= 3:
        score += 25

    if source_count >= 4:
        score += 20

    # Fast-moving sources
    if any(story["type"] == "fast" for story in cluster):
        score += 10

    # Lots of articles about the same story
    if len(cluster) >= 3:
        score += 10

    combined_text = " ".join(
        story["title"].lower()
        for story in cluster
    )

    if any(word in combined_text for word in BREAKING_WORDS):
        score += 10

    return score