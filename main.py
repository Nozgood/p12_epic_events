from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


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
    except Exception as e:
        return e


db_connection = connect_to_database(db_url)
