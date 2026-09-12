def get_content_opportunity(
    title,
    category,
    score,
    momentum,
    sources,
    cluster=None
):
    # -------------------------
    # CONTENT OPPORTUNITY
    # -------------------------

    opportunity = "MEDIUM"

    if score >= 70:
        opportunity = "HIGH"

    if score >= 90:
        opportunity = "VERY HIGH"

    # -------------------------
    # COLLECT DIFFERENT HEADLINES
    # -------------------------

    headlines = []

    if cluster:
        for story in cluster:
            story_title = story.get("title", "").strip()

            if story_title and story_title not in headlines:
                headlines.append(story_title)

    # -------------------------
    # WHAT IS HAPPENING
    # -------------------------

    if len(headlines) >= 2:
        context = (
            f"Multiple independent sources are now covering "
            f"the same developing story.\n\n"
            f"1. {headlines[0]}\n"
            f"2. {headlines[1]}"
        )
    else:
        context = title

    # -------------------------
    # WHY IT MATTERS
    # -------------------------

    if category == "Transfer":
        why = (
            "This is gaining transfer-market attention across "
            "multiple sources. Watch for confirmation, bids, "
            "agreement details or changes in the player's position."
        )

    elif category == "Injury":
        why = (
            "This could affect team selection, upcoming matches "
            "and the tactical role of whoever replaces the player."
        )

    elif category == "Manager":
        why = (
            "Manager stories can develop quickly into discussions "
            "about results, tactics, dressing-room pressure and "
            "possible replacements."
        )

    elif category == "Match Incident":
        why = (
            "This has immediate debate potential because the incident "
            "may have affected the direction or result of the match."
        )

    else:
        why = (
            "Independent football sources are covering the same "
            "development, suggesting the story is gaining attention."
        )

    # -------------------------
    # CONTENT ANGLES
    # -------------------------

    if category == "Transfer":
        angles = [
            "REACTION — Does this transfer actually make football sense?",
            "TACTICAL FIT — Where would the player fit and whose place is under threat?",
            "CLUB IMPACT — Who benefits most if the deal happens?"
        ]

    elif category == "Injury":
        angles = [
            "REPLACEMENT — Who should take the player's place?",
            "TACTICAL — What changes without this player?",
            "MATCH IMPACT — Which upcoming fixture is affected most?"
        ]

    elif category == "Manager":
        angles = [
            "TACTICAL — What football problem is actually hurting the manager?",
            "DECISION — Would sacking the manager genuinely fix the problem?",
            "REPLACEMENT — Who realistically fits the squad?"
        ]

    elif category == "Match Incident":
        angles = [
            "VERDICT — Was the decision actually correct?",
            "IMPACT — How did the incident change the match?",
            "DEBATE — Take a clear side on the argument fans are having."
        ]

    else:
        angles = [
            "REACTION — Give a clear football opinion instead of repeating the news.",
            "CONTEXT — Explain why this development actually matters.",
            "MISSED ANGLE — Find the part of the story most accounts are overlooking."
        ]

    # -------------------------
    # BARCELONA PRIORITY
    # -------------------------

    combined_text = " ".join(headlines).lower() + " " + title.lower()

    if any(
        word in combined_text
        for word in ["barcelona", "barca", "fcb"]
    ):
        angles.insert(
            0,
            "BARCA ANGLE — What does this specifically mean for Barcelona?"
        )

    # -------------------------
    # VERIFICATION
    # -------------------------

    source_count = len(set(sources))

    if source_count >= 3:
        verification = "STRONG MULTI-SOURCE SIGNAL"
    elif source_count >= 2:
        verification = "MULTI-SOURCE SIGNAL"
    else:
        verification = "VERIFY BEFORE POSTING"

    return {
        "opportunity": opportunity,
        "context": context,
        "why": why,
        "angles": angles[:3],
        "verification": verification
    }
