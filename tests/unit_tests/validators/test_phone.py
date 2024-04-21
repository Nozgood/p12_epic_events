import unittest
import validators


class TestValidatePhone(unittest.TestCase):
    def test_validate_phone_valid(self):
        self.assertEqual(
            validators.validate_phone("+33123456789"),
            "+33123456789"
        )

    def test_validate_phone_invalid(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_phone("1234567890")
        self.assertTrue(
            validators.ERR_NOT_VALID_PHONE in str(context.exception)
        )

    def test_validate_phone_empty(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_phone("")
        self.assertTrue(
            validators.ERR_NOT_VALID_PHONE in str(context.exception)
        )

    def test_validate_phone_missing_plus(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_phone("33123456789")
        self.assertTrue(
            validators.ERR_NOT_VALID_PHONE in str(context.exception)
        )

    def test_validate_phone_short_number(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_phone("+3312345678")
        self.assertTrue(
            validators.ERR_NOT_VALID_PHONE in str(context.exception)
        )
