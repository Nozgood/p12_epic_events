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
                input("please insert the digit corresponding to the action you want to make: \n"))
        except ValueError:
            print("please enter a digit value")
        return menu_selection

    @staticmethod
    def input_username():
        return input("Username: ")

    @staticmethod
    def input_password():
        return input("password: ")
