import models
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from controllers.main_controller import MainController
import themes
import sentry_sdk

load_dotenv()

sentry_sdk.init(
    dsn="https://c33c514f82b958d1e9076fe4b1e3fc8c@o4507271122255872"
        ".ingest.de.sentry.io/4507271125139536",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_url = (
    f"postgresql+psycopg2://{db_user}:"
    f"{db_password}@localhost:{db_port}/{db_name}"
)


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

Session = sessionmaker(bind=new_engine)
session = Session()


main_controller = MainController(
    session=session,
    console=themes.set_rich_console()
)
main_controller.run()
