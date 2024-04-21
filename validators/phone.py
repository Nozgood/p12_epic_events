import re
import validators

REG_EX_PHONE = r"^\+33[1-9][0-9]{8}$"


def validate_phone(phone):
    if not re.match(REG_EX_PHONE, phone):
        raise ValueError(validators.ERR_NOT_VALID_PHONE)
    return phone
