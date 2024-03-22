from sqlalchemy.orm import relationship
from sqlalchemy import Column,  String, ForeignKey, UUID, DateTime
from models.base import Base


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    corporation = Column(String(20), unique=False, index=True)
    created_at = Column(DateTime, unique=False, index=True)
    updated_at = Column(DateTime, unique=False, index=True)
    contact_id = Column(UUID, ForeignKey("collaborators.id"))

    contact = relationship("Collaborator", back_populates="customers")
    deals = relationship("Deal", back_populates="customer")
    events = relationship("Event", back_populates="customer")
