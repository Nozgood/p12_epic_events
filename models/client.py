from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


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
