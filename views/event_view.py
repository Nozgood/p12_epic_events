import errors
import models
import views
from rich.panel import Panel


class EventView(views.BaseView):

    def display_event(self, event: models.Event):
        return self.console.print(
            f"[input]Name[/]: {event.name} \n"
            f"[input]Start Date[/]: {event.start_date} \n"
            f"[input]End Date[/]: {event.end_date} \n"
            f"[input]Location[/]: {event.location} \n"
            f"[input]Attendees[/]: {event.attendees} \n"
            f"[input]Notes[/]: {event.notes} \n"
            f"[input]Support[/]: {event.contact.email} \n"
            f"[input]Customer[/]: {event.customer.email} \n"
            "--------------- \n"
        )

    def display_new_event_panel(self):
        return self.console.print(
            Panel(
                "--- New Event management ---",
                expand=True
            ),
            style="panel",
            justify="center"
        )

    def input_event_start_date(self):
        self.console.print("Event start date: (DD-MM-YY) ", style="input")
        return input()

    def input_event_end_date(self):
        self.console.print("Event end date: (DD-MM-YY) ", style="input")
        return input()

    def input_event_name(self):
        self.console.print("Event name:", style="input")
        return input()

    def input_event_location(self):
        self.console.print("Event location:", style="input")
        return input()

    def input_event_attendees(self):
        self.console.print("Event attendees:", style="input")
        attendees = 0
        while attendees == 0:
            try:
                attendees = int(input())
                if attendees < 0:
                    attendees = 0
                    self.display_error(errors.ERR_NOT_POSITIVE_VALUE)
                    continue
            except ValueError:
                self.display_error(errors.ERR_NOT_DIGIT_VALUE)
                continue
        return attendees

    def input_event_notes(self):
        self.console.print(
            "A note to add ? (max 200 characters)", style="input"
        )
        return input()

    def input_new_event(self):
        event_name = self.input_event_name()
        event_location = self.input_event_location()
        event_attendees = self.input_event_attendees()
        event_notes = self.input_event_notes()
        return {
            "name": event_name,
            "location": event_location,
            "attendees": event_attendees,
            "notes": event_notes
        }

    def display_new_event_validation(self):
        return self.console.print("New event created", style="success")

    def display_update_event_validation(self):
        return self.console.print("Event correctly updated", style="success")
