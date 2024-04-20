from unittest.mock import MagicMock
import controllers


def create_mock_main_controller():
    mock_session = MagicMock()
    mock_console = MagicMock()
    mock_collaborator_controller = MagicMock()

    mock_main_controller = controllers.MainController(
        session=mock_session,
        console=mock_console
    )
    mock_main_controller.collaborator_controller = mock_collaborator_controller
    mock_main_controller.view = MagicMock()
    return mock_main_controller


def create_mock_collaborator_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_collaborator_controller = controllers.CollaboratorController(
        session=mock_session,
        view=mock_view
    )
    mock_collaborator_controller.view = MagicMock()
    return mock_collaborator_controller
