import logging
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Echobot API",
    description="A simple echo chatbot API that returns user messages with a prefix",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    """Request model for chat messages."""
    message: str = Field(..., min_length=1, max_length=1000, description="The message to be echoed")

    class Config:
        schema_extra = {
            "example": {
                "message": "Hello, how are you?"
            }
        }

class ChatResponse(BaseModel):
    """Response model for chat messages."""
    reply: str = Field(..., description="The echoed message with prefix")

    class Config:
        schema_extra = {
            "example": {
                "reply": "You said: Hello, how are you?"
            }
        }

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Service message")

@app.exception_handler(Exception)
async def global_exception_handler(request: Any, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.post("/chat", 
         response_model=ChatResponse,
         summary="Echo a message",
         description="Takes a message and returns it with a 'You said:' prefix",
         response_description="The echoed message with prefix")
async def chat(message: ChatMessage) -> ChatResponse:
    """
    Echo back the user's message with a prefix.
    
    Args:
        message (ChatMessage): The message to be echoed
        
    Returns:
        ChatResponse: The echoed message with prefix
        
    Raises:
        HTTPException: If the message processing fails
    """
    try:
        logger.info(f"Received message: {message.message}")
        response = ChatResponse(reply=f"You said: {message.message}")
        logger.info(f"Sending response: {response.reply}")
        return response
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process message")

@app.get("/",
        response_model=HealthResponse,
        summary="Health check",
        description="Check if the API is running",
        response_description="Health status of the API")
async def root() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: The health status of the API
    """
    return HealthResponse(
        status="healthy",
        message="Echobot API is running"
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 