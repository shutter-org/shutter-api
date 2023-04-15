from datetime import date, datetime

TIME_INTERVALS = (
    ('year', 31536000),
    ('month', 2592000),
    ('week', 604800),
    ('day', 86400),
    ('hour', 3600),
    ('minute', 60)
)


def getAgeFromDate(date: date) -> int:
    """
    get the age diff between the date and the current date

    Args:
        date (date): birthdate

    Returns:
        int: age
    """
    today = date.today()
    age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    return age


def getIntFromRating(bytes: bytes) -> int:
    """
    from bytes to int 0 -> -1, 1 -> 1 and None -> 0

    Args:
        bytes (bytes): bytes that represent the rating

    Returns:
        int: the rating of the user
    """
    return 0 if bytes is None else (1 if bytes == b'\x01' else -1)


def getIntervalOdTimeSinceCreation(date: datetime) -> str:
    """
    get the interval of time between the dateTime and now

    Args:
        date (datetime): creation_date

    Returns:
        str: the interval of time like "1 year ago"
    """
    now = datetime.utcnow()
    timeDiff = now - date

    for name, duration in TIME_INTERVALS:
        count = int(timeDiff.total_seconds() / duration)
        if count != 0:
            return f"{count} {name}{'s' if count > 1 else ''} ago"
    return 'now'
