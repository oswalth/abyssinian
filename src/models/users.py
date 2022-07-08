from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models import Base
from models.base import GUID, BaseModel, UpdatedAtMixin


class AccessCode(BaseModel, Base):
    __tablename__ = "access_codes"

    name = Column(String)
    is_active = Column(Boolean, default=True)
    is_coach_session_enabled = Column(Boolean, default=False)
    is_communication_request_enabled = Column(Boolean, default=False)
    is_care_navigation_enabled = Column(Boolean, default=False)
    is_case_manager_notification_enabled = Column(Boolean, default=False)
    is_additional_session_request_enabled = Column(Boolean, default=False)
    coach_session_limit = Column(Integer)

    clients = relationship("Client", back_populates="access_code")
    
    
class User(BaseModel, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True)

    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True), server_default=func.now())

    hashed_password = Column(String)

    client = relationship("Client", back_populates="user", uselist=False)
    coach = relationship("Coach", back_populates="user", uselist=False)


class Coach(UpdatedAtMixin, Base):
    __tablename__ = "coaches"

    id = Column(GUID(), ForeignKey("users.id"), primary_key=True)
    sessions_limit_per_week = Column(Integer)

    user = relationship("User", back_populates="coach")
    clients = relationship("Client", back_populates="coach")


class Client(UpdatedAtMixin, Base):
    __tablename__ = "clients"

    id = Column(GUID(), ForeignKey("users.id"), primary_key=True)

    access_code_id = Column(GUID(), ForeignKey("access_codes.id"))
    coach_id = Column(GUID(), ForeignKey("coaches.id"))

    is_agree_uprise_emails = Column(Boolean, default=True)
    is_agree_terms_conditions = Column(Boolean, default=True)

    user = relationship("User", back_populates="client")
    access_code = relationship("AccessCode", back_populates="clients")
    coach = relationship("Coach", back_populates="clients")
