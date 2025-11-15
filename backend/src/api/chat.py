import traceback
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from models import ChatRequest
from llm.rag_chain import rag_chain

router = APIRouter()

@router.post("/chat")
async def stream_chat(request: ChatRequest):
    """Endpoint for streaming chat responses."""

    async def event_generator():
        try:
            print("--- Starting RAG chain stream... ---")
            async for chunk in rag_chain.astream(request.question):
                print(f"--- Received chunk: {chunk} ---")
                yield chunk
            print("--- RAG chain stream finished successfully. ---")
            
        except Exception as e:
            print("---!!! AN ERROR OCCURRED DURING THE STREAM !!!---")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Details: {e}")
            print("Full Traceback:")
            traceback.print_exc()
            yield "Error: A critical error occurred on the backend. Please check the server logs."

    return EventSourceResponse(event_generator())