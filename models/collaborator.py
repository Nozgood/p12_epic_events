import uuid
import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Column,  String,  UUID,  Enum, ARRAY
import enum
from models.base import Base


class CollaboratorRole(enum.Enum):
    MANAGEMENT = 1
    COMMERCIAL = 2
    SUPPORT = 3
    ADMIN = 4


class CollaboratorPermission(enum.Enum):
    EDIT_COLLABORATOR = 1
    EDIT_DEAL = 2
    CREATE_EVENT = 3
    EDIT_EVENT = 4
    EDIT_CUSTOMER = 5
    ALL_PERMISSIONS = 6


def get_permissions_by_role(role: CollaboratorRole):
    permissions = CollaboratorPermission
    match role:
        case CollaboratorRole.MANAGEMENT:
            return [permissions.EDIT_COLLABORATOR, permissions.EDIT_DEAL, permissions.EDIT_EVENT]
        case CollaboratorRole.COMMERCIAL:
            return [permissions.EDIT_CUSTOMER, permissions.EDIT_DEAL, permissions.CREATE_EVENT]
        case CollaboratorRole.SUPPORT:
            return [permissions.EDIT_EVENT]
        case CollaboratorRole.ADMIN:
            return [permissions.ALL_PERMISSIONS]
        case _:
            return []


def create_hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password_bytes, salt)
    hash_password_str = hash_password.decode('utf-8')
    return hash_password_str


def is_password_correct(input_password: str, db_password: str) -> bool:
    input_bytes = input_password.encode('utf-8')
    db_bytes = db_password.encode('utf-8')
    salt = bcrypt.gensalt()
    input_hashed = bcrypt.hashpw(input_bytes, salt)
    return bcrypt.checkpw(db_bytes, input_hashed)


class Collaborator(Base):

    __tablename__ = 'collaborators'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(60), unique=True, index=True)
    role = Column(Enum(CollaboratorRole), unique=False, index=True)
    email = Column(String(60), unique=True, index=True)
    password = Column(String(60), unique=True, index=True)

    customers = relationship("Customer", back_populates="contact")  # back_populates = relation inverse
    deals = relationship("Deal", back_populates="contact")
    events = relationship("Event", back_populates="contact")

    def __init__(self, name, role, email, password):
        hashed_password = create_hash_password(password)

        self.id = uuid.uuid4()
        self.name = name
        self.role = role
        self.email = email
        self.password = hashed_password

    def __repr__(self):
        return f"Name: {self.name}" f" Role: {self.role} " f"Email: {self.email}"
