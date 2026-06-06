import yake

class KeywordService:
    def __init__(self, max_keywords: int = 10):
        self.extractor = yake.KeywordExtractor(top=max_keywords)

    def get_keywords(self, text: str) -> list[str]:
        """
        Returns a list of keywords sorted by relevance.
        """
        keywords = self.extractor.extract_keywords(text)
        return [kw for kw, score in keywords]
