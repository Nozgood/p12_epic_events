import models
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker

import models.collaborator
from controllers.main_controller import MainController
from views.view import View

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

Session = sessionmaker(bind=new_engine)

session = Session()

#
# admin_user = models.Collaborator(
#     email="nowfeel@epic.io",
#     password="test",
#     role=models.CollaboratorRole.ADMIN,
#     first_name="Nowfeel",
#     last_name="Safi"
# )
#
# session.add(admin_user)
# session.commit()
# exit()

view = View()
main_controller = MainController(session=session, view=view)
main_controller.run()
