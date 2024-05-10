import unittest
from unittest import TestCase
from unittest.mock import patch
import models
import errors
from tests.conftest import new_mock_main_controller


class MainControllerRun(TestCase):

    def setUp(self):
        self.controller = new_mock_main_controller()

    def test_run_not_valid_input(self):
        self.controller.view.display_main_menu.side_effect = [99,0]
        self.controller.run()
        self.controller.view.display_error.assert_called_once()

    def test_run_exit(self):
        self.controller.view.display_main_menu.return_value = 0
        self.controller.run()
        self.controller.view.input_welcome.assert_called_once()
        self.controller.view.input_welcome_user.assert_not_called()

    def test_run_login_raise_exception(self):
        self.controller.view.display_main_menu.side_effect = [1, 0]
        self.controller.collaborator_controller.login.side_effect = ValueError(
            errors.ERR_COLLABORATOR_NOT_FOUND
        )
        with (
            patch.object(self.controller, "get_collaborator_main_menu")
            as mock_get_collaborator_main_menu
        ):
            self.controller.run()
            self.controller.view.display_error.assert_called_once()
            mock_get_collaborator_main_menu.assert_not_called()
            self.controller.view.input_welcome.assert_called_once()

    def test_run_login_no_error(self):
        self.controller.view.display_main_menu.side_effect = [1, 0]
        self.controller.view.display_collaborator_menu.return_value = 0
        self.controller.collaborator_controller.login.return_value = (
            models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.MANAGEMENT
            )
        )

        with (
            patch.object(self.controller, "get_collaborator_main_menu")
            as mock_get_collaborator_main_menu
        ):
            self.controller.run()
            self.controller.view.input_welcome.assert_called_once()
            assert self.controller.collaborator is not None
            assert self.controller.view.input_welcome_user()
            mock_get_collaborator_main_menu.assert_called_once()


class MainControllerCollaboratorMenu(TestCase):

    def setUp(self):
        self.controller = new_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=""
            )

    def test_get_collaborator_main_menu_exit(self):
        self.controller.collaborator_controller.view.display_collaborator_menu.return_value = 0
        with (
            patch.object(self.controller, "process_commercial_action")
            as mock_process_commercial_action
        ):
            self.controller.get_collaborator_main_menu()
            mock_process_commercial_action.assert_not_called()
            self.controller.collaborator_controller.view.display_collaborator_menu.assert_called_once()

    def test_get_collaborator_main_menu_management(self):
        self.controller.collaborator.role = models.CollaboratorRole.MANAGEMENT
        self.controller.collaborator_controller.view.display_collaborator_menu.side_effect = [1, 0]
        with (
            patch.object(self.controller, "process_management_action")
            as mock_process_management_action
        ):
            self.controller.get_collaborator_main_menu()
            mock_process_management_action.assert_called_once()
            self.assertEqual(
                self.
                controller.
                collaborator_controller.
                view.
                display_collaborator_menu.
                call_count,
                2
            )

    def test_get_collaborator_main_menu_commercial(self):
        self.controller.collaborator.role = models.CollaboratorRole.COMMERCIAL
        self.controller.collaborator_controller.view.display_collaborator_menu.side_effect = [1, 0]
        with (
            patch.object(self.controller, "process_commercial_action")
            as mock_process_commercial_action
        ):
            self.controller.get_collaborator_main_menu()
            mock_process_commercial_action.assert_called_once()
            self.assertEqual(
                self.controller.collaborator_controller.view.display_collaborator_menu.call_count,
                2
            )

    def test_get_collaborator_main_menu_support(self):
        self.controller.collaborator.role = models.CollaboratorRole.SUPPORT
        self.controller.collaborator_controller.view.display_collaborator_menu.side_effect = [1, 0]
        with (
            patch.object(self.controller, "process_support_action")
            as mock_process_support_action
        ):
            self.controller.get_collaborator_main_menu()
            mock_process_support_action.assert_called_once()
            self.assertEqual(
                self.
                controller.
                collaborator_controller.
                view.
                display_collaborator_menu.
                call_count,
                2
            )


