from unittest import TestCase
from unittest.mock import patch
import validators
import errors
from tests.conftest import new_mock_event_controller
import models
from datetime import datetime


class TestCreateEvent(TestCase):
    def setUp(self):
        self.controller = new_mock_event_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.SUPPORT
        )
        self.customer = models.Customer(
            first_name="test",
            last_name="test",
            email="email@test.io",
            phone_number="+33601010101",
            corporation="test",
            contact=self.controller.collaborator
        )
        self.deal = models.Deal(
            customer=self.customer,
            contact=self.controller.collaborator,
            bill=1000,
            remaining_on_bill=200,
            has_been_signed=True
        )

    def test_create_event_error_session(self):
        error = Exception("unexpected error")
        with patch.object(
            self.controller,
            "set_new_event_period"
        ) as mock_set_new_event_period:
            mock_set_new_event_period.return_value = "01-01-2024", "01-02-2024"
            self.controller.view.input_event_name.return_value = "test"
            self.controller.view.input_event_location.return_value = "lille"
            self.controller.view.input_event_attendees.return_value = 1000
            self.controller.view.input_event_notes.return_value = "enjoy"
            self.controller.session.commit.side_effect = error
            self.controller.create_event(self.customer, self.deal)
            self.controller.session.rollback_assert_called_once()
            self.controller.view.display_error.assert_called_with(error)

    def test_create_event_no_error(self):
        with patch.object(
            self.controller,
            "set_new_event_period"
        ) as mock_set_new_event_period:
            mock_set_new_event_period.return_value = "01-01-2024", "01-02-2024"
            self.controller.view.input_event_name.return_value = "test"
            self.controller.view.input_event_location.return_value = "lille"
            self.controller.view.input_event_attendees.return_value = 1000
            self.controller.view.input_event_notes.return_value = "enjoy"
            self.controller.create_event(self.customer, self.deal)
            (
                self.
                controller.
                view.
                display_new_event_validation.
                assert_called_once()
            )
            self.controller.session.rollback_assert_not_called()
            self.controller.view.display_error.assert_not_called()


class TestUpdateEvent(TestCase):
    def setUp(self):
        self.controller = new_mock_event_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.SUPPORT
        )
        self.customer = models.Customer(
            first_name="test",
            last_name="test",
            email="email@test.io",
            phone_number="+33601010101",
            corporation="test",
            contact=self.controller.collaborator
        )
        self.deal = models.Deal(
            customer=self.customer,
            contact=self.controller.collaborator,
            bill=1000,
            remaining_on_bill=200,
            has_been_signed=True
        )

    def test_update_event_with_both_assigned_and_new_support(self):
        self.controller.update_event(
            self.controller.collaborator,
            models.Collaborator(
                first_name="twotest",
                last_name="testtwo",
                password="testtwo",
                email="testtwo@epic.io",
                role=models.CollaboratorRole.SUPPORT
            )
        )
        self.controller.view.display_error.assert_called_with(
            errors.ERR_UPDATE_EVENT_WITH_TWO_SUPPORT
        )
        self.controller.view.display_event.assert_not_called()

    def test_update_error_getting_event(self):
        error = ValueError(errors.ERR_EVENT_NOT_FOUND)
        with patch.object(
            self.controller,
            "get_event",
            side_effect=error
        ):
            self.controller.update_event(
                support_collaborator=None,
                assigned_support=self.controller.collaborator
            )
            self.controller.view.display_event.assert_not_called()
            self.controller.view.display_error.assert_called_with(error)

    def test_update_event_no_support_assigned(self):
        with patch.object(
            self.controller,
            "get_event",
            return_value=models.Event(
                name="test",
                start_date="01-01-2024",
                end_date="01-02-2024",
                customer=self.customer,
                attendees=1000,
                location="paris",
                deal=self.deal,
                notes="no note"
            )
        ):
            self.controller.update_event(
                support_collaborator=self.controller.collaborator,
                assigned_support=None
            )
        self.controller.session.commit.assert_called_once()
        (
            self.
            controller.
            view.
            display_update_event_validation.
            assert_called_once()
        )
        self.controller.view.display_error.assert_not_called()

    def test_update_event_with_support_already_assigned(self):
        with (patch.object(
            self.controller,
            "get_event",
            return_value=models.Event(
                name="test",
                start_date="01-01-2024",
                end_date="01-02-2024",
                customer=self.customer,
                attendees=1000,
                location="paris",
                deal=self.deal,
                notes="no note"
            )
        )):
            with patch.object(
                self.controller,
                "set_new_event_period"
            ) as mock_set_new_event_period:
                mock_set_new_event_period.return_value = "01-01-2024", "01-03-2024"
                self.controller.view.input_event_location.return_value = "aix"
                self.controller.view.input_event_attendees.return_value = 2000
                self.controller.view.input_event_notes.return_value = ""
                self.controller.update_event(
                    support_collaborator=None,
                    assigned_support=self.controller.collaborator
                )
            self.controller.session.commit.assert_called_once()
            (
                self.
                controller.
                view.
                display_update_event_validation.
                assert_called_once()
            )
            self.controller.view.display_error.assert_not_called()


