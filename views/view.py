class View:
    def __init__(self):
        return

    @staticmethod
    def input_welcome():
        print("\n --- Welcome to Epic Events CRM --- \n")

    @staticmethod
    def input_menu_selection():
        menu_selection = ""
        print("(1) Login")
        print("(2) Exit the application")
        try:
            menu_selection = int(
                input("please insert the digit corresponding to the action you want to make: "))
        except ValueError:
            print("please enter a digit value")
        return menu_selection

    @staticmethod
    def input_email():
        return input("email: ")

    @staticmethod
    def input_password():
        return input("password: ")

    @staticmethod
    def input_login_error(err):
        print(f"{err}")

    @staticmethod
    def input_welcome_user(collaborator):
        print(f"Welcome Back {collaborator.first_name}")
