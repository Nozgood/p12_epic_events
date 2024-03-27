from unittest.mock import MagicMock
from controllers.controller import Controller


def create_mock_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_controller = Controller(session=mock_session, view=mock_view)
    return mock_controller
