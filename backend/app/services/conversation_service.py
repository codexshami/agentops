import uuid
from sqlalchemy.orm import Session
from app.models import Conversation, Message
from app.schemas import ConversationSchema, MessageSchema
from app.utils.logger import logger
from app.utils.errors import ConversationNotFound
from datetime import datetime

class ConversationService:
    @staticmethod
    def create_conversation(db: Session, title: str = "New Conversation") -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=title
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        logger.info(f"Created conversation: {conversation.id}")
        return conversation
    
    @staticmethod
    def get_conversation(db: Session, conversation_id: str) -> Conversation:
        """Get conversation by ID"""
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ConversationNotFound()
        return conversation
    
    @staticmethod
    def add_message(db: Session, conversation_id: str, role: str, 
                   content: str, tokens_used: int = 0) -> Message:
        """Add message to conversation"""
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            tokens_used=tokens_used
        )
        db.add(message)
        
        # Update conversation updated_at
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(message)
        logger.info(f"Added message {message.id} to conversation {conversation_id}")
        return message
    
    @staticmethod
    def get_all_conversations(db: Session) -> list:
        """Get all conversations"""
        return db.query(Conversation).order_by(
            Conversation.updated_at.desc()
        ).all()
    
    @staticmethod
    def get_conversation_history(db: Session, conversation_id: str) -> list:
        """Get message history for conversation"""
        conversation = ConversationService.get_conversation(db, conversation_id)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]