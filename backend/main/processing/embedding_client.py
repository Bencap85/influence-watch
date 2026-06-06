from main.processing.openai_http import post

class EmbeddingClient:

    def embed_http(self, text: str) -> list[float]:
        payload = {
            "model": "text-embedding-3-small",
            "input": text,
        }
        data = post("/embeddings", payload)
        return data["data"][0]["embedding"]

    def batch_embed_http(self, texts: list[str], logger = None) -> list[list[float]]:
        payload = {
            "model": "text-embedding-3-small",
            "input": texts,
        }
        data = post("/embeddings", payload)
        return [item["embedding"] for item in data["data"]]
