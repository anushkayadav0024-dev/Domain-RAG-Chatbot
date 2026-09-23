from sentence_transformers import SentenceTransformer
import faiss


class VectorStore:
    def __init__(self, chunks):
        self.chunks = chunks

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        texts = [chunk.page_content for chunk in chunks]

        self.embeddings = self.model.encode(texts)

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(self.embeddings)

    def search(self, question, k=3):
        k = min(k, len(self.chunks))

        question_embedding = self.model.encode([question])

        distances, indices = self.index.search(
            question_embedding,
            k
        )

        results = []

        for index in indices[0]:
            results.append(self.chunks[index])

        return results
        