from unittest import TestCase
from unittest.mock import patch
import models
import utils
from tests.conftest import create_mock_main_controller


class MainControllerRun(TestCase):

    def setUp(self):
        self.controller = create_mock_main_controller()

    def test_run_exit(self):
        self.controller.view.display_main_menu.return_value = 0
        self.controller.run()
        self.controller.view.input_welcome.assert_called_once()
        self.controller.view.input_welcome_user.assert_not_called()

    def test_run_login_raise_exception(self):
        self.controller.view.display_main_menu.side_effect = [1, 0]
        self.controller.collaborator_controller.login.side_effect = ValueError(
            utils.ERR_COLLABORATOR_NOT_FOUND
        )
        with (
            patch.object(self.controller, "get_collaborator_menu")
            as mock_get_collaborator_menu
        ):
            self.controller.run()
            self.controller.view.display_error.assert_called_once()
            mock_get_collaborator_menu.assert_not_called()
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
            patch.object(self.controller, "get_collaborator_menu")
            as mock_get_collaborator_menu
        ):
            self.controller.run()
            self.controller.view.input_welcome.assert_called_once()
            assert self.controller.collaborator is not None
            assert self.controller.view.input_welcome_user()
            mock_get_collaborator_menu.assert_called_once()


class MainControllerCollaboratorMenu(TestCase):

    def setUp(self):
        self.controller = create_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=""
            )

    def test_get_collaborator_exit(self):
        self.controller.view.display_collaborator_menu.return_value = 0
        with (
            patch.object(self.controller, "process_commercial_action")
            as mock_process_commercial_action
        ):
            self.controller.get_collaborator_menu()
            mock_process_commercial_action.assert_not_called()
            self.controller.view.display_collaborator_menu.assert_called_once()

    def test_get_collaborator_menu_management(self):
        self.controller.collaborator.role = models.CollaboratorRole.MANAGEMENT
        self.controller.view.display_collaborator_menu.side_effect = [1, 0]
        with (
            patch.object(self.controller, "process_management_action")
            as mock_process_management_action
        ):
            self.controller.get_collaborator_menu()
            mock_process_management_action.assert_called_once()
            self.assertEqual(
                self.controller.view.display_collaborator_menu.call_count,
                2
            )

    def test_get_collaborator_menu_commercial(self):
        self.controller.collaborator.role = models.CollaboratorRole.COMMERCIAL
        self.controller.view.display_collaborator_menu.side_effect = [1, 0]
        with (
            patch.object(self.controller, "process_commercial_action")
            as mock_process_commercial_action
        ):
            self.controller.get_collaborator_menu()
            mock_process_commercial_action.assert_called_once()
            self.assertEqual(
                self.controller.view.display_collaborator_menu.call_count,
                2
            )

    def test_get_collaborator_menu_support(self):
        self.controller.collaborator.role = models.CollaboratorRole.SUPPORT
        self.controller.view.display_collaborator_menu.side_effect = [1, 0]
        with (
            patch.object(self.controller, "process_support_action")
            as mock_process_support_action
        ):
            self.controller.get_collaborator_menu()
            mock_process_support_action.assert_called_once()
            self.assertEqual(
                self.controller.view.display_collaborator_menu.call_count,
                2
            )

    def test_get_collaborator_menu_admin(self):
        self.controller.collaborator.role = models.CollaboratorRole.ADMIN
        self.controller.view.display_collaborator_menu.side_effect = [1, 0]
        with (
            patch.object(self.controller, "process_admin_action")
            as mock_process_admin_action
        ):
            self.controller.get_collaborator_menu()
            mock_process_admin_action.assert_called_once()
            self.assertEqual(
                self.controller.view.display_collaborator_menu.call_count,
                2
            )


class TestMainControllerManagement(TestCase):
    def setUp(self):
        self.controller = create_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.MANAGEMENT
            )

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

    def test_not_correct_menu_selection(self):
        menu_selection = 99
        self.controller.process_management_action(menu_selection)
        (
            self.controller.view.display_error.assert_called_once()
        )


class TestMainControllerAdmin(TestCase):
    def setUp(self):
        self.controller = create_mock_main_controller()
        self.controller.collaborator = models.Collaborator(
                first_name="test",
                last_name="test",
                password="test",
                email="test@epic.io",
                role=models.CollaboratorRole.ADMIN
            )

    def test_create_collaborator(self):
        menu_selection = 4
        self.controller.process_admin_action(menu_selection)
        (
            self.
            controller.
            collaborator_controller.
            create_collaborator.
            assert_called_once()
        )

    def test_not_correct_menu_selection(self):
        menu_selection = 99
        self.controller.process_management_action(menu_selection)
        (
            self.controller.view.display_error.assert_called_once()
        )
