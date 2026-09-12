BREAKING_WORDS = {
    "breaking",
    "exclusive",
    "confirmed",
    "official",
    "agreed",
    "agreement",
    "sign",
    "signs",
    "signed",
    "transfer",
    "deal",
    "bid",
    "offer",
    "injury",
    "injured",
    "sacked",
    "dismissed",
    "red card",
    "suspended"
}


HIGH_INTEREST_WORDS = {
    "barcelona",
    "barca",
    "real madrid",
    "arsenal",
    "chelsea",
    "liverpool",
    "manchester united",
    "man utd",
    "manchester city",
    "bayern",
    "psg",
    "atletico",
    "tottenham"
}


DEBATE_WORDS = {
    "controversy",
    "controversial",
    "VAR",
    "penalty",
    "red card",
    "reaction",
    "criticism",
    "criticised",
    "slams",
    "furious",
    "booed",
    "boos",
    "referee"
}


def calculate_cluster_score(cluster):

    score = 10

    if not cluster:
        return score

    # --------------------------------
    # SOURCE STRENGTH
    # --------------------------------

    unique_sources = {
        story.get("source", "Unknown")
        for story in cluster
    }

    source_count = len(unique_sources)

    if source_count >= 2:
        score += 30

    if source_count >= 3:
        score += 20

    if source_count >= 4:
        score += 15

    # --------------------------------
    # NUMBER OF REPORTS
    # --------------------------------

    if len(cluster) >= 3:
        score += 10

    if len(cluster) >= 5:
        score += 10

    # --------------------------------
    # FAST SOURCE
    # --------------------------------

    if any(
        story.get("type") == "fast"
        for story in cluster
    ):
        score += 10

    # --------------------------------
    # COMBINE STORY TEXT
    # --------------------------------

    combined_text = " ".join(
        story.get("title", "").lower()
        for story in cluster
    )

    # --------------------------------
    # BREAKING / DEVELOPING STORY
    # --------------------------------

    if any(
        word.lower() in combined_text
        for word in BREAKING_WORDS
    ):
        score += 10

    # --------------------------------
    # HIGH-INTEREST CLUBS
    # --------------------------------

    if any(
        club in combined_text
        for club in HIGH_INTEREST_WORDS
    ):
        score += 5

    # --------------------------------
    # FAN DEBATE / VIRAL POTENTIAL
    # --------------------------------

    if any(
        word.lower() in combined_text
        for word in DEBATE_WORDS
    ):
        score += 10

    # --------------------------------
    # NEWS MOMENTUM SIGNAL
    # --------------------------------

    publishers = max(
        (
            story.get("publishers", 0)
            for story in cluster
        ),
        default=0
    )

    if publishers >= 2:
        score += 10

    if publishers >= 5:
        score += 10

    # Never show impossible scores like 125/100
    return min(score, 100)
