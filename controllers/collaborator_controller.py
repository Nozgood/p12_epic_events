import models
import bcrypt


class CollaboratorController:
    def __init__(self, session, view, collaborator):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def login(self):
        email = self.view.input_email()
        password = self.view.input_password()
        collaborator = self.session.query(models.Collaborator).filter_by(email=email).first()
        db_password = collaborator.password
        if self.is_password_correct(password, db_password) is False:
            raise ValueError("incorrect password")
        self.view.input_welcome_user(collaborator)
        self.collaborator = collaborator
        return collaborator

    @staticmethod
    def is_password_correct(input_password, db_password):
        input_bytes = input_password.encode('utf-8')
        db_bytes = db_password.encode('utf-8')
        return bcrypt.checkpw(input_bytes, db_bytes)
