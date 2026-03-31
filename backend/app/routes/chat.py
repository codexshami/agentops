from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatRequestSchema, ChatResponseSchema
from app.services.openai_service import OpenAIService
from app.services.conversation_service import ConversationService
from app.utils.logger import logger
from app.utils.errors import InvalidInput
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])
openai_service = OpenAIService()

@router.post("/send", response_model=ChatResponseSchema)
async def send_message(
    request: ChatRequestSchema,
    db: Session = Depends(get_db)
):
    """Send message and get AI response"""
    
    # Validate input
    if not request.message.strip():
        raise InvalidInput("Message cannot be empty")
    
    try:
        # Create or get conversation
        if request.conversation_id:
            conversation = ConversationService.get_conversation(
                db, request.conversation_id
            )
        else:
            conversation = ConversationService.create_conversation(db)
        
        # Add user message
        ConversationService.add_message(
            db, conversation.id, "user", request.message
        )
        
        # Get conversation history
        history = ConversationService.get_conversation_history(
            db, conversation.id
        )
        
        # Generate AI response
        response_data = openai_service.generate_response(history)
        
        # Add assistant message
        message = ConversationService.add_message(
            db, conversation.id, "assistant", 
            response_data["content"], response_data["tokens_used"]
        )
        
        logger.info(f"Message processed for conversation {conversation.id}")
        
        return ChatResponseSchema(
            conversation_id=conversation.id,
            message_id=message.id,
            response=response_data["content"],
            tokens_used=response_data["tokens_used"],
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-code")
async def generate_code(request: ChatRequestSchema, db: Session = Depends(get_db)):
    """Generate code based on prompt"""
    
    if not request.message.strip():
        raise InvalidInput("Prompt cannot be empty")
    
    try:
        response_data = openai_service.generate_code(request.message)
        return {
            "code": response_data["content"],
            "tokens_used": response_data["tokens_used"],
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Error in generate_code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))