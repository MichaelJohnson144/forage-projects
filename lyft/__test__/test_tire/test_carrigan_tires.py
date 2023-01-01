import unittest

from lyft.tire.carrigan_tires import CarriganTires


class TestCarriganTires(unittest.TestCase):
    def test_needs_service_true(self):
        x1, y1, x2, y2 = 0.4, 0.6, 0.8, 1.0
        tire = CarriganTires(x1, y1, x2, y2)
        self.assertTrue(tire.needs_service())

    def test_needs_service_false(self):
        x1, y1, x2, y2 = 0.0, 0.2, 0.4, 0.6
        tire = CarriganTires(x1, y1, x2, y2)
        self.assertFalse(tire.needs_service())
