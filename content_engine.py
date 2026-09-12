def get_content_opportunity(title, category, score, momentum, sources):

    text = title.lower()

    opportunity = "MEDIUM"

    if score >= 70:
        opportunity = "HIGH"

    if score >= 90:
        opportunity = "VERY HIGH"

    angles = []

    # TRANSFERS
    if category == "Transfer":
        angles = [
            "What does this move actually mean for the clubs involved?",
            "Is the reported transfer worth the money?",
            "Who benefits most if this deal happens?"
        ]

    # INJURIES
    elif category == "Injury":
        angles = [
            "How does this injury change the team's next match?",
            "Who replaces the injured player?",
            "How does the tactical setup change without him?"
        ]

    # MANAGERS
    elif category == "Manager":
        angles = [
            "Why is the manager under pressure?",
            "What tactical problem is causing the situation?",
            "Who could realistically replace him?"
        ]

    # MATCH INCIDENT
    elif category == "Match Incident":
        angles = [
            "Was the decision actually correct?",
            "How did the incident change the match?",
            "What are fans likely to debate about this?"
        ]

    # GENERAL FOOTBALL
    else:
        angles = [
            "Why does this story actually matter?",
            "What is the strongest football argument around this?",
            "What angle are most people missing?"
        ]

    # Barcelona relevance
    barca_words = [
        "barcelona",
        "barca",
        "fcb"
    ]

    if any(word in text for word in barca_words):
        angles.insert(
            0,
            "What does this mean specifically for Barcelona?"
        )

    return {
        "opportunity": opportunity,
        "angles": angles[:3]
    }
