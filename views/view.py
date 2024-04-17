import models
import utils
from rich.console import Console


class View:
    def __init__(self):
        self.console = Console()

    def input_welcome(self):
        self.console.print("\n --- Welcome to Epic Events CRM --- \n")

    def input_menu_selection(self):
        menu_selection = ""
        try:
            self.console.print(
                "please insert the digit corresponding to the action "
                "you want to make:"
            )
            menu_selection = int(input())
        except ValueError:
            self.console.print(utils.ERR_NOT_DIGIT_VALUE)
        return menu_selection

    def display_main_menu(self):
        self.console.print("(0) Exit the application")
        self.console.print("(1) Login")
        return self.input_menu_selection()

    def input_email(self):
        self.console.print("email:")
        return input()

    def input_password(self):
        self.console.print("password:")
        return input()

    def display_error(self, err):
        self.console.print(f"{err}")

    def input_welcome_user(self, collaborator):
        self.console.print(f"Welcome Back {collaborator.first_name}")

    def display_collaborator_menu(self, role: models.CollaboratorRole):
        self.console.print("(0) Logout")
        self.console.print("(1) Display All Customers")
        self.console.print("(2) Display All Deals")
        self.console.print("(3) Display All Events")

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

    def display_management_menu(self):
        self.console.print("(4) Manage Events")
        self.console.print("(5) Manage Collaborators")
        self.console.print("(6) Manage Deals")

    def display_commercial_menu(self):
        self.console.print("(4) Create a new Customer")
        self.console.print("(5) Manage your Customers")
        self.console.print("(6) Manage your Customers Deals")
        self.console.print("(7) Filter and Display Deals")
        self.console.print("(8) Create an Event for a Customer")

    def display_support_menu(self):
        self.console.print("(4) Filter and display Events")
        self.console.print("(5) Manage your Events")

    def display_admin_menu(self):
        self.console.print("(4) Create a collaborator")

    def input_new_collaborator(self):
        self.console.print("-- New Collaborator Management --")
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

    def input_update_collaborator(self):
        self.console.print("-- Update Collaborator Management --")
        email = self.input_email()
        first_name = self.input_first_name()
        last_name = self.input_last_name()
        role = self.input_collaborator_role()
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role
        }

    def input_first_name(self):
        self.console.print("First name:")
        return input()

    def input_last_name(self):
        self.console.print("Last name:")
        return input()

    def input_collaborator_role(self):
        self.console.print(f"(1) {models.CollaboratorRole.MANAGEMENT}")
        self.console.print(f"(2) {models.CollaboratorRole.COMMERCIAL}")
        self.console.print(f"(3) {models.CollaboratorRole.SUPPORT}")
        role_selection = 0
        while role_selection <= 0 or role_selection > 3:
            try:
                self.console.print("Role of new collaborator:")
                role_selection = int(input())
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

    def display_new_collaborator_validation(self):
        self.console.print("New collaborator correctly created")

    def input_collaborator_management(self):
        self.console.print("(0) Exit")
        self.console.print("(1) Create a new Collaborator")
        self.console.print("(2) Update a Collaborator")
        self.console.print("(3) Delete a Collaborator")
        selection = -1
        while selection < 0 or selection > 3:
            try:
                self.console.print("Select an action:")
                selection = int(input())
                if selection > 3 or selection < 0:
                    raise ValueError
            except ValueError:
                self.console.print(utils.ERR_MENU_INPUT)
        return selection

    def display_collaborator_information(self, collaborator):
        self.console.print(
            f"First Name: {collaborator.first_name} \n"
            f"Last Name: {collaborator.last_name} \n"
            f"Role: {collaborator.role} \n"
            f"Email: {collaborator.email} \n"
        )

    def display_update_collaborator_validation(self):
        self.console.print("Collaborator successfully updated")

    def display_delete_collaborator_validation(self):
        self.console.print("Collaborator successfully deleted")
