from transformers import pipeline

SENTIMENT_CLASSIFIER = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="af0f99b",
)


def nickname_sentiment(team_a, team_b, **kwargs):
    """
    Uses the huggingface library to compare the sentiment of each team's nickname.
    Returns the team with the higher positive sentiment for its nickname.

    Parameters
    ----------
    team_a: Team
    team_b: Team

    Returns
    -------
    Team
    """
    a_sentiment = SENTIMENT_CLASSIFIER(team_a.nickname)[0]
    b_sentiment = SENTIMENT_CLASSIFIER(team_b.nickname)[0]
    a_score = a_sentiment["score"] * (1 if a_sentiment["label"] == "POSITIVE" else -1)
    b_score = b_sentiment["score"] * (1 if b_sentiment["label"] == "POSITIVE" else -1)
    if a_score > b_score:
        return team_a
    else:
        return team_b
