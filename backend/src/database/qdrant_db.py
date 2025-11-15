from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from config import settings
import numpy as np
import uuid # Import the uuid library to generate unique IDs

# Initialize the embedding model once
EMBEDDING_MODEL = SentenceTransformer(settings.EMBEDDING_MODEL)
embedding_size = EMBEDDING_MODEL.get_sentence_embedding_dimension()

# Initialize Qdrant client
qdrant_client = QdrantClient(url=settings.QDRANT_URL)

def get_qdrant_client():
    return qdrant_client

def initialize_qdrant():
    """Ensure the collection exists in Qdrant."""
    try:
        qdrant_client.get_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
        print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' already exists.")
    except Exception:
        print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' not found. Creating...")
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=embedding_size, distance=models.Distance.COSINE),
        )
        print("Collection created successfully.")

def text_to_chunks(text: str, chunk_size: int = 512, overlap: int = 50):
    """Splits text into overlapping chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def upsert_text(text: str):
    """Chunks, embeds, and upserts text into Qdrant."""
    chunks = text_to_chunks(text)
    
    # Generate embeddings for each chunk
    vectors = EMBEDDING_MODEL.encode(chunks, convert_to_tensor=False).tolist()
    
    # Generate a unique ID for each chunk/vector
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Prepare points for upsertion
    # *** THIS IS THE FIX: Changed payload key from "text" to "page_content" ***
    points = [
        models.PointStruct(id=id, vector=vector, payload={"page_content": chunk})
        for id, vector, chunk in zip(ids, vectors, chunks)
    ]
    
    # Upsert points into the collection
    qdrant_client.upsert(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        points=points,
        wait=True
    )
    print(f"Successfully upserted {len(chunks)} chunks of text.")

