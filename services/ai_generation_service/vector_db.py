import chromadb

# Initialize the ChromaDB client with persistence
client = chromadb.PersistentClient(path="chroma_db")

# Create or get the collection for the curriculum
# In a multi-tenant application, you would create a separate collection for each user.
collection = client.get_or_create_collection(name="curriculum")

def add_vectors_to_db(text_chunks: list, embeddings: list, filename: str):
    """Adds a batch of vectors and their corresponding text to the database."""
    # Create a unique ID for each chunk to prevent duplicates.
    ids = [f"{filename}-{i}" for i in range(len(text_chunks))]

    collection.add(
        embeddings=embeddings,
        documents=text_chunks,
        metadatas=[{"source": filename} for _ in text_chunks],
        ids=ids
    )
