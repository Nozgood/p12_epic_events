import models


class Controller:
    def __init__(self, session, view):
        self.session = session
        self.view = view

    def run(self):
        self.view.input_welcome()
        running = True
        while running:
            menu_selection = self.view.input_menu_selection()
            match menu_selection:
                case 1:
                    self.login()
                case 2:
                    running = False

    def login(self):
        name = self.view.input_username()
        password = self.view.input_password()
        collaborator = self.session.query(models.Collaborator).filter_by(name=name).first()
        print(f'collaborator: {collaborator}')
        return
