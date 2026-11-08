"""F1-F4 filtering tests on the real catalog and on small custom rooms."""
import unittest
from tests import helpers  # noqa: F401
from smart_campus.filtering import filter_rooms, AVAILABLE, BLOCKED
from smart_campus.models import Room
from smart_campus.rooms_data import ROOMS


def ids(result):
    return [r.id for r, _ in result]


class FilterTests(unittest.TestCase):
    def test_catalog_has_at_least_four_rooms(self):
        self.assertGreaterEqual(len(ROOMS), 4)

    def test_f1_capacity_exactly_equal_matches_but_one_more_does_not(self):
        rooms = (Room("a", "A", 10, frozenset(), False, ()),)
        self.assertEqual(ids(filter_rooms(rooms, 10)), ["a"])
        self.assertEqual(filter_rooms(rooms, 11), [])

    def test_f2_requires_all_selected_equipment(self):
        got = ids(filter_rooms(ROOMS, 0, ["projector", "microphone"]))
        self.assertEqual(got, ["pine"])           # others have only one of the two
        self.assertEqual(filter_rooms(ROOMS, 0, ["projector", "whiteboard", "computers"]), [])

    def test_f3_blocked_room_is_never_available(self):
        status = dict((r.id, s) for r, s in filter_rooms(ROOMS, 5, ["whiteboard"]))
        self.assertEqual(status["atrium"], BLOCKED)
        self.assertTrue(all(s != AVAILABLE for rid, s in status.items() if rid == "atrium"))

    def test_f4_empty_result_for_impossible_filters(self):
        self.assertEqual(filter_rooms(ROOMS, 500, []), [])

    def test_no_filters_returns_whole_catalog(self):
        self.assertEqual(len(filter_rooms(ROOMS)), len(ROOMS))


if __name__ == "__main__":
    unittest.main()
