import unittest
import validators
import errors
from datetime import datetime


class TestValidateDate(unittest.TestCase):
    def test_validate_period_not_valid(self):
        with self.assertRaises(ValueError) as context:
            validators.validate_period(
                datetime(2024, 2, 1),
                datetime(2024, 1, 1)
            )
        self.assertTrue(
            errors.ERR_NOT_VALID_PERIOD in str(context.exception)
        )

    def test_validate_period_valid(self):
        self.assertEqual(
            validators.validate_period(
                datetime(2024, 2, 1),
                datetime(2024, 12, 10)
            ),
            (
                datetime(2024, 2, 1),
                datetime(2024, 12, 10)
            )
        )
