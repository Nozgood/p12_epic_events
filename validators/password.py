import errors


def validate_password(password):
    if password == "":
        raise ValueError(errors.ERR_NOT_VALID_PASSWORD)
    return password
