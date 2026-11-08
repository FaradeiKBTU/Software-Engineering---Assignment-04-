"""Integration tests: parsing + filtering + rules through RoomService (F5 included)."""
import unittest
from tests import helpers  # noqa: F401
from smart_campus.service import RoomService, parse_minutes


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.svc = RoomService()

    def test_f5_same_time_different_result_per_room(self):
        # 560-590 overlaps Maple (570-630) but not Sunset (600-660)
        self.assertTrue(self.svc.check("sunset", "560", "590")["available"])
        self.assertEqual(self.svc.check("maple", "560", "590")["code"], "OVERLAP")

    def test_f5_each_room_uses_only_its_own_bookings(self):
        # 720-780 is booked in Maple only
        self.assertEqual(self.svc.check("maple", "720", "780")["code"], "OVERLAP")
        self.assertTrue(self.svc.check("sunset", "720", "780")["available"])
        self.assertTrue(self.svc.check("cedar", "720", "780")["available"])

    def test_blocked_room_rejected_via_service(self):
        self.assertEqual(self.svc.check("atrium", "700", "760")["code"], "BLOCKED")

    def test_strict_parser_rejects_tricky_text(self):
        for bad in ("1e3", "0700", "0x10", "720.5", "-5", "", " ", "abc"):
            self.assertIsNone(parse_minutes(bad), bad)
        self.assertEqual(parse_minutes("0"), 0)
        self.assertEqual(parse_minutes("700"), 700)

    def test_bad_text_gives_friendly_message(self):
        out = self.svc.check("sunset", "1e3", "1100")
        self.assertFalse(out["available"])
        self.assertIn("digits only", out["message"])

    def test_search_capacity_and_empty_state(self):
        self.assertTrue(self.svc.search("500")["empty"])
        self.assertIn("whole number", self.svc.search("abc")["error"])
        names = [r["id"] for r in self.svc.search("25")["rooms"]]
        self.assertEqual(names, ["maple", "pine"])

    def test_unknown_room(self):
        self.assertEqual(self.svc.check("nope", "700", "760")["code"], "NO_ROOM")


if __name__ == "__main__":
    unittest.main()
