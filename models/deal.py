from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean, UUID, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


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

