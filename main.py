from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime, Enum, ARRAY, Float, Boolean
import enum


Base = declarative_base()


class Collaborator(Base):
    __tablename__ = 'collaborators'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, index=True)


load_dotenv()

db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost:{db_port}/{db_name}"
print(f'db url: {db_url}')

try:
    engine = create_engine(db_url)
    connection = engine.connect()
    print(f'connected: port {db_port}')
    Base.metadata.create_all(bind=engine)
    print("tables created")
except Exception as e:
    print(e)

