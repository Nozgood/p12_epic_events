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
                    self.register_employee()
                case 2:
                    running = False

    @staticmethod
    def register_employee():
        print("method not implemented")
        return
