from sentence_transformers import SentenceTransformer
import faiss

# Our example chunks
chunks = [
    "Artificial Intelligence is the field of creating machines that can perform tasks requiring human intelligence.",
    "Machine Learning is a subset of Artificial Intelligence where computers learn patterns from data."
]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for chunks
embeddings = model.encode(chunks)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# User's question
question = "What is machine learning?"

# Convert question into embedding
question_embedding = model.encode([question])

# Search for the closest chunk
distances, indices = index.search(question_embedding, k=1)

# Display result
print("Question:", question)
print("\nMost relevant chunk:")
print(chunks[indices[0][0]])

print("\nDistance:", distances[0][0])