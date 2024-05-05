import errors


def validate_period(start_date, end_date):
    if start_date > end_date:
        raise ValueError(errors.ERR_NOT_VALID_PERIOD)
