import errors
import models
import views
from datetime import datetime
from sqlalchemy import and_

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
            return self.update_deal(customer)
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

    def update_deal(self, customer: models.Customer):
        try:
            deal_to_manage = self.get_deal(customer)
            self.view.display_deal_informations(deal_to_manage)

            if (
                    deal_to_manage.has_been_signed and
                    deal_to_manage.remaining_on_bill == 0
            ):
                return self.view.display_error(
                    errors.ERR_DEAL_NOTHING_TO_UPDATE
                )

            if not deal_to_manage.has_been_signed:
                deal_to_manage.has_been_signed = self.view.input_deal_signed()

            if deal_to_manage.remaining_on_bill > 0:
                deal_to_manage.remaining_on_bill = (
                    self.
                    view.
                    input_deal_remaining_amount(
                        deal_to_manage.remaining_on_bill,
                        deal_to_manage.bill
                    )
                )
            deal_to_manage.updated_at = datetime.now()

            self.session.commit()
            return self.view.display_update_deal_validation()
        except ValueError as err:
            return self.view.display_error(err)

    def get_deal(self, customer: models.Customer) -> models.Deal:
        deal = (
            self.
            session.
            query(models.Deal).
            filter_by(customer=customer).
            first()
        )
        if deal is None:
            raise ValueError(errors.ERR_DEAL_NOT_FOUND)
        return deal

    def list_deals(self):
        filters_input = self.view.input_list_deals_filters()
        filters = []
        if filters_input == 1:
            filters.append(models.Deal.has_been_signed == False)
        if filters_input == 2:
            filters.append(models.Deal.remaining_on_bill > 0)

        deals = self.session.query(models.Deal).filter(and_(*filters)).all()

        for deal in deals:
            self.view.display_deal_informations(deal)
