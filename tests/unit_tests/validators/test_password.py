import unittest
import validators
import errors


class TestValidatePassword(unittest.TestCase):

    def test_validate_password_empty(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_password("")
        self.assertTrue(
            errors.ERR_NOT_VALID_PASSWORD in str(context.exception)
        )

    def test_validate_password_valid(self):
        self.assertEqual(
            validators.validate_password("test_password"),
            "test_password"
        )
