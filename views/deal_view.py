import models
import views
import errors


class DealView(views.BaseView):

    def input_deal_management(self):
        self.console.print("[menu_selection]0[/] - Exit")
        self.console.print("[menu_selection]1[/] - Create a new Deal")
        self.console.print("[menu_selection]2[/] - Update a Deal")
        selection = -1
        while selection < 0 or selection > 2:
            try:
                self.console.print("Select an action:", style="input")
                selection = int(input())
                if selection > 2 or selection < 0:
                    raise ValueError
            except ValueError:
                self.console.print(errors.ERR_MENU_INPUT)
        return selection

    def input_deal_amount(self):
        self.console.print("Deal amount:", style="input")
        return input()

    def input_deal_remaining_amount(self, remaining_on_bill, bill):
        self.console.print(
            f"remaining on bill: {remaining_on_bill}",
            style="menu_text"
        )
        self.console.print(
            "Insert the new amount remaining to be paid",
            style="input"
        )
        new_remaining_on_bill = ""
        while new_remaining_on_bill == "":
            try:
                new_remaining_on_bill = int(input())
                if new_remaining_on_bill > bill:
                    self.display_error(errors.ERR_NEW_REMAINING_BILL_TO_BIG)
                    new_remaining_on_bill = ""
                    continue
                continue
            except ValueError:
                self.display_error(errors.ERR_NOT_DIGIT_VALUE)
                continue
        return new_remaining_on_bill

    def input_deal_signed(self):
        self.console.print(
            "Deal already signed ? (-0- if NO / -1- if YES)",
            style="input"
        )
        int_signed = -1
        while int_signed == -1:
            user_input = input()
            if user_input != "0" and user_input != "1":
                self.display_error(errors.ERR_MENU_INPUT)
                continue
            int_signed = user_input
            continue
        if int_signed == "0":
            return False
        return True

    def input_new_deal(self):
        bill_input = self.input_deal_amount()
        has_been_signed_input = self.input_deal_signed()
        return {
            "bill": bill_input,
            "has_been_signed": has_been_signed_input
        }

    def display_deal_informations(self, deal: models.Deal):
        return self.console.print(
            f"[input]Customer[/]: "
            f"{deal.customer.first_name} "
            f"{deal.customer.last_name} \n"
            f"[input]Contact[/]: "
            f"{deal.contact.first_name} "
            f"{deal.contact.last_name} \n"
            f"[input]Has Been signed[/]: {deal.has_been_signed} \n"
            f"[input]Remaining on Bill[/]: {deal.remaining_on_bill} \n"
            f"[input]Created at[/]: {deal.created_at} \n"
        )

    def input_list_deals_filters(self):
        self.console.print("[input] -- List Deals Filters --")
        self.console.print("[menu_selection]0[/] - No filters")
        self.console.print("[menu_selection]1[/] - Deals not signed")
        self.console.print("[menu_selection]2[/] - Deals not totally paid")
        list_deal_filter = ""
        while list_deal_filter == "":
            try:
                list_deal_filter = int(input())
                if list_deal_filter < 0 or list_deal_filter > 2:
                    list_deal_filter = ""
                    self.display_error(errors.ERR_MENU_INPUT)
                    continue
                continue
            except ValueError:
                self.display_error(errors.ERR_NOT_DIGIT_VALUE)
                continue
        return list_deal_filter

    def display_new_deal_validation(self):
        return self.console.print("Deal successfully created", style="success")

    def display_update_deal_validation(self):
        return self.console.print("Deal successfully updated", style="success")
