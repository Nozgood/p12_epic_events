import models


class View:
    def __init__(self):
        return

    @staticmethod
    def input_welcome():
        print("\n --- Welcome to Epic Events CRM --- \n")

    @staticmethod
    def input_menu_selection():
        menu_selection = ""
        try:
            menu_selection = int(
                input("please insert the digit corresponding to the action you want to make: "))
        except ValueError:
            print("please enter a digit value")
        return menu_selection

    def display_main_menu(self):
        print("(1) Login")
        print("(2) Exit the application")
        return self.input_menu_selection()

    @staticmethod
    def input_email():
        return input("email: ")

    @staticmethod
    def input_password():
        return input("password: ")

    @staticmethod
    def display_error(err):
        print(f"{err}")

    @staticmethod
    def input_welcome_user(collaborator):
        print(f"Welcome Back {collaborator.first_name}")

    def display_collaborator_menu(self, role: models.CollaboratorRole):
        print("(0) Logout")
        print("(1) Display All Customers")
        print("(2) Display All Deals")
        print("(3) Display All Events")

        match role:
            case models.CollaboratorRole.MANAGEMENT:
                self.display_management_menu()
            case models.CollaboratorRole.COMMERCIAL:
                self.display_commercial_menu()
            case models.CollaboratorRole.SUPPORT:
                self.display_support_menu()
            case models.CollaboratorRole.ADMIN:
                self.display_admin_menu()

        return self.input_menu_selection()

    @staticmethod
    def display_management_menu():
        print("(4) Manage Collaborators")
        print("(5) Manage Deals")
        print("(6) Filter and display Events")
        print("(7) Edit an Event")

    @staticmethod
    def display_commercial_menu():
        print("(4) Create a new Customer")
        print("(5) Manage your Customers")
        print("(6) Manage your Customers Deals")
        print("(7) Filter and Display Deals")
        print("(8) Create an Event for a Customer")

    @staticmethod
    def display_support_menu():
        print("(4) Filter and display Events")
        print("(5) Manage your Events")

    @staticmethod
    def display_admin_menu():
        print("(4) Create a collaborator")
