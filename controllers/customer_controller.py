import models


class CustomerController:
    def __init__(self, session, view, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def create_customer(self):
        new_customer_input = self.view.input_new_customer()
        new_customer = models.Customer(
            first_name=new_customer_input["first_name"],
            last_name=new_customer_input["last_name"],
            email=new_customer_input["email"],
            phone_number=new_customer_input["phone_number"],
            corporation=new_customer_input["corporation"],
            contact=self.collaborator
        )
        self.session.add(new_customer)
        try:
            self.session.commit()
        except Exception as err:
            self.view.display_error(err)
            return
        return self.view.display_new_customer_validation()
