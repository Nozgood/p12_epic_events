import models
import errors
import validators
import views
from datetime import datetime

class CustomerController:
    def __init__(self, session, view: views.CustomerView, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def create_customer(self):
        email = self.set_new_customer_email()
        phone = self.set_customer_phone()
        new_customer_input = self.view.input_customer_information()
        new_customer = models.Customer(
            first_name=new_customer_input["first_name"],
            last_name=new_customer_input["last_name"],
            email=email,
            phone_number=phone,
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

    def update_customer(self):
        try:
            customer = self.get_customer(self.collaborator)
            self.view.display_customer_information(customer)
            phone = self.set_customer_phone()
            update_customer_input = self.view.input_customer_information()
            customer.phone = phone
            customer.first_name = update_customer_input["first_name"]
            customer.last_name = update_customer_input["last_name"]
            customer.corporation = update_customer_input["corporation"]
            customer.updated_at = datetime.now()
            self.session.commit()
        except ValueError as err:
            return self.view.display_error(err)

    def get_customer(self, collaborator: models.Collaborator):
        email = self.view.input_email()
        customer = (
            self.
            session.
            query(models.Customer).
            filter_by(email=email, contact_id=collaborator.id).
            first()
        )
        if customer is None:
            raise ValueError(errors.ERR_COLLABORATOR_NOT_FOUND)
        return customer

    def set_new_customer_email(self):
        email = ""
        while email == "":
            try:
                email_input = self.view.input_email()
                validators.validate_email(email_input)
                self.is_email_in_database(email_input)
                email = email_input
                continue
            except ValueError as err:
                self.view.display_error(err)
                continue
        return email

    def set_customer_phone(self):
        phone = ""
        while phone == "":
            try:
                phone_input= self.view.input_phone_number()
                validators.validate_phone(phone_input)
                phone = phone_input
                continue
            except ValueError as err:
                self.view.display_error(err)
                continue
        return phone

    def is_email_in_database(self, email):
        if (
            self.
            session.
            query(models.Collaborator).
            filter_by(email=email).
            first()
            is not None
        ):
            raise ValueError(errors.ERR_EMAIL_ALREADY_EXISTS)
