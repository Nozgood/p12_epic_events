from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from models.models import Base

load_dotenv()

db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@localhost:{db_port}/{db_name}"


def connect_to_database(url: str):
    engine = create_engine(url)
    try:
        connection = engine.connect()
        print(f'connected: {connection}')
        Base.metadata.create_all(bind=connection)
        return connection
    except Exception as e:
        print(e)
        return e


test = connect_to_database(db_url)
