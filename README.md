##Agentic RAG Chatbot

This is a full-stack, dockerized RAG (Retrieval-Augmented Generation) chatbot application. It uses a Next.js frontend, a FastAPI backend, and a Qdrant vector database to allow users to "chat with their documents."

The application allows users to first ingest text-based knowledge into a vector database. Then, they can ask questions, and the backend will retrieve the most relevant context from the database to provide an accurate, in-context answer from an Anthropic (Claude) LLM.

#Tech Stack

Frontend: Next.js, React, TypeScript, Tailwind CSS

Backend: FastAPI, Python, LangChain

LLM: Anthropic (Claude)

Database: Qdrant (Vector Database)

Orchestration: Docker & Docker Compose

##Architecture

This project runs entirely on Docker and is composed of three services defined in docker-compose.yml:

frontend: A Next.js application that serves the chat interface at http://localhost:3000.

backend: A FastAPI server that provides the API at http://localhost:8000. It handles both ingestion and chat logic.

qdrant: The Qdrant vector database instance, which stores the document embeddings and is accessible to the backend.

##How it Works

The application has two primary workflows:

#1. Ingestion Flow

User pastes text into the "Add Knowledge" form in the UI.

Frontend sends the text to the backend's /api/ingest endpoint.

FastAPI Backend (ingest.py):

Receives the text.

Uses the text_to_chunks function to split the text into manageable pieces.

Uses a SentenceTransformer (e.g., all-MiniLM-L6-v2) to convert each chunk into a vector embedding.

Generates a unique ID (uuid) for each chunk.

Saves the {id, vector, payload} triplets into the Qdrant database.

#2. RAG Chat Flow

User asks a question in the chatbox (e.g., "What is FastAPI?").

Frontend sends the question to the backend's /api/chat endpoint.

FastAPI Backend (rag_chain.py):

The question is embedded into a vector.

This vector is used to search Qdrant for the most similar (i.e., most relevant) text chunks.

These retrieved chunks (the "context") are formatted into a prompt along with the user's original question.

The complete, augmented prompt is sent to the Anthropic (Claude) LLM.

The LLM generates an answer based only on the provided context.

The Backend streams this answer back to the Frontend as it's generated.

Frontend parses the Server-Sent Events (SSE) stream and displays the answer word-by-word.

Getting Started

Follow these steps to set up and run the project locally.

1. Prerequisites

Docker and Docker Compose

An API key from Anthropic

2. Configuration

You must create two environment files (.env) to store your secret keys and configuration. This repository is pre-configured with a .gitignore to protect these files from being committed.

A. Backend Configuration

Create a file at backend/.env.

Copy the contents of backend/.env.example (or the content below) into it.

#Add your secret Anthropic API Key.

File: backend/.env

#--- Anthropic (Generation Model) ---
Get your key from [https://console.anthropic.com/](https://console.anthropic.com/)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
ANTHROPIC_MODEL=claude-3-haiku-20240307

--- Qdrant (Vector Database) ---
This URL works because Docker Compose creates a network where 
# the service name 'qdrant' is a valid hostname.
QDRANT_URL=http://qdrant:6333
QDRANT_COLLECTION_NAME=my_knowledge_base

# --- Embeddings (Hugging Face) ---
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2


B. Frontend Configuration

Create a file at frontend/.env.local.

Add the following line to tell the frontend where to find the backend API.

File: frontend/.env.local

NEXT_PUBLIC_API_URL=http://localhost:8000


3. Build and Run

With your configuration files in place, you can build and run the entire application with a single command from the project's root directory:

docker compose up --build


4. Use the Application

Open the web interface: http://localhost:3000

Add Knowledge: Paste some text into the "Add Knowledge" text area and click "Ingest Text".

Chat: Ask a question about the text you just ingested. The bot will use that text as context to answer your question.
