from fastapi import APIRouter, HTTPException
from models import IngestRequest, IngestResponse
from database.qdrant_db import upsert_text

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_data(request: IngestRequest):
    try:
        upsert_text(request.text)
        return IngestResponse(success=True, message="Text ingested successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest text: {e}")