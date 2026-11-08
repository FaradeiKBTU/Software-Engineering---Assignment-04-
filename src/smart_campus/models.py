"""Immutable data types. Bookings are tuples, so nothing can change them (AC5)."""
from dataclasses import dataclass
from typing import Tuple

Booking = Tuple[int, int]  # (start_minute, end_minute)


@dataclass(frozen=True)
class Room:
    id: str
    name: str
    capacity: int
    equipment: frozenset
    blocked: bool
    bookings: Tuple[Booking, ...]
