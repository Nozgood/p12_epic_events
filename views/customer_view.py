import views
from rich.panel import Panel
from datetime import datetime

class CustomerView(views.BaseView):

    def input_first_name(self):
        self.console.print("First name:", style="input")
        return input()

    def input_last_name(self):
        self.console.print("Last name:", style="input")
        return input()

    def input_email(self):
        self.console.print("email:", style="input")
        return input()

    def input_phone_number(self):
        self.console.print("phone number:", style="input")
        return input()

    def input_corporation(self):
        self.console.print("corporation:", style="input")
        return input()

    def input_new_customer(self):
        self.console.print(
            Panel(
                "--- New Customer Management ---",
                expand=True
            ),
            style="panel",
            justify="center"
        )
        fist_name = self.input_first_name()
        last_name = self.input_last_name()
        email = self.input_email()
        phone_number = self.input_phone_number()
        corporation = self.input_corporation()

        return {
            "first_name": fist_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "corporation": corporation
        }

    def display_new_customer_validation(self):
        return self.console.print(
            "New collaborator correctly created",
            style="success"
        )
