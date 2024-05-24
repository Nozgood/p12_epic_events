from unittest import TestCase

import errors
import models
from tests.conftest import new_mock_deal_controller
from unittest.mock import patch


class TestManageDeals(TestCase):

    def setUp(self):
        self.controller = new_mock_deal_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )
        self.customer = models.Customer(
            first_name="test",
            last_name="test",
            email="email@test.io",
            phone_number="+33601010101",
            corporation="test",
            contact=self.controller.collaborator
        )

    def test_cancel_input(self):
        self.controller.view.input_deal_management.return_value = 0
        with patch.object(
            self.controller,
            "create_deal"
        ) as mock_create_deal:
            with patch.object(
                self.controller,
                "update_deal"
            ) as mock_update_deal:
                self.controller.manage_deals(self.customer)
                mock_create_deal.assert_not_called()
                mock_update_deal.assert_not_called()
                self.controller.view.display_error.assert_not_called()

    def test_create_deal_input(self):
        self.controller.view.input_deal_management.return_value = 1
        with patch.object(
                self.controller,
                "create_deal"
        ) as mock_create_deal:
            self.controller.manage_deals(self.customer)
            mock_create_deal.assert_called_once()
            self.controller.view.display_error.assert_not_called()

    def test_update_deal_input(self):
        self.controller.view.input_deal_management.return_value = 2
        with patch.object(
            self.controller,
            "update_deal"
        ) as mock_update_deal:
            self.controller.manage_deals(self.customer)
            mock_update_deal.assert_called_once()
            self.controller.view.display_error.assert_not_called()

    def test_not_correct_input_not_triggered_by_view(self):
        self.controller.view.input_deal_management.return_value = 99
        self.controller.manage_deals(self.customer)
        self.controller.view.display_error.assert_called_with(
            errors.ERR_MENU_INPUT
        )


class TestCreateDeal(TestCase):
    def setUp(self):
        self.controller = new_mock_deal_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )
        self.customer = models.Customer(
            first_name="test",
            last_name="test",
            email="email@test.io",
            phone_number="+33601010101",
            corporation="test",
            contact=self.controller.collaborator
        )

    def test_create_deal_error_session_commit(self):
        error = Exception("error session")
        self.controller.view.input_new_deal.return_value = {
            "bill": 1000,
            "has_been_signed": False
        }
        self.controller.session.commit.side_effect = error
        self.controller.create_deal(self.customer)
        self.controller.view.display_new_deal_validation.assert_not_called()
        self.controller.session.rollback_assert_called_once()
        self.controller.view.display_error.assert_called_with(error)

    def test_create_deal_normal_behavior(self):
        self.controller.view.input_new_deal.return_value = {
            "bill": 1000,
            "has_been_signed": False
        }
        self.controller.create_deal(self.customer)
        self.controller.session.rollback_assert_not_called()
        self.controller.view.display_error.assert_not_called()
        self.controller.view.display_new_deal_validation.assert_called_once()


class TestUpdateDeal(TestCase):
    def setUp(self):
        self.controller = new_mock_deal_controller()
        self.controller.collaborator = models.Collaborator(
            first_name="test",
            last_name="test",
            password="test",
            email="test@epic.io",
            role=models.CollaboratorRole.COMMERCIAL
        )
        self.customer = models.Customer(
            first_name="test",
            last_name="test",
            email="email@test.io",
            phone_number="+33601010101",
            corporation="test",
            contact=self.controller.collaborator
        )

    def test_update_deal_not_found(self):
        error = ValueError(errors.ERR_DEAL_NOT_FOUND)
        with patch.object(
            self.controller,
            "get_deal",
            side_effect=error
        ):
            self.controller.update_deal(self.customer)
            self.controller.session.commit.assert_not_called()
            self.controller.view.display_error.assert_called_with(error)

    def test_update_deal_error_commit_session(self):
        error = Exception("error")
        with patch.object(
            self.controller,
            "get_deal",
            return_value=models.Deal(
                customer=self.customer,
                contact=self.customer.contact,
                bill=1000,
                remaining_on_bill=0,
                has_been_signed=False
            )
        ):
            self.controller.session.commit.side_effect = error
            self.controller.update_deal(self.customer)
            self.controller.session.rollback_assert_called_once()
            self.controller.view.display_error.assert_called_with(error)

    def test_update_deal_nothing_to_update(self):
        with patch.object(
            self.controller,
            "get_deal",
            return_value=models.Deal(
                customer=self.customer,
                contact=self.customer.contact,
                bill=1000,
                remaining_on_bill=0,
                has_been_signed=True
            )
        ):
            self.controller.update_deal(self.customer)
            self.controller.view.display_deal_informations.assert_called_once()
            self.controller.view.display_error.assert_called_with(
                errors.ERR_DEAL_NOTHING_TO_UPDATE
            )
            self.controller.session.commit.assert_not_called()

    def test_update_deal_remaining_on_bill_and_sign(self):
        with patch.object(
            self.controller,
            "get_deal",
            return_value=models.Deal(
                customer=self.customer,
                contact=self.customer.contact,
                bill=1000,
                remaining_on_bill=500,
                has_been_signed=False
            )
        ):
            self.controller.update_deal(self.customer)
            self.controller.view.input_deal_signed.assert_called_once()
            self.controller.view.input_deal_remaining_amount.assert_called_with(
                500,
                1000
            )
            self.controller.session.commit.assert_called_once()
            (
                self.
                controller.
                view.
                display_update_deal_validation.
                assert_called_once()
            )
