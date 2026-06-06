import spacy

class EntityService:
    def __init__(self, model: str = "en_core_web_sm"):
        self.nlp = spacy.load(model)

    def get_entities(self, text: str) -> list[tuple[str, str]]:
        """
        Returns a list of (entity_text, entity_label) pairs.
        """
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
