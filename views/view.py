import models
import utils


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
                input("please insert the digit corresponding to the action "
                      "you want to make: "))
        except ValueError:
            print(utils.ERR_NOT_DIGIT_VALUE)
        return menu_selection

    def display_main_menu(self):
        print("(0) Exit the application")
        print("(1) Login")
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
        print("(4) Manage Events")
        print("(5) Manage Collaborators")
        print("(6) Manage Deals")

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

    def input_new_collaborator(self):
        print("-- New Collaborator Management --")
        first_name = self.input_first_name()
        last_name = self.input_last_name()
        password = self.input_password()
        role = self.input_collaborator_role()
        return {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "role": role
        }

    @staticmethod
    def input_first_name():
        return input("First name: ")

    @staticmethod
    def input_last_name():
        return input("Last name: ")

    def input_collaborator_role(self):
        print(f"(1) {models.CollaboratorRole.MANAGEMENT}")
        print(f"(2) {models.CollaboratorRole.COMMERCIAL}")
        print(f"(3) {models.CollaboratorRole.SUPPORT}")
        role_selection = 0
        while role_selection <= 0 or role_selection > 3:
            try:
                role_selection = int(input("Role of new collaborator: "))
                if role_selection > 3:
                    raise ValueError
            except ValueError:
                self.display_error(utils.ERR_NOT_DIGIT_VALUE)
        match role_selection:
            case 1:
                return models.CollaboratorRole.MANAGEMENT
            case 2:
                return models.CollaboratorRole.COMMERCIAL
            case _:
                return models.CollaboratorRole.SUPPORT

    @staticmethod
    def display_new_collaborator_validation():
        print("New collaborator correctly created")


    @staticmethod
    def input_collaborator_management():
        print("(1) Create a new Collaborator")
        print("(2) Update a Collaborator")
        print("(3) Delete a Collaborator")
        print("(4) Display Collaborator information")
        selection = 0
        while selection <= 0 or selection > 4:
            try:
                selection = int(input("Select an action: "))
                if selection > 4:
                    raise ValueError
            except ValueError:
                print(utils.ERR_MENU_INPUT)
        return selection
