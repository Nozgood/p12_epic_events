from unittest import TestCase
from unittest.mock import patch, MagicMock
import models
from tests.conftest import new_mock_collaborator_controller
import errors
import validators


class CollaboratorControllerLogin(TestCase):
    def setUp(self):
        self.controller = new_mock_collaborator_controller()

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
                errors.ERR_COLLABORATOR_NOT_FOUND
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
                errors.ERR_COLLABORATOR_NOT_FOUND
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


class CollaboratorControllerManageCollaborators(TestCase):
    def setUp(self):
        self.controller = new_mock_collaborator_controller()

    def test_manage_collaborators_not_good_input(self):
        self.controller.view.input_collaborator_management.return_value = 4
        self.controller.manage_collaborators()
        self.controller.view.display_error.assert_called_once()

    def test_back_action(self):
        self.controller.view.input_collaborator_management.return_value = 0
        with patch.object(
                self.controller,
                'create_collaborator'
        ) as mock_create:
            with patch.object(
                    self.controller,
                    'update_collaborator'
            ) as mock_update:
                with patch.object(
                        self.controller,
                        'delete_collaborator'
                ) as mock_delete:
                    self.controller.manage_collaborators()
                    mock_create.assert_not_called()
                    mock_update.assert_not_called()
                    mock_delete.assert_not_called()
                    self.controller.view.display_error.assert_not_called()

    def test_manage_collaborators_create(self):
        self.controller.view.input_collaborator_management.return_value = 1
        with patch.object(
                self.controller,
                "create_collaborator"
        ) as mock_create_collaborator:
            self.controller.manage_collaborators()
            mock_create_collaborator.assert_called_once()

    def test_manage_collaborators_update(self):
        self.controller.view.input_collaborator_management.return_value = 2
        with patch.object(
                self.controller,
                "update_collaborator"
        ) as mock_update_collaborator:
            self.controller.manage_collaborators()
            mock_update_collaborator.assert_called_once()

    def test_manage_collaborators_delete(self):
        self.controller.view.input_collaborator_management.return_value = 3
        with patch.object(
                self.controller,
                "delete_collaborator"
        ) as mock_delete_collaborator:
            self.controller.manage_collaborators()
            mock_delete_collaborator.assert_called_once()


class TestCollaboratorControllerCRUD(TestCase):
    def setUp(self):
        self.controller = new_mock_collaborator_controller()

    def test_create_email_normal_behavior(self):
        self.controller.view.input_email.return_value = "good@epic.io"
        self.controller.view.input_password.return_value = "password"
        self.controller.is_email_in_database = MagicMock(return_value=False)
        self.controller.view.input_new_collaborator.return_value = {
            "first_name": "test",
            "last_name": "test",
            "role": models.CollaboratorRole.MANAGEMENT
        }
        self.controller.create_collaborator()
        self.controller.session.add.assert_called_once()
        self.controller.session.commit.assert_called_once()
        (
            self.
            controller.
            view.
            display_new_collaborator_validation.
            assert_called_once()
        )
        self.controller.view.display_error.assert_not_called()

    def test_get_collaborator_not_good_email(self):
        self.controller.view.input_email.return_value = "notgood@epic.io"
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
        with self.assertRaises(ValueError) as err:
            self.controller.get_collaborator()
        self.assertEqual(str(err.exception), errors.ERR_COLLABORATOR_NOT_FOUND)

    def test_get_collaborator_normal_behavior(self):
        expected = models.Collaborator(
            email="good@epic.io",
            first_name="test",
            last_name="test",
            password="test",
            role=models.CollaboratorRole.MANAGEMENT
        )
        self.controller.view.input_email.return_value = "good@epic.io"
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter_by.
            return_value.
            first
        ).return_value = expected
        collaborator = self.controller.get_collaborator()
        self.assertEqual(expected, collaborator)

    def test_update_collaborator_not_valid(self):
        with patch.object(
                self.controller,
                "get_collaborator"
        ) as mock_get_collaborator:
            mock_get_collaborator.side_effect = ValueError
            self.controller.update_collaborator()
            (
                self.
                controller.
                view.
                display_collaborator_information.
                assert_not_called()
            )

    def test_update_collaborator_normal_behavior(self):
        collaborator_not_updated = models.Collaborator(
                email="good@epic.io",
                first_name="test",
                last_name="test",
                password="test",
                role=models.CollaboratorRole.MANAGEMENT
            )
        with patch.object(
                self.controller,
                "get_collaborator"
        ) as mock_get_collaborator:
            mock_get_collaborator.return_value = collaborator_not_updated
            self.controller.view.input_update_collaborator.return_value = {
                "first_name": "update_test",
                "last_name": "update_test",
                "email": "good@epic.io",
                "role": models.CollaboratorRole.SUPPORT
            }
            self.controller.update_collaborator()
            self.controller.session.commit.assert_called_once()
            (
                self.
                controller.
                view.
                display_collaborator_information.
                assert_called_once()
            )
            (
                self.
                controller.
                view.
                display_update_collaborator_validation.
                assert_called_once()
            )

    def test_delete_collaborator_error(self):
        with patch.object(
                self.controller,
                "get_collaborator"
        ) as mock_get_collaborator:
            mock_get_collaborator.side_effect = ValueError
            self.controller.delete_collaborator()
            self.controller.session.delete.assert_not_called()

    def test_delete_collaborator_valid(self):
        collaborator = models.Collaborator(
                email="good@epic.io",
                first_name="test",
                last_name="test",
                password="test",
                role=models.CollaboratorRole.MANAGEMENT
            )
        with patch.object(
                self.controller,
                "get_collaborator"
        ) as mock_get_collaborator:
            mock_get_collaborator.return_value = collaborator
            self.controller.delete_collaborator()
            self.controller.session.delete.assert_called_once()
            self.controller.session.commit.assert_called_once()
            (
                self.
                controller.
                view.
                display_delete_collaborator_validation.
                assert_called_once()
            )


class TestSetNewCollaboratorEmail(TestCase):

    def setUp(self):
        self.controller = new_mock_collaborator_controller()

    def test_set_new_collaborator_email_with_error_then_success(self):
        error = ValueError(errors.ERR_NOT_VALID_EMAIl)
        with patch.object(
                self.controller.view,
                'input_email',
                side_effect=['invalid_email', 'valid_email@domain.com']
        ):
            with patch.object(
                    self.controller,
                    'is_email_in_database',
                    side_effect=[None]
            ):
                with patch.object(
                        validators,
                        'validate_email',
                        side_effect=[error, None]
                ):
                    result = self.controller.set_new_collaborator_email()
                    self.controller.view.display_error.assert_called_once_with(
                        error
                    )
                    self.assertEqual(result, 'valid_email@domain.com')

    def test_set_new_collaborator_password_with_error_then_success(self):
        error = ValueError(errors.ERR_NOT_VALID_PASSWORD)
        with patch.object(
                self.controller.view,
                'input_password',
                side_effect=['weak', 'StrongPassword123']
        ):
            with patch.object(
                    validators,
                    'validate_password',
                    side_effect=[error, None]
            ):
                result = self.controller.set_new_collaborator_password()
                self.controller.view.display_error.assert_called_once_with(
                        error
                )
                self.assertEqual(result, 'StrongPassword123')
