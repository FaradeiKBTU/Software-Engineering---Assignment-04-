"""Application layer: parses UI input, calls filtering and rules, builds responses."""
import re

from . import filtering, rules
from .messages import hhmm, message_for
from .rooms_data import ALL_EQUIPMENT, CURRENT_TIME, ROOMS

_DIGITS = re.compile(r"^(0|[1-9]\d*)$")


def parse_minutes(text):
    """Strict whole-minute parser: rejects 1e3, 0700, 0x10, 720.5, -5, ''."""
    if isinstance(text, int) and not isinstance(text, bool):
        return text
    if isinstance(text, str) and _DIGITS.match(text.strip()):
        return int(text.strip())
    return None


def _room_json(room, status):
    return {
        "id": room.id, "name": room.name, "capacity": room.capacity,
        "equipment": sorted(room.equipment), "status": status,
        "bookings": [hhmm(s) + "-" + hhmm(e) for s, e in room.bookings],
    }


class RoomService:
    def __init__(self, rooms=ROOMS, now=CURRENT_TIME):
        self._rooms = {r.id: r for r in rooms}
        self._order = tuple(rooms)
        self.now = now

    def config(self):
        return {"now": self.now, "nowText": hhmm(self.now), "maxLength": rules.MAX_LENGTH,
                "dayEnd": rules.MINUTES_PER_DAY, "equipment": list(ALL_EQUIPMENT)}

    def search(self, participants_text="", equipment=()):
        text = (participants_text or "").strip()
        participants = 0 if text == "" else parse_minutes(text)
        if participants is None:
            return {"error": "Participants must be a whole number (0 or more).", "rooms": []}
        found = filtering.filter_rooms(self._order, participants, equipment)
        return {"error": None, "rooms": [_room_json(r, s) for r, s in found],
                "empty": not found}

    def check(self, room_id, start_text, end_text):
        room = self._rooms.get(room_id)
        if room is None:
            return {"available": False, "code": "NO_ROOM", "message": "Choose a room first."}
        start, end = parse_minutes(start_text), parse_minutes(end_text)
        code = rules.NOT_INTEGER if start is None or end is None else \
            rules.check_room(room, start, end, self.now)
        return {"available": code == rules.OK, "code": code,
                "message": message_for(code), "room": room.name}
