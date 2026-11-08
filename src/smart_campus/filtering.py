"""Room catalog filtering (F1-F4). Pure functions, no UI and no booking rules."""

AVAILABLE = "available"
BLOCKED = "blocked"


def matches(room, participants, required_equipment):
    """F1: capacity >= participants. F2: room has ALL required equipment."""
    return room.capacity >= participants and set(required_equipment) <= room.equipment


def filter_rooms(rooms, participants=0, required_equipment=()):
    """Return [(room, status)] for rooms that fit the filters.
    F3: a blocked room is never reported as 'available'.
    F4: an empty list means 'nothing matched' (the UI shows the empty state)."""
    result = []
    for room in rooms:
        if matches(room, participants, required_equipment):
            result.append((room, BLOCKED if room.blocked else AVAILABLE))
    return result
