from rich.panel import Panel
import views


class MainView(views.BaseView):
    def input_welcome(self):
        self.console.print(
            Panel(
                "--- Welcome to Epic Events CRM ---",
                expand=True),
            style="panel",
            justify="center"
        )

    def display_main_menu(self):
        self.console.print(
            "[menu_selection]0[/] - Exit the application")
        self.console.print(
            "[menu_selection]1[/] - Login"
        )
        return self.input_menu_selection()

    def input_welcome_user(self, collaborator):
        self.console.print(
            Panel(
                f"--- Welcome Back {collaborator.first_name} ---",
                expand=True
            ),
            style="panel",
            justify="center"
        )
