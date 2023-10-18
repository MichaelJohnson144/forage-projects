import unittest
from datetime import datetime

from lyft.car_factory import CarFactory
from lyft.utils.utils import add_years_to_date


class TestCalliope(unittest.TestCase):
    def test_engine_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=None,
        current_mileage=0,
        last_service_mileage=0,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        if last_service_date is None:
            last_service_date = add_years_to_date(current_date, -3)

        car = CarFactory.calliope(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if current_mileage >= 30000:
                return self.assertTrue(car.needs_service())
            elif current_mileage < 30000:
                return self.assertFalse(car.needs_service())

    def test_battery_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=None,
        current_mileage=None,
        last_service_mileage=None,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.calliope(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if last_service_date == current_date.replace(year=current_date.year - 3):
                return self.assertTrue(car.needs_service())
            elif last_service_date == current_date.replace(year=current_date.year - 1):
                return self.assertFalse(car.needs_service())


class TestGlissade(unittest.TestCase):
    def test_engine_service_criteria(
        self,
        current_date=None,
        last_service_date=None,
        current_mileage=0,
        last_service_mileage=0,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.glissade(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if current_mileage >= 60000:
                return self.assertTrue(car.needs_service())
            elif current_mileage < 60000:
                return self.assertFalse(car.needs_service())

    def test_battery_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=None,
        current_mileage=int,
        last_service_mileage=int,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.glissade(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if last_service_date == current_date.replace(year=current_date.year - 3):
                return self.assertTrue(car.needs_service())
            elif last_service_date == current_date.replace(year=current_date.year - 1):
                return self.assertFalse(car.needs_service())


class TestPalindrome(unittest.TestCase):
    def test_engine_service_criteria(
        self,
        current_date=None,
        last_service_date=None,
        warning_indicator_is_on=bool,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.palindrome(
            current_date, last_service_date, warning_indicator_is_on, x1, y1, x2, y2
        )
        if warning_indicator_is_on is True:
            return self.assertTrue(car.needs_service())
        elif warning_indicator_is_on is False:
            return self.assertFalse(car.needs_service())

    def test_battery_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=None,
        warning_indicator_is_on=bool,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.palindrome(
            current_date, last_service_date, warning_indicator_is_on, x1, y1, x2, y2
        )
        if car:
            if last_service_date == current_date.replace(year=current_date.year - 5):
                return self.assertTrue(car.needs_service())
            elif last_service_date == current_date.replace(year=current_date.year - 3):
                return self.assertFalse(car.needs_service())


class TestRorschach(unittest.TestCase):
    def test_engine_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=datetime.today().date(),
        current_mileage=0,
        last_service_mileage=0,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.calliope(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if current_mileage >= 60000:
                return self.assertTrue(car.needs_service())
            elif current_mileage < 60000:
                return self.assertFalse(car.needs_service())

    def test_battery_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=None,
        current_mileage=int,
        last_service_mileage=int,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.calliope(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if last_service_date == current_date.replace(year=current_date.year - 5):
                return self.assertTrue(car.needs_service())
            elif last_service_date == current_date.replace(year=current_date.year - 3):
                return self.assertFalse(car.needs_service())


class TestThovex(unittest.TestCase):
    def test_engine_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=datetime.today().date(),
        current_mileage=0,
        last_service_mileage=0,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.calliope(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if current_mileage >= 30000:
                return self.assertTrue(car.needs_service())
            elif current_mileage < 30000:
                return self.assertFalse(car.needs_service())

    def test_battery_service_criteria(
        self,
        current_date=datetime.today().date(),
        last_service_date=None,
        current_mileage=int,
        last_service_mileage=int,
        x1=0,
        y1=0,
        x2=0,
        y2=0,
    ):
        car = CarFactory.calliope(
            current_date,
            last_service_date,
            current_mileage,
            last_service_mileage,
            x1,
            y1,
            x2,
            y2,
        )
        if car:
            if last_service_date == current_date.replace(year=current_date.year - 5):
                return self.assertTrue(car.needs_service())
            elif last_service_date == current_date.replace(year=current_date.year - 3):
                return self.assertFalse(car.needs_service())


if __name__ == "__main__":
    unittest.main()
