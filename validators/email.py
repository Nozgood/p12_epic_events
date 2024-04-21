import re
import errors

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


def validate_email(email):
    if not re.match(EMAIL_REGEX, email):
        raise ValueError(errors.ERR_NOT_VALID_EMAIl)
    return email
