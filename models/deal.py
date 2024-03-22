from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, UUID, DateTime, Float, Boolean
from models.base import Base


class Deal(Base):
    __tablename__ = 'deals'
    id = Column(UUID, primary_key=True, index=True)
    client_id = Column(UUID, ForeignKey("clients.id"))
    contact_id = Column(UUID, ForeignKey("collaborators.id"))
    bill = Column(Float, unique=False)
    remaining_on_bill = Column(Float, unique=False)
    created_at = Column(DateTime, unique=False, index=True)
    has_been_signed = Column(Boolean, unique=False, index=True)

    contact = relationship("Collaborator", back_populates="deals")
    client = relationship("Client", back_populates="deals")
    events = relationship("Event", back_populates="deal")
