from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from sqlalchemy.orm import sessionmaker

from models import base, collaborator, customer, deal, event


load_dotenv()

db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost:{db_port}/{db_name}"


def connect_to_db(url):
    engine = None
    try:
        engine = create_engine(url)
    except Exception as e:
        print(f'error while trying to connect to the database: {e}')
    return engine


def create_tables(engine, declarative_base):
    try:
        declarative_base.metadata.create_all(engine)
    except Exception as e:
        print(e)
    print("tables created")


def drop_tables(engine, declarative_base):
    try:
        declarative_base.metadata.drop_all(engine)
        print("all tables dropped")
    except Exception as e:
        print(f'error while trying to drop tables: {e}')


new_engine = connect_to_db(db_url)
if new_engine is None:
    print('could not connect to the db')
    exit()
# create_tables(new_engine, base.Base)
# drop_tables(new_engine, base.Base)

Session = sessionmaker(bind=new_engine)
session = Session()

collaborator_test = collaborator.Collaborator(
    name="Nowfeel Safi",
    role=collaborator.CollaboratorRole.ADMIN,
    password="password",

)

