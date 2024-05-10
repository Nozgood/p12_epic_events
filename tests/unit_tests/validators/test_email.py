import unittest
import validators
import errors


class TestValidateEmail(unittest.TestCase):
    def test_validate_email_valid(self):
        self.assertEqual(
            validators.validate_email("example@test.com"),
            "example@test.com"
        )

    def test_validate_email_invalid(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_email("example")
        self.assertTrue(
            errors.ERR_NOT_VALID_EMAIl in str(context.exception)
        )

    def test_validate_email_empty(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_email("")
        self.assertTrue(
            errors.ERR_NOT_VALID_EMAIl in str(context.exception)
        )

    def test_validate_email_no_domain(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_email("example@")
        self.assertTrue(
            errors.ERR_NOT_VALID_EMAIl in str(context.exception)
        )

    def test_validate_email_no_at_symbol(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_email("example.com")
        self.assertTrue(
            errors.ERR_NOT_VALID_EMAIl in str(context.exception)
        )
