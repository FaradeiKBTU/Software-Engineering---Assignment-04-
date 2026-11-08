"""Fictional room catalog and fixed 'current time'. Data only, no logic."""
from .models import Room

CURRENT_TIME = 540  # 09:00, fixed for the whole prototype

ROOMS = (
    Room("sunset", "Sunset Lounge", 20, frozenset({"projector", "whiteboard"}),
         False, ((600, 660), (900, 960))),
    Room("maple", "Maple Lab", 30, frozenset({"computers", "projector"}),
         False, ((570, 630), (720, 780))),
    Room("atrium", "Atrium Studio", 8, frozenset({"whiteboard"}),
         True, ((600, 660),)),
    Room("pine", "Pine Seminar Hall", 60,
         frozenset({"projector", "microphone", "whiteboard"}),
         False, ((600, 660), (1000, 1100))),
    Room("cedar", "Cedar Nook", 4, frozenset(), False, ()),
)

ALL_EQUIPMENT = ("computers", "microphone", "projector", "whiteboard")
