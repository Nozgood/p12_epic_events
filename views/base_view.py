import errors


class BaseView:
    def __init__(self, console):
        self.console = console

    def display_error(self, err):
        self.console.print(f"[bold]Error[/]: {err}", style="error")

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
                self.display_error(errors.ERR_NOT_DIGIT_VALUE)
        return menu_selection
