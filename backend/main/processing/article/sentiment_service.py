import nltk

class SentimentService:
    def __init__(self):
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon")

        from nltk.sentiment import SentimentIntensityAnalyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text: str) -> float:
        """
        Returns a sentiment score in [-1, 1].
        Positive = positive sentiment
        Negative = negative sentiment
        """
        scores = self.analyzer.polarity_scores(text)
        return scores["compound"]
