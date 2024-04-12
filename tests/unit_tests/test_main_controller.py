from unittest import TestCase
from unittest.mock import patch

import models
from tests.conftest import create_mock_main_controller


class TestCaseController(TestCase):

    def set_up(self):
        self.controller = create_mock_main_controller()

    def test_run_exit(self):
        self.set_up()
        self.controller.view.display_main_menu.return_value = 0
        self.controller.run()
        self.controller.view.input_welcome.assert_called_once()

    def test_run_login_no_error(self):
        self.set_up()
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
