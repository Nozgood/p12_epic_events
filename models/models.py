from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime, Enum, ARRAY, Float, Boolean
import enum


Base = declarative_base()


class CollaboratorRole(enum.Enum):
    MANAGEMENT = 1
    COMMERCIAL = 2
    SUPPORT = 3


class CollaboratorPermission(enum.Enum):
    EDIT_COLLABORATOR = 1
    EDIT_DEAL = 2
    EDIT_EVENT = 3
    EDIT_CLIENT = 4


class Collaborator(Base):

    __tablename__ = 'collaborators'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    role = Column(Enum(CollaboratorRole), unique=False, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(20), unique=True, index=True)
    permissions = Column(ARRAY(Enum(CollaboratorPermission)), unique=False, index=True)

    clients = relationship("Client", back_populates="contact")  # back_populates = relation inverse
    deals = relationship("Deal", back_populates="contact")
    events = relationship("Event", back_populates="contact")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    corporation = Column(String(20), unique=False, index=True)
    created_at = Column(DateTime, unique=False, index=True)
    updated_at = Column(DateTime, unique=False, index=True)
    contact_id = Column(UUID, ForeignKey("collaborators.id"))  # it must be a commercial role

    contact = relationship("Collaborator", back_populates="clients")
    deals = relationship("Deal", back_populates="client")
    events = relationship("Event", back_populates="client")


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


class Event(Base):
    __tablename__ = 'events'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    deal_id = Column(UUID, ForeignKey("deals.id"))
    client_id = Column(UUID, ForeignKey("clients.id"))
    contact_id = Column(UUID, ForeignKey("collaborators.id"))  # => it must be a support role
    start_date = Column(DateTime, unique=False, index=True)
    end_date = Column(DateTime, unique=False, index=True)
    location = Column(String(50), unique=False, index=True)
    attendees = Column(Integer, unique=False, index=False)
    notes = Column(String(200), unique=False, index=False)

    contact = relationship("Collaborator", back_populates="events")
    client = relationship("Client", back_populates="events")
    deal = relationship("Deal", back_populates="events")