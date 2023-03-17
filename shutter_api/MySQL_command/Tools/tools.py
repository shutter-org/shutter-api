from datetime import date,datetime, timedelta

TIME_INTERVALS = (
    ('year', 31536000),
    ('month', 2592000),
    ('week', 604800),
    ('day', 86400),
    ('hour', 3600),
    ('minute', 60)
)

def getAgeFromDate(date:date) -> int:
    today = date.today()
    age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    return age

def getIntFromRating(bytes:bytes) -> int:
    return 0 if bytes is None else (1 if bytes == b'\x01' else -1)

def getIntervalOdTimeSinceCreation(date:datetime) -> str:
    now = datetime.utcnow()
    timeDiff = now-date
    
    for name, duration in TIME_INTERVALS:
        count = int(timeDiff.total_seconds() / duration)
        if count != 0:
            return f"{count} {name}{'s' if count > 1 else ''} ago"
    return 'now'
    