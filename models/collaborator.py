from sqlalchemy import Column, String, UUID, Enum, ARRAY
from sqlalchemy.orm import relationship, declarative_base
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
    name = Column(String, unique=True, index=True)
    role = Column(Enum(CollaboratorRole), unique=False, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=True, index=True)
    permissions = Column(ARRAY(Enum(CollaboratorPermission)), unique=False, index=True)

    clients = relationship("Client", back_populates="contact")  # back_populates = relation inverse
    deals = relationship("Deal", back_populates="contact")
    events = relationship("Event", back_populates="contact")
