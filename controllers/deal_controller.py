import models
import views


class DealController:
    def __init__(self, session, view: views.DealView, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def manage_deals(self, customer: models.Customer):
        menu_selection = self.view.input_deal_management()
        if menu_selection == 1:
            return self.create_deal(customer)
        if menu_selection == 2:
            pass
        return

    def create_deal(self, customer: models.Customer):
        input_new_deal = self.view.input_new_deal()
        deal = models.Deal(
            customer=customer,
            contact=customer.contact,
            bill=input_new_deal["bill"],
            remaining_on_bill=input_new_deal["bill"],
            has_been_signed=input_new_deal["has_been_signed"]
        )
        self.session.add(deal)
        self.session.commit()
        return self.view.display_new_deal_validation()
