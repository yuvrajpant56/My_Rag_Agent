from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import ingest, chat
from database.qdrant_db import initialize_qdrant

app = FastAPI(
    title="Agentic RAG Chatbot API",
    description="API for a RAG chatbot using FastAPI, Anthropic, and Qdrant.",
    version="1.0.0"
)

# CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:3000",  # Allow frontend origin
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(ingest.router, prefix="/api", tags=["Ingestion"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.on_event("startup")
def on_startup():
    """Actions to perform on application startup."""
    initialize_qdrant()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the RAG Chatbot API!"}