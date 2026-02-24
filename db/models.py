from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    create_engine
)
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user / assistant
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))


class EmotionRecord(Base):
    __tablename__ = "emotion_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    label = Column(String)
    confidence = Column(Float)
    reason = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))


class RiskRecord(Base):
    __tablename__ = "risk_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    risk_level = Column(Integer)
    risk_reason = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    
    
    
def init_db(database_url: str):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine