import uuid

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime
from models.base import Base


class Event(Base):
    def __init__(
            self,
            name,
            start_date,
            end_date,
            location,
            attendees,
            notes,
            customer,
            deal
    ):
        self.id = uuid.uuid4()
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.attendees = attendees
        self.notes = notes

        self.customer = customer
        self.deal = deal

    __tablename__ = 'events'
    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    deal_id = Column(UUID, ForeignKey("deals.id"))
    customer_id = Column(UUID, ForeignKey("customers.id"))
    contact_id = Column(UUID, ForeignKey("collaborators.id"))
    start_date = Column(DateTime, unique=False, index=True)
    end_date = Column(DateTime, unique=False, index=True)
    location = Column(String(50), unique=False, index=True)
    attendees = Column(Integer, unique=False, index=False)
    notes = Column(String(200), unique=False, index=False)

    contact = relationship("Collaborator", back_populates="events")
    customer = relationship("Customer", back_populates="events")
    deal = relationship("Deal", back_populates="events")
