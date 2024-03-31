import models
import bcrypt

ERR_COLLABORATOR_NOT_FOUND = "Collaborator not found, email or password incorrect"
ERR_MENU_INPUT = "Not valid menu selection"


class CollaboratorController:
    def __init__(self, session, view, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def login(self):
        email = self.view.input_email()
        password = self.view.input_password()
        collaborator = self.session.query(models.Collaborator).filter_by(email=email).first()
        if collaborator is None:
            raise ValueError(ERR_COLLABORATOR_NOT_FOUND)
        if self.is_password_correct(password, collaborator.password) is False:
            raise ValueError(ERR_COLLABORATOR_NOT_FOUND)
        self.collaborator = collaborator
        return collaborator

    @staticmethod
    def is_password_correct(input_password, db_password):
        input_bytes = input_password.encode('utf-8')
        db_bytes = db_password.encode('utf-8')
        return bcrypt.checkpw(input_bytes, db_bytes)

    def get_collaborator_menu(self):
        running = True
        while running:
            menu_selection = self.view.display_collaborator_menu(self.collaborator.role)
            if menu_selection == 0:
                running = False
            match self.collaborator.role:
                case models.CollaboratorRole.MANAGEMENT:
                    self.process_management_action(menu_selection)
                case models.CollaboratorRole.COMMERCIAL:
                    self.process_commercial_action(menu_selection)
                case models.CollaboratorRole.SUPPORT:
                    self.process_support_action(menu_selection)
                case _:
                    self.process_admin_action(menu_selection)

    def process_management_action(self, menu_selection):
        if menu_selection > 7:
            self.view.display_error(ERR_MENU_INPUT)
            return

    def process_commercial_action(self, menu_selection):
        if menu_selection > 8:
            self.view.display_error(ERR_MENU_INPUT)
            return

    def process_support_action(self, menu_selection):
        if menu_selection > 5:
            self.view.display_error(ERR_MENU_INPUT)
            return

    def process_admin_action(self, menu_selection):
        if menu_selection > 4:
            self.view.display_error(ERR_MENU_INPUT)
            return

        if menu_selection == 4:
            print("hello bro on va créer un collaborateur maintenant")

    def get_permissions_by_role(self):
        permissions = models.CollaboratorPermission
        match self.collaborator.role:
            case models.CollaboratorRole.MANAGEMENT:
                return [permissions.EDIT_COLLABORATOR, permissions.EDIT_DEAL, permissions.EDIT_EVENT]
            case models.CollaboratorRole.COMMERCIAL:
                return [permissions.EDIT_CUSTOMER, permissions.EDIT_DEAL, permissions.CREATE_EVENT]
            case models.CollaboratorRole.SUPPORT:
                return [permissions.EDIT_EVENT]
            case models.CollaboratorRole.ADMIN:
                return [permissions.ALL_PERMISSIONS]
            case _:
                return []
