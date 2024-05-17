from unittest import TestCase
from tests.conftest import new_mock_customer_controller
from unittest.mock import patch
import models
import errors
import validators
class TestCreateCustomer(TestCase):

    def setUp(self):
        self.controller = new_mock_customer_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )

    def test_create_customer_error_session_commit(self):
        with patch.object(
            self.controller,
            "set_new_customer_email",
            side_effect="test@test.io"
        ):
            with patch.object(
                self.controller,
                "set_customer_phone",
                side_effect="+33601010101"
            ):
                self.controller.view.input_customer_information.return_value = (
                    {
                        "first_name": "first_name",
                        "last_name": "last_name",
                        "corporation": "corporation"
                    }
                )
                self.controller.session.commit.side_effect = ValueError("error")
                self.controller.create_customer()
                self.controller.session.add.assert_called_once()
                (
                    self.
                    controller.
                    view.
                    display_new_customer_validation.
                    assert_not_called()
                )
                self.controller.view.display_error.assert_called_once()
                self.controller.session.rollback.assert_called_once()

    def test_create_customer_normal_behavior(self):
        with patch.object(
            self.controller,
            "set_new_customer_email",
            side_effect="test@test.io"
        ):
            with patch.object(
                self.controller,
                "set_customer_phone",
                side_effect="+33601010101"
            ):
                self.controller.view.input_customer_information.return_value = (
                    {
                        "first_name": "first_name",
                        "last_name": "last_name",
                        "corporation": "corporation"
                    }
                )
                self.controller.create_customer()
                self.controller.session.add.assert_called_once()
                (
                    self.
                    controller.
                    view.
                    display_new_customer_validation.
                    assert_called_once()
                )
                self.controller.session.commit.assert_called_once()
                self.controller.view.display_error.assert_not_called()
                self.controller.session.rollback.assert_not_called()


class TestUpdateCustomer(TestCase):
    def setUp(self):
        self.controller = new_mock_customer_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )

    def test_update_customer_customer_not_found(self):
        error = ValueError(errors.ERR_CUSTOMER_NOT_FOUND)
        with patch.object(
            self.controller,
            "get_customer",
            side_effect=error
        ):
            self.controller.update_customer()
            (
                self.
                controller.
                view.
                display_customer_information.
                assert_not_called()
            )
            self.controller.view.display_error.assert_called_once()

    def test_normal_behavior(self):
        with patch.object(
            self.controller,
            "get_customer",
            return_value=models.Customer(
                first_name="first_name",
                last_name="last_name",
                email="email@email.io",
                phone_number="+33601010101",
                corporation="corporation",
                contact=self.controller.collaborator
            )
        ):
            with patch.object(
                self.controller,
                "set_customer_phone",
                side_effect="+33601010102"
            ):
                self.controller.update_customer()
                self.controller.session.commit.assert_called_once()
                self.controller.view.display_error.assert_not_called()


class TestGetCustomer(TestCase):
    def setUp(self):
        self.controller = new_mock_customer_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )

    def test_customer_not_found_with_no_collaborator(self):
        self.controller.view.input_email.return_value = "email@test.io"
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

        with self.assertRaises(ValueError) as context:
            self.controller.get_customer()
        self.assertEqual(str(context.exception), errors.ERR_CUSTOMER_NOT_FOUND)

    def test_get_customer_with_collaborator(self):
        mock_collaborator = models.Collaborator(
            first_name="ok",
            last_name="ok",
            password="ok",
            email="test@ok.io",
            role=models.CollaboratorRole.COMMERCIAL
        )

        mock_collaborator.id = "1"

        self.controller.view.input_email.return_value = 'john@example.com'
        (
            self.
            controller.
            session.
            query.
            return_value.
            filter_by.
            return_value.
            first
        ).return_value = models.Customer(
                first_name="first_name",
                last_name="last_name",
                email="john@example.com",
                phone_number="+33601010101",
                corporation="corporation",
                contact=models.Collaborator(
                    first_name="ok",
                    last_name="ok",
                    password="ok",
                    email="test@ok.io",
                    role=models.CollaboratorRole.COMMERCIAL
                )
            )

        customer = self.controller.get_customer(mock_collaborator)
        self.assertEqual(customer.email, 'john@example.com')


class TestListCustomers(TestCase):
    def setUp(self):
        self.controller = new_mock_customer_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )

    def test_no_customer(self):
        self.controller.session.query.return_value.all.return_value = []
        self.controller.list_customers()
        self.controller.view.display_customer_information.assert_not_called()
        self.controller.view.display_error.assert_called_with(
            errors.ERR_NO_CUSTOMER_TO_LIST
        )

    def test_normal_behavior(self):
        self.controller.session.query.return_value.all.return_value = [
            models.Customer(
                first_name="first_name",
                last_name="last_name",
                email="john@example.com",
                phone_number="+33601010101",
                corporation="corporation",
                contact=models.Collaborator(
                    first_name="ok",
                    last_name="ok",
                    password="ok",
                    email="test@ok.io",
                    role=models.CollaboratorRole.COMMERCIAL
                )
            ),
            models.Customer(
                first_name="first_name",
                last_name="last_name",
                email="johnokok@example.com",
                phone_number="+33601010201",
                corporation="corporation",
                contact=models.Collaborator(
                    first_name="ok",
                    last_name="ok",
                    password="ok",
                    email="test@ok.io",
                    role=models.CollaboratorRole.COMMERCIAL
                )
            )
        ]
        self.controller.list_customers()
        self.assertEqual(
            self.controller.view.display_customer_information.call_count,
            2
        )


class TestSetCustomerPhone(TestCase):
    def setUp(self):
        self.controller = new_mock_customer_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )

    def test_set_customer_phone_with_retry(self):
        error = ValueError(errors.ERR_NOT_VALID_PHONE)
        with patch.object(
                self.controller.view,
                'input_phone_number',
                side_effect=["123", "+33601010101"]
        ):
            with patch.object(
                    validators,
                    'validate_phone'
            ) as mock_validate_phone:
                mock_validate_phone.side_effect = [error, None]
                phone = self.controller.set_customer_phone()
                self.assertEqual(mock_validate_phone.call_count, 2)
                self.controller.view.display_error.assert_called_once_with(
                    error
                )
                self.assertEqual(phone, "+33601010101")


class TestSetNewCustomerEmail(TestCase):
    def setUp(self):
        self.controller = new_mock_customer_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )

    def test_set_new_customer_email_with_retry(self):
        error = ValueError(errors.ERR_NOT_VALID_EMAIl)
        with patch.object(
            self.controller.view,
            "input_email",
            side_effect=["test", "test@gmail.io"]
        ):
            with patch.object(
                    validators,
                    'validate_email'
            ) as mock_validate_email:
                with patch.object(
                        self.controller,
                    "is_email_in_database",
                    return_value=True
                ):
                    mock_validate_email.side_effect = [error, None]
                    email = self.controller.set_new_customer_email()
                    self.assertEqual(mock_validate_email.call_count, 2)
                    self.controller.view.display_error.assert_called_once_with(
                        error
                    )
                    self.assertEqual(email, "test@gmail.io")
