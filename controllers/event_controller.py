import errors
import models
import views
from datetime import datetime


class EventController:
    def __init__(self, session, view: views.EventView, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def create_event(self, customer: models.Customer, deal: models.Deal):
        self.view.display_new_event_panel()
        new_event = models.Event(
            name=self.view.input_event_name(),
            start_date=self.set_new_event_date(is_start_date=True),
            end_date=self.set_new_event_date(is_start_date=False),
            location=self.view.input_event_location(),
            attendees=self.view.input_event_attendees(),
            notes=self.view.input_event_notes(),
            customer=customer,
            deal=deal
        )
        try:
            self.session.add(new_event)
            self.session.commit()
            return self.view.display_new_event_validation()
        except Exception as err:
            self.session.rollback()
            return self.view.display_error(err)

    def set_new_event_date(self, is_start_date):
        date_format = "%d-%m-%y"
        new_date = ""
        while new_date == "":
            if is_start_date:
                new_date_input = self.view.input_event_start_date()
            else:
                new_date_input = self.view.input_event_end_date()
            try:
                new_date = datetime.strptime(new_date_input, date_format)
                continue
            except ValueError as err:
                self.view.display_error(err)
                continue
        return new_date
