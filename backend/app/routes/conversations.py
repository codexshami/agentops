from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ConversationSchema
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

@router.get("/", response_model=list[ConversationSchema])
async def get_conversations(db: Session = Depends(get_db)):
    """Get all conversations"""
    return ConversationService.get_all_conversations(db)

@router.get("/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get specific conversation"""
    return ConversationService.get_conversation(db, conversation_id)

@router.post("/create")
async def create_conversation(db: Session = Depends(get_db)):
    """Create new conversation"""
    conversation = ConversationService.create_conversation(db)
    return ConversationSchema.model_validate(conversation)