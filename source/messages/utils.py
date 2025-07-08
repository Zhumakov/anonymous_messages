from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def is_valid_timezone(timezone: str) -> bool:
    try:
        ZoneInfo(timezone)
        return True
    except ZoneInfoNotFoundError:
        return False
