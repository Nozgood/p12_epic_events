from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from models import base, collaborator, customer, deal, event


load_dotenv()

db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost:{db_port}/{db_name}"


def connect_to_db(url):
    try:
        engine = create_engine(url)
    except Exception as e:
        return e
    return engine


def create_tables(engine, declarative_base):
    try:
        declarative_base.metadata.create_all(engine)
    except Exception as e:
        return e


engine = connect_to_db(db_url)
print(f'connected: port {db_port}')
create_tables(engine, base.Base)
print("tables created")