class TestMainControllerManagement(TestCase):
    def setUp(self):
        self.controller = new_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.MANAGEMENT
            )

    def test_list_customers(self):
        menu_selection = 1
        self.controller.process_management_action(menu_selection)
        self.controller.customer_controller.list_customers.assert_called_once()

    def test_list_deals(self):
        menu_selection = 2
        self.controller.process_management_action(menu_selection)
        self.controller.deal_controller.list_deals.assert_called_once()

    def test_list_events(self):
        menu_selection = 3
        self.controller.process_management_action(menu_selection)
        self.controller.event_controller.list_events.assert_called_once()

    def test_assign_support_on_event(self):
        menu_selection = 4
        with patch.object(
                self.controller,
                "set_support_on_event"
        ) as mock_set_support_on_event:
            self.controller.process_management_action(menu_selection)
            mock_set_support_on_event.assert_called_once()

    def test_manage_collaborators(self):
        menu_selection = 5
        self.controller.process_management_action(menu_selection)
        (
            self.
            controller.
            collaborator_controller.
            manage_collaborators.
            assert_called_once()
        )

    def test_manage_deal_for_customer(self):
        menu_selection = 6
        with patch.object(
            self.controller,
            "manage_deal_for_customer"
        ) as mock_manage_deal_for_customer:
            self.controller.process_management_action(menu_selection)
            mock_manage_deal_for_customer.assert_called_once()

    def test_not_correct_menu_selection(self):
        menu_selection = 99
        self.controller.process_management_action(menu_selection)
        (
            self.controller.view.display_error.assert_called_once()
        )


class TestManageDealForCustomer(unittest.TestCase):
    def setUp(self):
        self.controller = new_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.MANAGEMENT
            )

    def test_customer_not_found(self):
        self.controller.customer_controller.get_customer.side_effect = (
            ValueError(errors.ERR_CUSTOMER_NOT_FOUND)
        )
        self.controller.manage_deal_for_customer()
        self.controller.view.display_error.assert_called_once()

    def test_normal_behavior(self):
        self.controller.customer_controller.get_customer.return_value = models.Customer(
                first_name="test",
                last_name="test",
                email="test@test.io",
                corporation="test",
                phone_number="+33601010101",
                contact=None
            )
        self.controller.manage_deal_for_customer()
        self.controller.deal_controller.manage_deals.assert_called_once()
        self.controller.view.display_error.assert_not_called()


class TestSetSupportOnEvent(unittest.TestCase):
    def setUp(self):
        self.controller = new_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.MANAGEMENT
            )

    def test_support_not_found(self):
        self.controller.collaborator_controller.get_collaborator.side_effect = (
            ValueError(errors.ERR_COLLABORATOR_NOT_FOUND)
        )
        self.controller.set_support_on_event()
        self.controller.view.display_error.assert_called_once()

    def test_collaborator_not_support(self):
        self.controller.collaborator_controller.get_collaborator.return_value = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.MANAGEMENT
            )
        self.controller.set_support_on_event()
        self.controller.view.display_error.assert_called_once()

    def test_normal_behavior(self):
        self.controller.collaborator_controller.get_collaborator.return_value = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.SUPPORT
            )
        self.controller.set_support_on_event()
        self.controller.event_controller.update_event.assert_called_once()
        self.controller.view.display_error.assert_not_called()


class TestProcessCommercialAction(unittest.TestCase):
    def setUp(self):
        self.controller = new_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.MANAGEMENT
        )

    def test_list_customers(self):
        menu_selection = 1
        self.controller.process_commercial_action(menu_selection)
        self.controller.customer_controller.list_customers.assert_called_once()
        self.controller.view.display_error.assert_not_called()

    def test_list_deals(self):
        menu_selection = 2
        self.controller.process_commercial_action(menu_selection)
        self.controller.deal_controller.list_deals.assert_called_once()
        self.controller.view.display_error.assert_not_called()

    def test_list_events(self):
        menu_selection = 3
        self.controller.process_commercial_action(menu_selection)
        self.controller.event_controller.list_events.assert_called_once()
        self.controller.view.display_error.assert_not_called()

    def test_create_customer(self):
        menu_selection = 4
        self.controller.process_commercial_action(menu_selection)
        self.controller.customer_controller.create_customer.assert_called_once()
        self.controller.view.display_error.assert_not_called()

    def test_update_customer(self):
        menu_selection = 5
        self.controller.process_commercial_action(menu_selection)
        self.controller.customer_controller.update_customer.assert_called_once()
        self.controller.view.display_error.assert_not_called()

    def test_update_deal_for_customer(self):
        menu_selection = 6
        with patch.object(
            self.controller,
            "update_customer_deal_by_commercial"
        ) as mock_update_customer_deal_by_commercial:
            self.controller.process_commercial_action(menu_selection)
            mock_update_customer_deal_by_commercial.assert_called_once()
            self.controller.view.display_error.assert_not_called()

    def test_create_event_for_customer(self):
        menu_selection = 7
        with patch.object(
            self.controller,
            "create_event_for_customer_by_commercial"
        ) as mock_create_event:
            self.controller.process_commercial_action(menu_selection)
            mock_create_event.assert_called_once()
            self.controller.view.display_error.assert_not_called()
