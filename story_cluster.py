import re


IGNORE_WORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on",
    "for", "with", "as", "at", "is", "are", "was", "were",
    "be", "been", "from", "about", "after", "before", "this",
    "that", "could", "would", "should", "has", "have", "had"
}


def get_words(title):
    title = title.lower()

    words = re.findall(r"[a-z0-9£€$]+", title)

    return {
        word
        for word in words
        if word not in IGNORE_WORDS and len(word) > 2
    }


def same_story(title1, title2):
    words1 = get_words(title1)
    words2 = get_words(title2)

    if not words1 or not words2:
        return False

    common = words1.intersection(words2)

    smaller_title = min(len(words1), len(words2))

    similarity = len(common) / smaller_title

    if len(common) >= 3 and similarity >= 0.40:
        return True

    return False


def cluster_stories(stories):
    clusters = []

    for story in stories:
        added = False

        for cluster in clusters:
            for existing_story in cluster:
                if same_story(
                    story["title"],
                    existing_story["title"]
                ):
                    cluster.append(story)
                    added = True
                    break

            if added:
                break

        if not added:
            clusters.append([story])

    return clusters