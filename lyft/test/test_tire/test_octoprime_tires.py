import unittest

from lyft.tire.octoprime_tires import OctoprimeTires


class TestOctoprimeTires(unittest.TestCase):
    def test_needs_service_true(self):
        x1, y1, x2, y2 = 0.2, 0.3, 1.2, 1.3
        tire = OctoprimeTires(x1, y1, x2, y2)
        self.assertTrue(tire.needs_service())

    def test_needs_service_false(self):
        x1, y1, x2, y2 = 0.1875, 0.375, 0.75, 1.5
        tire = OctoprimeTires(x1, y1, x2, y2)
        self.assertFalse(tire.needs_service())
