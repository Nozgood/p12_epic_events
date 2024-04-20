from sqlalchemy.orm import relationship
from sqlalchemy import Column,  String, ForeignKey, UUID, DateTime
from models.base import Base
from datetime import datetime
import uuid


class Customer(Base):

    def __init__(
            self,
            first_name,
            last_name,
            email,
            phone_number,
            corporation,
            contact
    ):
        self.id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone_number
        self.corporation = corporation
        self.contact = contact
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    __tablename__ = 'customers'

    id = Column(UUID, primary_key=True, index=True)
    first_name = Column(String(50), unique=True, index=True)
    last_name = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    corporation = Column(String(100), unique=False, index=True)
    created_at = Column(DateTime, unique=False, index=True)
    updated_at = Column(DateTime, unique=False, index=True)
    contact_id = Column(UUID, ForeignKey("collaborators.id"))

    contact = relationship("Collaborator", back_populates="customers")
    deals = relationship("Deal", back_populates="customer")
    events = relationship("Event", back_populates="customer")
