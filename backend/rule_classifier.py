# Rule-based query classifier
import re


def classify_by_rules(text):
    """
    Returns:
        "fact_claim"
        "opinion"
        None (if no rule matches)
    """

    # Convert everything to lowercase
    text = text.lower().strip()

    # -----------------------------
    # Rule 1: Factual Questions
    # -----------------------------
    fact_starters = (
        "is ", "are ", "was ", "were ",
        "do ", "does ", "did ",
        "has ", "have ", "had ",
        "can ", "could ",
        "will ", "would ",
        "who ", "what ", "when ",
        "where ", "which ",
        "how many ", "how much "
    )

    if text.startswith(fact_starters):
        return "fact_claim"

    # -----------------------------
    # Rule 2: Subjective words
    # -----------------------------
    opinion_words = [
        "best",
        "greatest",
        "better",
        "worst",
        "beautiful",
        "amazing",
        "favorite",
        "overrated",
        "underrated",
        "boring",
        "awesome",
        "terrible"
    ]

    for word in opinion_words:
        if word in text:
            return "opinion"

    # -----------------------------
    # Rule 3: Comparisons
    # -----------------------------
    comparison_words = [
        "better than",
        "worse than",
        "greater than",
        "less than",
        "more than"
    ]

    for word in comparison_words:
        if word in text:
            return "opinion"

    # -----------------------------
    # No rule matched
    # -----------------------------
    return None