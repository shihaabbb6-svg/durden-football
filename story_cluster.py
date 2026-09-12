import re


IGNORE_WORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on",
    "for", "with", "as", "at", "is", "are", "was", "were",
    "be", "been", "from", "about", "after", "before", "this",
    "that", "could", "would", "should", "has", "have", "had",
    "says", "say", "report", "reports", "latest"
}


def normalize(text):
    text = text.lower()

    replacements = {
        "man utd": "manchester united",
        "man united": "manchester united",
        "man city": "manchester city",
        "barca": "barcelona",
        "atleti": "atletico madrid",
        "spurs": "tottenham"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def get_words(title):
    title = normalize(title)

    words = re.findall(r"[a-z0-9£€$]+", title)

    return {
        word
        for word in words
        if word not in IGNORE_WORDS
        and len(word) > 2
    }


def similarity_score(title1, title2):
    words1 = get_words(title1)
    words2 = get_words(title2)

    if not words1 or not words2:
        return 0

    common = words1.intersection(words2)
    union = words1.union(words2)

    if not union:
        return 0

    jaccard = len(common) / len(union)

    smaller = min(
        len(words1),
        len(words2)
    )

    overlap = len(common) / smaller

    return max(jaccard, overlap)


def same_story(title1, title2):
    words1 = get_words(title1)
    words2 = get_words(title2)

    common = words1.intersection(words2)

    score = similarity_score(
        title1,
        title2
    )

    if len(common) >= 3 and score >= 0.45:
        return True

    if len(common) >= 2 and score >= 0.70:
        return True

    return False


def cluster_stories(stories):
    clusters = []

    for story in stories:
        best_cluster = None
        best_score = 0

        for cluster in clusters:
            for existing_story in cluster:

                score = similarity_score(
                    story["title"],
                    existing_story["title"]
                )

                if (
                    same_story(
                        story["title"],
                        existing_story["title"]
                    )
                    and score > best_score
                ):
                    best_score = score
                    best_cluster = cluster

        if best_cluster is not None:
            best_cluster.append(story)
        else:
            clusters.append([story])

    return clusters
