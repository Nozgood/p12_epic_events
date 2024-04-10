import uuid
import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Column,  String,  UUID,  Enum
import enum
from models.base import Base


class CollaboratorPermission:
    EDIT_COLLABORATOR = 1
    EDIT_DEAL = 2
    CREATE_EVENT = 3
    EDIT_EVENT = 4
    EDIT_CUSTOMER = 5
    ALL_PERMISSIONS = 6


class CollaboratorRole(enum.Enum):
    MANAGEMENT = 1
    COMMERCIAL = 2
    SUPPORT = 3
    ADMIN = 4

    def __str__(self):
        return self.name


def create_hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password_bytes, salt)
    hash_password_str = hash_password.decode('utf-8')
    return hash_password_str


class Collaborator(Base):

    __tablename__ = 'collaborators'

    id = Column(UUID, primary_key=True, index=True)
    first_name = Column(String(60), unique=False, index=True)
    last_name = Column(String(60), unique=False, index=True)
    role = Column(Enum(CollaboratorRole), unique=False, index=True)
    email = Column(String(60), unique=True, index=True)
    password = Column(String(60), unique=True, index=True)

    customers = relationship("Customer", back_populates="contact")
    deals = relationship("Deal", back_populates="contact")
    events = relationship("Event", back_populates="contact")

    def __init__(self, first_name, last_name, role, email, password):
        hashed_password = create_hash_password(password)

        self.id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.email = email
        self.password = hashed_password

    def __repr__(self):
        return (
            f"Email: {self.email}" 
            f" Role: {self.role} "  
            f"Name: {self.first_name} {self.last_name} "
        )
