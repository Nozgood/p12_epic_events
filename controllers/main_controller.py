import models
from utils import ERR_MENU_INPUT


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
                case 0:
                    running = False
                case 1:
                    collaborator = None
                    try:
                        collaborator = self.collaborator_controller.login()
                    except ValueError as err:
                        self.view.display_error(err)
                        continue
                    self.collaborator = collaborator
                    self.view.input_welcome_user(self.collaborator)
                    self.get_collaborator_menu()

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
        match menu_selection:
            case 0:
                return
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                new_collaborator = self.collaborator_controller.new_collaborator()
            case _:
                self.view.display_error(ERR_MENU_INPUT)
