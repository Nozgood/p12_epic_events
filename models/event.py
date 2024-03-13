from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    deal_id = Column(Integer, ForeignKey("contacts.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    contact_id = Column(Integer, ForeignKey("collaborators.id"))  # => it must be a support role
    start_date = Column(DateTime, unique=False, index=True)
    end_date = Column(DateTime, unique=False, index=True)
    location = Column(String, unique=False, index=True)
    attendees = Column(Integer, unique=False, index=False)
    notes = Column(String, unique=False, index=False)

    contact = relationship("Collaborator", back_populates="events")
    client = relationship("Client", back_populates="events")
    deal = relationship("Deal", back_populates="events")