class TestGetEvent(TestCase):
    def setUp(self):
        self.controller = new_mock_event_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.SUPPORT
        )
        self.customer = models.Customer(
            first_name="test",
            last_name="test",
            email="email@test.io",
            phone_number="+33601010101",
            corporation="test",
            contact=self.controller.collaborator
        )
        self.deal = models.Deal(
            customer=self.customer,
            contact=self.controller.collaborator,
            bill=1000,
            remaining_on_bill=200,
            has_been_signed=True
        )

    def test_get_event_not_found(self):
        self.controller.view.input_event_name.return_value = "test"
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter_by.
            return_value.
            first
        ).return_value = None
        with self.assertRaises(ValueError) as context:
            self.controller.get_event(assigned_support=None)
        self.assertEqual(str(context.exception), errors.ERR_EVENT_NOT_FOUND)

    def test_get_event_no_error_with_assigned_support(self):
        mock_event = models.Event(
                name="test",
                start_date="01-01-2024",
                end_date="01-02-2024",
                customer=self.customer,
                attendees=1000,
                location="paris",
                deal=self.deal,
                notes="no note",
                contact=self.controller.collaborator
            )
        self.controller.view.input_event_name.return_value = "test"
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter_by.
            return_value.
            first
        ).return_value = mock_event
        event = self.controller.get_event(
            assigned_support=self.controller.collaborator
        )
        self.assertEqual(event, mock_event)


class TestListEvents(TestCase):
    def setUp(self):
        self.controller = new_mock_event_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.SUPPORT
        )
        self.customer = models.Customer(
            first_name="test",
            last_name="test",
            email="email@test.io",
            phone_number="+33601010101",
            corporation="test",
            contact=self.controller.collaborator
        )
        self.deal = models.Deal(
            customer=self.customer,
            contact=self.controller.collaborator,
            bill=1000,
            remaining_on_bill=200,
            has_been_signed=True
        )

    def test_list_no_filters(self):
        first_mock_event = models.Event(
                name="test",
                start_date="01-01-2024",
                end_date="01-02-2024",
                customer=self.customer,
                attendees=1000,
                location="paris",
                deal=self.deal,
                notes="no note",
                contact=self.controller.collaborator
            )
        second_mock_event = models.Event(
                name="test2",
                start_date="01-01-2024",
                end_date="01-02-2024",
                customer=self.customer,
                attendees=1000,
                location="paris",
                deal=self.deal,
                notes="no note",
                contact=self.controller.collaborator
            )
        self.controller.view.input_list_events_filters.return_value = 0
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter.
            return_value.
            all
        ).return_value = [
            first_mock_event,
            second_mock_event
        ]
        self.controller.list_events()
        self.assertEqual(
            self.controller.view.display_event.call_count,
            2
        )


class TestSetNewEventPeriod(TestCase):
    def setUp(self):
        self.controller = new_mock_event_controller()

    def test_set_new_event_period_with_initial_failure_then_success(self):
        error = ValueError(errors.ERR_NOT_VALID_PERIOD)
        start_date = datetime(2023, 1, 10)
        end_date_initial = datetime(2023, 1,5)
        end_date = datetime(2023, 1,15)
        with patch.object(
                self.controller,
                'set_new_event_date',
                side_effect=[start_date, end_date_initial, start_date,end_date]
        ) as mock_set_date:
            with patch.object(
                    validators,
                    'validate_period',
                    side_effect=[
                        error,
                        None
                    ]
            ) as mock_validate:
                result_start_date, result_end_date = (
                    self.
                    controller.
                    set_new_event_period()
                )
                self.assertEqual(result_start_date, start_date)
                self.assertEqual(result_end_date, end_date)
                self.assertEqual(mock_validate.call_count, 2)
                self.controller.view.display_error.assert_called_once_with(
                    error
                )
                self.assertEqual(mock_set_date.call_count, 4)