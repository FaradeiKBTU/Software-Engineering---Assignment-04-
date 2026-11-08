"""Human-readable texts. The only module that knows wording."""
from . import rules

TEXT = {
    rules.OK: "Available: the room is free for this time.",
    rules.BLOCKED: "Unavailable: this room is blocked.",
    rules.NOT_INTEGER: "Enter whole minutes after midnight, digits only (for example 660).",
    rules.OUT_OF_RANGE: "Times must satisfy 0 <= start < end <= %d." % rules.MINUTES_PER_DAY,
    rules.NOT_IN_FUTURE: "Start must be later than the current time.",
    rules.TOO_LONG: "Unavailable: a booking can be at most %d minutes." % rules.MAX_LENGTH,
    rules.OVERLAP: "Unavailable: this overlaps an existing booking.",
}


def hhmm(minutes):
    return "%02d:%02d" % divmod(minutes, 60)


def message_for(code):
    return TEXT[code]
