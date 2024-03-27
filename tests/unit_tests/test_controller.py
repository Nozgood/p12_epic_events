from unittest import TestCase

from tests.conftest import create_mock_controller


class TestCaseController(TestCase):
    def set_up(self):
        self.controller = create_mock_controller()

    def test_run(self):
        self.set_up()
        self.controller.view.input_menu_selection.return_value = 2

        self.controller.run()
        self.controller.view.input_welcome.assert_called_once()

