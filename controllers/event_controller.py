import errors
import models
import validators
import views
from datetime import datetime
from sqlalchemy import and_


class EventController:
    def __init__(self, session, view: views.EventView, collaborator=None):
        self.session = session
        self.view = view
        self.collaborator = collaborator

    def create_event(self, customer: models.Customer, deal: models.Deal):
        self.view.display_new_event_panel()
        start_date, end_date = self.set_new_event_period()

        new_event = models.Event(
            name=self.view.input_event_name(),
            start_date=start_date,
            end_date=end_date,
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

    def update_event(self, support_collaborator=None, assigned_support=None):
        """
        update an existing event based on the new provided information

        :param support_collaborator: a support to assign to the event as contact
        :param assigned_support: the support that is already assigned to the
        event as contact to filter by this support
        :return: a validation message print in the console
        """
        if support_collaborator is not None and assigned_support is not None:
            return self.view.display_error(
                errors.ERR_UPDATE_EVENT_WITH_TWO_SUPPORT
            )
        try:
            event_to_update = self.get_event(assigned_support)
            self.view.display_event(event_to_update)
            if support_collaborator is not None:
                event_to_update.contact = support_collaborator
            else:
                start_date, end_date = self.set_new_event_period()
                event_to_update.location = self.view.input_event_location()
                event_to_update.attendees = self.view.input_event_attendees()
                event_to_update.notes = self.view.input_event_notes()
                event_to_update.start_date = start_date
                event_to_update.end_date = end_date
            self.session.commit()
            return self.view.display_update_event_validation()
        except ValueError as err:
            self.view.display_error(err)

    def get_event(
            self,
            assigned_support: models.Collaborator = None
    ) -> models.Event:
        event_name = self.view.input_event_name()
        filters = {
            "name": event_name
        }
        if assigned_support is not None:
            filters["contact"] = assigned_support
        event = (
            self.
            session.
            query(models.Event).
            filter_by(**filters).
            first()
        )
        if event is None:
            raise ValueError(errors.ERR_EVENT_NOT_FOUND)
        return event

    def list_events(self):
        event_filters_input = self.view.input_list_events_filters()
        filters = []
        if event_filters_input == 1:
            filters.append(models.Event.contact == self.collaborator)
        if event_filters_input == 2:
            filters.append(models.Event.contact_id is None)
        events = (
            self.
            session.
            query(models.Event).
            filter(and_(True, *filters)).
            all()
        )
        for event in events:
            self.view.display_event(event)

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

    def set_new_event_period(self):
        start_date = None
        end_date = None
        while start_date is None and end_date is None:
            try:
                start_date = self.set_new_event_date(is_start_date=True)
                end_date = self.set_new_event_date(is_start_date=False)
                validators.validate_period(start_date, end_date)
                continue
            except ValueError as err:
                self.view.display_error(err)
                start_date = None
                end_date = None
                continue
        return start_date, end_date
