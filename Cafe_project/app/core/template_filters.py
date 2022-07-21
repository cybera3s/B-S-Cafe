def format_datetime(value, fmt: str ='%Y/%-m/%d %-I:%m'):
    """
        format a datetime object by provided fmt
    """
    return value.strftime(fmt)
