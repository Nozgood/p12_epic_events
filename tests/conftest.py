from unittest.mock import MagicMock
import controllers


def create_mock_main_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()
    mock_collaborator_controller = MagicMock()

    mock_main_controller = controllers.MainController(
        session=mock_session,
        view=mock_view
    )
    mock_main_controller.collaborator_controller = mock_collaborator_controller
    return mock_main_controller


def create_mock_collaborator_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    return controllers.CollaboratorController(
        session=mock_session,
        view=mock_view
    )
