"""v1: first AI-generated implementation of can_book (saved before any fixes)."""

MINUTES_PER_DAY = 1440
MAX_DURATION = 120


def _is_int(value):
    # bool is a subclass of int in Python, so exclude it explicitly
    return isinstance(value, int) and not isinstance(value, bool)


def can_book(start, end, now, blocked, existing):
    """Return True only if the requested interval [start, end) is bookable.

    Rules (AC1-AC4):
      - room must not be blocked                       (AC3)
      - 0 <= start < end <= 1440, integers             (AC1)
      - start strictly after now                       (AC1)
      - end - start <= 120                             (AC2)
      - no overlap with any existing booking;
        touching at an endpoint is NOT an overlap      (AC4)
    Inputs are never modified.
    """
    # AC3: a blocked room rejects everything
    if blocked:
        return False

    # AC1: types and day bounds
    if not (_is_int(start) and _is_int(end) and _is_int(now)):
        return False
    if not (0 <= start < end <= MINUTES_PER_DAY):
        return False

    # AC1: must start strictly after now
    if start <= now:
        return False

    # AC2: max 120 minutes (exactly 120 allowed)
    if end - start > MAX_DURATION:
        return False

    # AC4: overlap check against every existing booking
    for booked_start, booked_end in existing:
        if start < booked_end and booked_start < end:
            return False

    return True
