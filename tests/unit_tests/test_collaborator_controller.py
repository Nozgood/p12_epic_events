from unittest import TestCase
from unittest.mock import patch, MagicMock
import models
from tests.conftest import create_mock_collaborator_controller
import utils


class CollaboratorControllerLogin(TestCase):
    def setUp(self):
        self.controller = create_mock_collaborator_controller()

    def test_login_collaborator_not_found(self):
        self.controller.view.input_email.return_value = "notgood@epic.io"
        self.controller.view.input_password.return_value = "notgood"
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter_by.
            return_value.
            first
        ).return_value = None
        with self.assertRaises(ValueError) as error:
            self.controller.login()
            self.assertEqual(
                str(error.exception),
                utils.ERR_COLLABORATOR_NOT_FOUND
            )

    def test_login_not_correct_password(self):
        self.controller.view.input_email.return_value = "test@epic.io"
        self.controller.view.input_password.return_value = "notgoodpw"
        self.controller.is_password_correct = MagicMock(return_value=False)
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter_by.
            return_value.
            first
        ).return_value = models.Collaborator(
            first_name="test",
            last_name="test",
            email="test@epic.io",
            password="goodpw",
            role=models.CollaboratorRole.MANAGEMENT
        )

        with self.assertRaises(ValueError) as error:
            self.controller.login()
            self.assertEqual(
                str(error.exception),
                utils.ERR_COLLABORATOR_NOT_FOUND
            )

    def test_login_normal_behavior(self):
        collaborator_test = models.Collaborator(
            first_name="test",
            last_name="test",
            email="test@epic.io",
            password="goodpw",
            role=models.CollaboratorRole.MANAGEMENT
        )
        self.controller.view.input_email.return_value = "test@epic.io"
        self.controller.view.input_password.return_value = "goodpw"
        self.controller.is_password_correct = MagicMock(return_value=True)
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter_by.
            return_value.
            first
        ).return_value = collaborator_test
        collaborator = self.controller.login()
        self.assertEqual(collaborator, collaborator_test)
        self.assertEqual(collaborator, self.controller.collaborator)
