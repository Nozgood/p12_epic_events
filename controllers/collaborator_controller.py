import models
import bcrypt
import utils


class CollaboratorController:
    def __init__(self, session, view, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def login(self):
        #email = self.view.input_email()
        #password = self.view.input_password()
        collaborator = (self.session.query(models.Collaborator).
                        filter_by(email="nowfeel@epic.io").first()
                        )
        if collaborator is None:
            raise ValueError(utils.ERR_COLLABORATOR_NOT_FOUND)
        if self.is_password_correct("test", collaborator.password) is False:
            raise ValueError(utils.ERR_COLLABORATOR_NOT_FOUND)
        self.collaborator = collaborator
        return collaborator

    @staticmethod
    def is_password_correct(input_password, db_password):
        input_bytes = input_password.encode('utf-8')
        db_bytes = db_password.encode('utf-8')
        return bcrypt.checkpw(input_bytes, db_bytes)

    def new_collaborator(self):
        email = self.view.input_email()
        if self.is_email_in_database(email):
            print(utils.ERR_EMAIL_ALREADY_EXISTS)
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
        self.view.display_new_collaborator_validation()
        return

    def is_email_in_database(self, email):
        return (self.session.query(models.Collaborator).
                filter_by(email=email).first() is not None)

    def get_permissions_by_role(self):
        permissions = models.CollaboratorPermission
        match self.collaborator.role:
            case models.CollaboratorRole.MANAGEMENT:
                return [
                    permissions.EDIT_COLLABORATOR,
                    permissions.EDIT_DEAL,
                    permissions.EDIT_EVENT
                ]
            case models.CollaboratorRole.COMMERCIAL:
                return [
                    permissions.EDIT_CUSTOMER,
                    permissions.EDIT_DEAL,
                    permissions.CREATE_EVENT
                ]
            case models.CollaboratorRole.SUPPORT:
                return [permissions.EDIT_EVENT]
            case models.CollaboratorRole.ADMIN:
                return [permissions.ALL_PERMISSIONS]
            case _:
                return []
