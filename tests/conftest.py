from unittest.mock import MagicMock
import controllers


def new_mock_main_controller():
    mock_session = MagicMock()
    mock_console = MagicMock()
    mock_collaborator_controller = MagicMock()
    mock_customer_controller = MagicMock()
    mock_deal_controller = MagicMock()
    mock_event_controller = MagicMock()

    mock_main_controller = controllers.MainController(
        session=mock_session,
        console=mock_console
    )
    mock_main_controller.collaborator_controller = mock_collaborator_controller
    mock_main_controller.customer_controller = mock_customer_controller
    mock_main_controller.deal_controller = mock_deal_controller
    mock_main_controller.event_controller = mock_event_controller

    mock_main_controller.view = MagicMock()
    return mock_main_controller


def new_mock_collaborator_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_collaborator_controller = controllers.CollaboratorController(
        session=mock_session,
        view=mock_view
    )
    mock_collaborator_controller.view = MagicMock()
    return mock_collaborator_controller


def new_mock_customer_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_customer_controller = controllers.CustomerController(
        session=mock_session,
        view=mock_view
    )

    return mock_customer_controller


def new_mock_deal_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_deal_controller = controllers.DealController(
        session=mock_session,
        view=mock_view
    )

    return mock_deal_controller


def new_mock_event_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_event_controller = controllers.EventController(
        session=mock_session,
        view=mock_view
    )
    mock_event_controller.view = MagicMock()
    return mock_event_controller
