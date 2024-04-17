import models
import bcrypt
import utils


class CollaboratorController:
    def __init__(self, session, view, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def login(self):
        email = self.view.input_email()
        password = self.view.input_password()
        collaborator = (self.session.query(models.Collaborator).
                        filter_by(email=email).first()
                        )
        if collaborator is None:
            raise ValueError(utils.ERR_COLLABORATOR_NOT_FOUND)
        if self.is_password_correct(password, collaborator.password) is False:
            raise ValueError(utils.ERR_COLLABORATOR_NOT_FOUND)
        self.collaborator = collaborator
        return collaborator

    @staticmethod
    def is_password_correct(input_password, db_password):
        input_bytes = input_password.encode('utf-8')
        db_bytes = db_password.encode('utf-8')
        return bcrypt.checkpw(input_bytes, db_bytes)

    def manage_collaborators(self):
        selection = self.view.input_collaborator_management()
        match selection:
            case 0:
                return
            case 1:
                self.create_collaborator()
            case 2:
                self.update_collaborator()
            case 3:
                self.delete_collaborator()
            case _:
                self.view.display_error(utils.ERR_MENU_INPUT)
        return

    def create_collaborator(self):
        email = self.view.input_email()
        if self.is_email_in_database(email):
            self.view.display_error(utils.ERR_EMAIL_ALREADY_EXISTS)
            return
        new_collaborator_input = self.view.input_new_collaborator()
        new_collaborator_input["email"] = email
        new_collaborator = models.Collaborator(
            first_name=new_collaborator_input["first_name"],
            last_name=new_collaborator_input["last_name"],
            email=new_collaborator_input["email"],
            password=new_collaborator_input["password"],
            role=new_collaborator_input["role"]
        )
        self.session.add(new_collaborator)
        try:
            self.session.commit()
        except Exception as err:
            self.view.display_error(err)
            return
        return self.view.display_new_collaborator_validation()

    def update_collaborator(self):
        try:
            collaborator = self.get_collaborator()
            self.view.display_collaborator_information(collaborator)
            update_collaborator_input = self.view.input_update_collaborator()
            collaborator.email = update_collaborator_input["email"]
            collaborator.first_name = update_collaborator_input["first_name"]
            collaborator.last_name = update_collaborator_input["last_name"]
            collaborator.role = update_collaborator_input["role"]
            self.session.commit()
            return self.view.display_update_collaborator_validation()
        except ValueError:
            return

    def delete_collaborator(self):
        try:
            collaborator = self.get_collaborator()
            self.session.delete(collaborator)
            self.session.commit()
            return self.view.display_delete_collaborator_validation()
        except ValueError:
            return

    def get_collaborator(self):
        email = self.view.input_email()
        collaborator = (
            self.
            session.
            query(models.Collaborator).
            filter_by(email=email).
            first()
        )
        if collaborator is None:
            raise ValueError(utils.ERR_COLLABORATOR_NOT_FOUND)
        return collaborator

    def is_email_in_database(self, email):
        return (self.session.query(models.Collaborator).
                filter_by(email=email).first() is not None)
