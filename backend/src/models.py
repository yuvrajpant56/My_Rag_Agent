from pydantic import BaseModel

class IngestRequest(BaseModel):
    text: str

class IngestResponse(BaseModel):
    success: bool
    message: str
    
class ChatRequest(BaseModel):
    question: str
    
class ChatResponse(BaseModel):
    answer: str