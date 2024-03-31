import models


class MainController:
    def __init__(self, session, view, collaborator_controller):
        self.session = session
        self.view = view
        self.collaborator_controller = collaborator_controller
        self.collaborator = None

    def run(self):
        self.view.input_welcome()
        running = True
        while running:
            menu_selection = self.view.display_main_menu()
            match menu_selection:
                case 1:
                    collaborator = None
                    try:
                        collaborator = self.collaborator_controller.login()
                    except ValueError as err:
                        self.view.display_error(err)
                        continue
                    self.collaborator = collaborator
                    self.view.input_welcome_user(self.collaborator)
                    self.collaborator_controller.get_collaborator_menu()
                case 2:
                    running = False
