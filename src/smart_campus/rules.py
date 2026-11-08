"""The ONLY place where booking/availability rules (AC1-AC5) are implemented."""
from .models import Room

MINUTES_PER_DAY = 1440
MAX_LENGTH = 120

OK = "OK"
NOT_INTEGER = "NOT_INTEGER"
BLOCKED = "BLOCKED"
OUT_OF_RANGE = "OUT_OF_RANGE"
NOT_IN_FUTURE = "NOT_IN_FUTURE"
TOO_LONG = "TOO_LONG"
OVERLAP = "OVERLAP"


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def overlaps(start, end, booked_start, booked_end):
    """Strict comparison: touching at an endpoint is NOT an overlap (AC4)."""
    return start < booked_end and booked_start < end


def check_interval(start, end, now, blocked, existing):
    """Return OK or the code of the first rule that rejects the request."""
    if blocked:
        return BLOCKED
    if not (_is_int(start) and _is_int(end) and _is_int(now)):
        return NOT_INTEGER
    if not (0 <= start < end <= MINUTES_PER_DAY):
        return OUT_OF_RANGE
    if start <= now:
        return NOT_IN_FUTURE
    if end - start > MAX_LENGTH:
        return TOO_LONG
    for booked_start, booked_end in existing:
        if overlaps(start, end, booked_start, booked_end):
            return OVERLAP
    return OK


def check_room(room: Room, start, end, now):
    """Check a request against ONE room, using that room's own bookings (F5)."""
    return check_interval(start, end, now, room.blocked, room.bookings)


def can_book(start, end, now, blocked, existing):
    """Same contract as the Assignment #03 function."""
    return check_interval(start, end, now, blocked, existing) == OK
