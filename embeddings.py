from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Example text
text = "Machine learning is a subset of artificial intelligence."

# Convert text into an embedding
embedding = model.encode(text)

print("Embedding created successfully!")
print("Number of values:", len(embedding))
print("First 10 values:", embedding[:10])