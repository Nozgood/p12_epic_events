from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime
from models.base import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    deal_id = Column(UUID, ForeignKey("deals.id"))
    client_id = Column(UUID, ForeignKey("clients.id"))
    contact_id = Column(UUID, ForeignKey("collaborators.id"))  # it must be a support role
    start_date = Column(DateTime, unique=False, index=True)
    end_date = Column(DateTime, unique=False, index=True)
    location = Column(String(50), unique=False, index=True)
    attendees = Column(Integer, unique=False, index=False)
    notes = Column(String(200), unique=False, index=False)

    contact = relationship("Collaborator", back_populates="events")
    client = relationship("Client", back_populates="events")
    deal = relationship("Deal", back_populates="events")
