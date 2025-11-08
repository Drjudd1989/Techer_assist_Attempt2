from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb
import os

def get_vector_store() -> Chroma:
    """
    Initializes and returns a LangChain vector store backed by ChromaDB.
    """
    # Initialize the embedding function
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Initialize the ChromaDB client with persistence
    client = chromadb.PersistentClient(path="chroma_db")

    # Initialize the LangChain vector store
    vector_store = Chroma(
        client=client,
        collection_name="curriculum",
        embedding_function=embedding_function,
    )
    return vector_store

def add_vectors_to_db(text_chunks: list, filename: str):
    """Adds a batch of text chunks to the vector database."""
    vector_store = get_vector_store()

    # Create a unique ID for each chunk to prevent duplicates.
    ids = [f"{filename}-{i}" for i in range(len(text_chunks))]

    vector_store.add_texts(
        texts=text_chunks,
        metadatas=[{"source": filename} for _ in text_chunks],
        ids=ids
    )
