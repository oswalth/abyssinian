import uuid

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models import Base


class AccessCode(Base):
    __tablename__ = "access_codes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    is_coach_session_enabled = Column(Boolean, default=False)
    is_communication_request_enabled = Column(Boolean, default=False)
    is_care_navigation_enabled = Column(Boolean, default=False)
    is_case_manager_notification_enabled = Column(Boolean, default=False)
    is_additional_session_request_enabled = Column(Boolean, default=False)
    coach_session_limit = Column(Integer)

    clients = relationship("Client", back_populates="access_code")
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), server_default=func.now())

    hashed_password = Column(String)

    client = relationship("Client", back_populates="user", uselist=False)
    coach = relationship("Coach", back_populates="user", uselist=False)


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    sessions_limit_per_week = Column(Integer)

    user = relationship("User", back_populates="coach")
    clients = relationship("Client", back_populates="coach")


class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    access_code_id = Column(UUID(as_uuid=True), ForeignKey("access_codes.id"))
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coaches.id"))

    is_agree_uprise_emails = Column(Boolean, default=True)
    is_agree_terms_conditions = Column(Boolean, default=True)

    user = relationship("User", back_populates="client")
    access_code = relationship("AccessCode", back_populates="clients")
    coach = relationship("Coach", back_populates="clients")
