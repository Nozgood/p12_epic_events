from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, UUID, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Collaborator(Base):

    __tablename__ = 'collaborators'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    role = Column(String, unique=False, index=True)  # How to set this as an enum ?
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=True, index=True)  # => Hash the password (lib / plugin?)

    clients = relationship("Client", back_populates="contact")  # back_populates = relation inverse
    deals = relationship("Deal", back_populates="contact")
    events = relationship("Event", back_populates="contact")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    corporation = Column(String, unique=False, index=True)
    created_at = Column(DateTime, unique=False, index=True)
    updated_at = Column(DateTime, unique=False, index=True)
    contact_id = Column(Integer, ForeignKey("collaborators.id"))  # it must be a commercial role

    contact = relationship("Collaborator", back_populates="clients")
    deals = relationship("Deal", back_populates="client")
    events = relationship("Event", back_populates="client")


class Deal(Base):
    __tablename__ = 'deals'

    id = Column(UUID, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    contact_id = Column(Integer, ForeignKey("collaborators.id"))
    bill = Column(Float, unique=False)
    remaining_on_bill = Column(Float, unique=False)
    created_at = Column(DateTime, unique=False, index=True)
    has_been_signed = Column(Boolean, unique=False, index=True)

    contact = relationship("Collaborator", back_populates="deals")
    client = relationship("Client", back_populates="deals")
    events = relationship("Event", back_populates="deal")


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

