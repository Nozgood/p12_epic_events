import uuid
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, UUID, DateTime, Float, Boolean
from models.base import Base


class Deal(Base):
    def __init__(
            self,
            customer,
            contact,
            bill,
            remaining_on_bill,
            has_been_signed
    ):
        self.id = uuid.uuid4()
        self.bill = bill
        self.remaining_on_bill = remaining_on_bill
        self.has_been_signed = has_been_signed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        self.contact = contact
        self.customer = customer

    __tablename__ = 'deals'

    id = Column(UUID, primary_key=True, index=True)
    customer_id = Column(UUID, ForeignKey("customers.id"))
    contact_id = Column(UUID, ForeignKey("collaborators.id"))
    bill = Column(Float, unique=False)
    remaining_on_bill = Column(Float, unique=False)
    created_at = Column(DateTime, unique=False, index=True)
    updated_at = Column(DateTime, unique=False, index=True)
    has_been_signed = Column(Boolean, unique=False, index=True)

    contact = relationship("Collaborator", back_populates="deals")
    customer = relationship("Customer", back_populates="deals")
    events = relationship("Event", back_populates="deal")
