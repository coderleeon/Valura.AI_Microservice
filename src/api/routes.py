from fastapi import APIRouter, Header, Request
from sse_starlette.sse import EventSourceResponse
from src.models.schemas import ChatRequest
from src.core.streaming import streaming_service
import uuid

router = APIRouter()

@router.post("/chat/stream")
async def chat_stream(
    chat_request: ChatRequest,
    session_id: str = Header(default=None)
):
    """
    Main SSE endpoint for the AI agent.
    Streams safety, classification, and agent execution events.
    """
    if not session_id:
        session_id = str(uuid.uuid4())
        
    generator = streaming_service.stream_orchestration(
        session_id=session_id,
        query=chat_request.query,
        portfolio_data=chat_request.portfolio
    )
    
    return EventSourceResponse(generator)
