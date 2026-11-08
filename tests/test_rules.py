"""Regression tests for the Assignment #03 rules AC1-AC5."""
import unittest
from tests import helpers  # noqa: F401
from smart_campus import rules
from smart_campus.rules import can_book, check_interval

NOW, EX = 540, ((600, 660), (900, 960))


class RuleTests(unittest.TestCase):
    def test_ac1_start_equal_now_rejected(self):
        self.assertEqual(check_interval(540, 570, NOW, False, EX), rules.NOT_IN_FUTURE)

    def test_ac1_reversed_and_day_bounds(self):
        self.assertEqual(check_interval(720, 660, NOW, False, EX), rules.OUT_OF_RANGE)
        self.assertTrue(can_book(1380, 1440, NOW, False, EX))
        self.assertFalse(can_book(1400, 1441, NOW, False, EX))

    def test_ac2_boundary_120_vs_121(self):
        self.assertTrue(can_book(720, 840, NOW, False, EX))
        self.assertEqual(check_interval(720, 841, NOW, False, EX), rules.TOO_LONG)

    def test_ac3_blocked_rejects_everything(self):
        self.assertEqual(check_interval(660, 720, NOW, True, EX), rules.BLOCKED)

    def test_ac4_touching_is_not_overlap(self):
        self.assertTrue(can_book(660, 720, NOW, False, EX))   # after 600-660
        self.assertTrue(can_book(540 + 1, 600, NOW, False, EX))  # before 600-660

    def test_ac4_real_overlap_and_later_booking(self):
        self.assertEqual(check_interval(630, 690, NOW, False, EX), rules.OVERLAP)
        self.assertEqual(check_interval(930, 990, NOW, False, EX), rules.OVERLAP)

    def test_ac5_bookings_not_mutated(self):
        ex = [(600, 660)]
        can_book(700, 760, NOW, False, ex)
        self.assertEqual(ex, [(600, 660)])

    def test_non_integer_inputs_return_false(self):
        for bad in ("700", 700.5, None, True):
            self.assertFalse(can_book(bad, 760, NOW, False, EX))


if __name__ == "__main__":
    unittest.main()
