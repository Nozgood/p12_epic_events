from unittest import TestCase
from tests.conftest import new_mock_event_controller


class TestEventControllerSetDate(TestCase):
    def setUp(self):
        self.controller = new_mock_event_controller()
