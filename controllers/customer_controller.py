import models


class CustomerController:
    def __init__(self, session, view, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def create_customer(self):
        new_customer_input = self.view.input_new_customer()
        new_customer = models.Customer(

        )
