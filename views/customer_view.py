import models
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

    def input_customer_information(self):
        self.console.print(
            Panel(
                "---Customer Management ---",
                expand=True
            ),
            style="panel",
            justify="center"
        )
        fist_name = self.input_first_name()
        last_name = self.input_last_name()
        corporation = self.input_corporation()

        return {
            "first_name": fist_name,
            "last_name": last_name,
            "corporation": corporation
        }

    def display_new_customer_validation(self):
        return self.console.print(
            "New collaborator correctly created",
            style="success"
        )

    def display_customer_information(self, customer: models.Customer):
        return self.console.print(
            f"[input]First Name[/]: {customer.first_name} \n"
            f"[input]Last Name[/]: {customer.last_name} \n"
            f"[input]Phone[/]: {customer.phone} \n"
            f"[input]Email[/]: {customer.email} \n"
            f"[input]Corporation[/]: {customer.corporation} \n"
            "--------------- \n"
        )

    def input_update_customer(self):
        self.console.print(
            Panel(
                "--- Update Customer Management ---",
                expand=True
            ),
            style="panel",
            justify="center"
        )
        first_name = self.input_first_name()
        last_name = self.input_last_name()
        phone = self.input_phone_number()
        return {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone
        }

    def display_update_customer_validation(self):
        self.console.print("Customer successfully updated", style="success")