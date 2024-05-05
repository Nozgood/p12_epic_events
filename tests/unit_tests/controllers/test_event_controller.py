from unittest import TestCase
from tests.conftest import create_mock_event_controller


class TestEventControllerSetDate(TestCase):
    def setUp(self):
        self.controller = create_mock_event_controller()
