import copy
import unittest

from booking import can_book

NOW = 540
EXISTING = [(600, 660)]


class TestCanBook(unittest.TestCase):
    # --- cases listed in the assignment ---
    def test_touching_end_is_available(self):  # AC4
        self.assertTrue(can_book(660, 720, NOW, False, EXISTING))

    def test_touching_start_is_available(self):  # AC4
        self.assertTrue(can_book(540 + 1, 600, NOW, False, EXISTING))

    def test_overlap_is_unavailable(self):  # AC4
        self.assertFalse(can_book(630, 690, NOW, False, EXISTING))

    def test_fully_inside_existing_is_unavailable(self):  # AC4
        self.assertFalse(can_book(610, 650, NOW, False, EXISTING))

    def test_fully_covering_existing_is_unavailable(self):  # AC4
        self.assertFalse(can_book(590, 670, NOW, False, EXISTING))

    def test_blocked_room_rejects(self):  # AC3
        self.assertFalse(can_book(660, 720, NOW, True, EXISTING))

    def test_exactly_120_minutes_is_available(self):  # AC2
        self.assertTrue(can_book(720, 840, NOW, False, EXISTING))

    def test_121_minutes_is_unavailable(self):  # AC2
        self.assertFalse(can_book(720, 841, NOW, False, EXISTING))

    def test_starts_now_is_unavailable(self):  # AC1
        self.assertFalse(can_book(540, 570, NOW, False, EXISTING))

    def test_starts_before_now_is_unavailable(self):  # AC1
        self.assertFalse(can_book(500, 530, NOW, False, EXISTING))

    def test_starts_one_minute_after_now_is_available(self):  # AC1
        self.assertTrue(can_book(541, 570, NOW, False, []))

    # --- reversed / empty ranges ---
    def test_reversed_times(self):  # AC1
        self.assertFalse(can_book(720, 660, NOW, False, EXISTING))

    def test_start_equals_end(self):  # AC1
        self.assertFalse(can_book(720, 720, NOW, False, EXISTING))

    # --- day bounds ---
    def test_end_at_1440_is_available(self):  # AC1
        self.assertTrue(can_book(1380, 1440, NOW, False, []))

    def test_end_after_1440_is_unavailable(self):  # AC1
        self.assertFalse(can_book(1400, 1441, NOW, False, []))

    def test_negative_start_is_unavailable(self):  # AC1
        self.assertFalse(can_book(-10, 30, NOW, False, []))

    def test_start_zero_with_now_zero_is_unavailable(self):  # AC1
        self.assertFalse(can_book(0, 30, 0, False, []))

    # --- multiple bookings ---
    def test_overlap_with_second_booking_is_unavailable(self):  # AC4
        existing = [(600, 660), (700, 760)]
        self.assertFalse(can_book(730, 780, NOW, False, existing))

    def test_gap_between_two_bookings_is_available(self):  # AC4
        existing = [(600, 660), (720, 780)]
        self.assertTrue(can_book(660, 720, NOW, False, existing))

    def test_unsorted_existing_bookings(self):  # AC4
        existing = [(720, 780), (600, 660)]
        self.assertFalse(can_book(640, 700, NOW, False, existing))
        self.assertTrue(can_book(660, 720, NOW, False, existing))

    def test_empty_existing_list(self):
        self.assertTrue(can_book(600, 660, NOW, False, []))

    # --- invalid types ---
    def test_non_integer_inputs_rejected(self):  # AC1
        self.assertFalse(can_book(600.5, 660, NOW, False, []))
        self.assertFalse(can_book("600", 660, NOW, False, []))
        self.assertFalse(can_book(None, 660, NOW, False, []))
        self.assertFalse(can_book(True, 660, NOW, False, []))

    # --- inputs unchanged (AC5) ---
    def test_inputs_not_mutated(self):  # AC5
        existing = [(720, 780), (600, 660)]
        snapshot = copy.deepcopy(existing)
        can_book(660, 720, NOW, False, existing)
        can_book(630, 690, NOW, False, existing)
        self.assertEqual(existing, snapshot)


if __name__ == "__main__":
    unittest.main(verbosity=2)
