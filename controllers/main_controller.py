import models
from controllers.collaborator_controller import CollaboratorController


class MainController:
    def __init__(self, session, view):
        self.session = session
        self.view = view
        self.collaborator = None

    def run(self):
        self.view.input_welcome()
        running = True
        while running:
            menu_selection = self.view.input_menu_selection()
            match menu_selection:
                case 1:
                    collaborator_controller = CollaboratorController(
                        session=self.session,
                        view=self.view,
                        collaborator=None
                    )
                    try:
                        self.collaborator = collaborator_controller.login()
                    except ValueError as err:
                        self.view.input_login_error(err)

                case 2:
                    running = False

    def manage_client(self):
        pass
