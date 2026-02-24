from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from datetime import datetime, timezone

from .models import Conversation, EmotionRecord, RiskRecord


class Repository:

    def __init__(self, engine: Engine):
        self.Session = sessionmaker(bind=engine)

    def save_message(self, user_id: str, session_id: str, role: str, content: str):

        with self.Session() as session:
            record = Conversation(
                user_id=user_id,
                session_id=session_id,
                role=role,
                content=content,
                timestamp=datetime.now(timezone.utc)
            )
            session.add(record)
            session.commit()


    def save_emotion(self, user_id: str, session_id: str, emotion: dict):
        with self.Session() as session:
            record = EmotionRecord(
                user_id=user_id,
                session_id=session_id,
                label=emotion.get("label"),
                confidence=emotion.get("confidence"),
                reason=emotion.get("reason"),
                timestamp=datetime.now(timezone.utc)
            )
            session.add(record)
            session.commit()

    def save_risk(self, user_id: str, session_id: str, risk_level: int, risk_reason: str):
        with self.Session() as session:
            record = RiskRecord(
                user_id=user_id,
                session_id=session_id,
                risk_level=risk_level,
                risk_reason=risk_reason,
                timestamp=datetime.now(timezone.utc)
            )
            session.add(record)
            session.commit()
            
