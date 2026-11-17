import unittest
from yixing_calculators import (
    compute_tape_cycle,
    compute_tolerance_stackup,
    match_carton_erector,
)


class TestYixingCalculators(unittest.TestCase):
    def test_vision_labeler_threshold(self) -> None:
        r = compute_tolerance_stackup(target_mm=0.15, part_tolerance_mm=0.10, material_tolerance_mm=0.10)
        self.assertTrue(r.feasible_rss)
        self.assertLessEqual(r.allowable_machine_rss_mm, 0.08)
        self.assertIn("±0.05 mm", r.recommended_architecture_en)

    def test_ccd_tape_applicator_threshold(self) -> None:
        r = compute_tolerance_stackup(target_mm=0.50, part_tolerance_mm=0.25, material_tolerance_mm=0.15)
        self.assertTrue(r.feasible_rss)
        self.assertAlmostEqual(r.allowable_machine_rss_mm, 0.4062, places=3)
        self.assertIn("±0.5 mm", r.recommended_architecture_en)

    def test_tape_cycle_and_short_cut_warning(self) -> None:
        r = compute_tape_cycle(strip_length_mm=60, strips_per_part=2, index_swap_seconds=1.6, roll_length_meters=50.0)
        self.assertFalse(r.min_cut_length_warning)
        self.assertEqual(r.parts_per_roll, 416)
        short = compute_tape_cycle(strip_length_mm=20, strips_per_part=1)
        self.assertTrue(short.min_cut_length_warning)

    def test_carton_erector_matching(self) -> None:
        r = match_carton_erector("ch", 180, 120, 60, 350)
        self.assertTrue(r.grammage_in_standard_range)
        self.assertIn("FEFCO 0427", r.matched_series)


if __name__ == "__main__":
    unittest.main()
