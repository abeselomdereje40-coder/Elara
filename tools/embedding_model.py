from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    def __init__(self):
        print("Loading multilingual-e5-small...")

        model_path = r"C:\Users\user\.cache\huggingface\hub\models--intfloat--multilingual-e5-small\snapshots\614241f622f53c4eeff9890bdc4f31cfecc418b3"

        self.model = SentenceTransformer(
            model_path,
            local_files_only=True
        )

        print("Embedding model loaded.")
    def embed_documents(self, texts):

        if not texts:
            return []

        texts = [
            f"passage: {text}"
            for text in texts
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings

    def embed_query(self, query):

        query = f"query: {query}"

        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        return embedding[0]