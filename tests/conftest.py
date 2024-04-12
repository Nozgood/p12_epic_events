from unittest.mock import MagicMock
from controllers.main_controller import MainController


def create_mock_main_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()
    mock_collaborator_controller = MagicMock()

    mock_controller = MainController(session=mock_session, view=mock_view)
    mock_controller.collaborator_controller = mock_collaborator_controller
    return mock_controller
