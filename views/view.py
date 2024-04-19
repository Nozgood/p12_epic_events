import models
import utils
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

theme = Theme({
    "error": "red",
    "success": "bold green",
    "menu_selection": "bright_blue bold",
    "menu_text": "bright_blue",
    "panel": "bold blue",
    "input": "bold cyan"
})


class View:
    def __init__(self):
        self.console = Console(theme=theme)

    def input_welcome(self):
        self.console.print(
            Panel(
                "--- Welcome to Epic Events CRM ---",
                expand=True),
            style="panel",
            justify="center"
        )

    def input_menu_selection(self):
        menu_selection = ""
        while menu_selection == "":
            try:
                self.console.print(
                    "\n please insert the digit corresponding to the action "
                    "you want to make:",
                    style="input"
                )
                menu_selection = int(input())
            except ValueError:
                self.display_error(utils.ERR_NOT_DIGIT_VALUE)
        return menu_selection

    def display_main_menu(self):

        self.console.print(
            "[menu_selection]0[/] - Exit the application")
        self.console.print(
            "[menu_selection]1[/] - Login"
        )
        return self.input_menu_selection()

    def display_error(self, err):
        self.console.print(f"[bold]Error[/]: {err}", style="error")

    def input_welcome_user(self, collaborator):
        self.console.print(
            Panel(
                f"--- Welcome Back {collaborator.first_name} ---",
                expand=True
            ),
            style="panel",
            justify="center"
        )

    def display_collaborator_menu(self, role: models.CollaboratorRole):
        self.console.print("[menu_selection]0[/] - Logout")
        self.console.print("[menu_selection]1[/] - Display All Customers")
        self.console.print("[menu_selection]2[/] - Display All Deals")
        self.console.print("[menu_selection]3[/] - Display All Events")

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
        self.console.print("[menu_selection]4[/] - Manage Events")
        self.console.print("[menu_selection]5[/] - Manage Collaborators")
        self.console.print("[menu_selection]6[/] - Manage Deals")

    def display_commercial_menu(self):
        self.console.print("[menu_selection]4[/] - Create a new Customer")
        self.console.print("[menu_selection]5[/] - Manage your Customers")
        self.console.print("[menu_selection]6[/] - Manage your Customers Deals")
        self.console.print("[menu_selection]7[/] - Filter and Display Deals")
        self.console.print(
            "[menu_selection]8[/] - Create an Event for a Customer"
        )

    def display_support_menu(self):
        self.console.print("[menu_selection]4[/] - Filter and display Events")
        self.console.print("[menu_selection]5[/] - Manage your Events")

    def display_admin_menu(self):
        self.console.print("[menu_selection]4[/] - Create a collaborator")

    def input_new_collaborator(self):
        self.console.print(
            Panel(
                "--- New Collaborator Management ---",
                expand=True
            ),
            style="panel",
            justify="center"
        )
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
        self.console.print("--- Update Collaborator Management ---")
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

    def input_email(self):
        self.console.print("email:", style="input")
        return input()

    def input_password(self):
        self.console.print("password:", style="input")
        return input()

    def input_first_name(self):
        self.console.print("First name:", style="input")
        return input()

    def input_last_name(self):
        self.console.print("Last name:", style="input")
        return input()

    def input_collaborator_role(self):
        self.console.print(
            f"[menu_selection]1[/] - {models.CollaboratorRole.MANAGEMENT}"
        )
        self.console.print(
            f"[menu_selection]2[/] - {models.CollaboratorRole.COMMERCIAL}"
        )
        self.console.print(
            f"[menu_selection]3[/] - {models.CollaboratorRole.SUPPORT}"
        )

        role_selection = 0
        while role_selection <= 0 or role_selection > 3:
            try:
                self.console.print(
                    "Role of new collaborator: (enter the digit value)",
                    style="input"
                )
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

    def input_collaborator_management(self):
        self.console.print("[menu_selection]0[/] - Exit")
        self.console.print("[menu_selection]1[/] - Create a new Collaborator")
        self.console.print("[menu_selection]2[/] - Update a Collaborator")
        self.console.print("[menu_selection]3[/] - Delete a Collaborator")
        selection = -1
        while selection < 0 or selection > 3:
            try:
                self.console.print("Select an action:", style="input")
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
        self.console.print("Collaborator successfully updated", style="success")

    def display_delete_collaborator_validation(self):
        self.console.print("Collaborator successfully deleted", style="success")

    def display_new_collaborator_validation(self):
        self.console.print(
            "New collaborator correctly created",
            style="success"
        )
