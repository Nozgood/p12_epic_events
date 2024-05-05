import models
import bcrypt
import errors
import validators


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
            raise ValueError(errors.ERR_COLLABORATOR_NOT_FOUND)
        if self.is_password_correct(password, collaborator.password) is False:
            raise ValueError(errors.ERR_COLLABORATOR_NOT_FOUND)
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
                self.view.display_error(errors.ERR_MENU_INPUT)
        return

    def set_new_collaborator_email(self):
        email = ""
        while email == "":
            try:
                email_input = self.view.input_email()
                validators.validate_email(email_input)
                self.is_email_in_database(email_input)
                email = email_input
                continue
            except ValueError as err:
                self.view.display_error(err)
                continue
        return email

    def set_new_collaborator_password(self):
        password = ""
        while password == "":
            try:
                password_input = self.view.input_password()
                validators.validate_password(password_input)
                password = password_input
                continue
            except ValueError as err:
                self.view.display_error(err)
                continue
        return password

    def create_collaborator(self):
        self.view.display_new_collaborator_panel()
        new_collaborator = models.Collaborator(
                email=self.set_new_collaborator_email(),
                password=self.set_new_collaborator_password(),
                role=self.view.input_collaborator_role(),
                first_name=self.view.input_first_name(),
                last_name=self.view.input_last_name(),
            )
        try:
            self.session.add(new_collaborator)
            self.session.commit()
            return self.view.display_new_collaborator_validation()
        except Exception as err:
            self.session.rollback()
            return self.view.display_error(err)

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
            return self.view.display_update_customer_validation()
        except ValueError as err:
            return self.view.display_error(err)

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
            raise ValueError(errors.ERR_COLLABORATOR_NOT_FOUND)
        return collaborator

    def is_email_in_database(self, email):
        if (
            self.
            session.
            query(models.Collaborator).
            filter_by(email=email).
            first()
            is not None
        ):
            raise ValueError(errors.ERR_EMAIL_ALREADY_EXISTS)
