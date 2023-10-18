from lyft.battery.nubbin_battery import NubbinBattery
from lyft.battery.spindler_battery import SpindlerBattery
from lyft.car import Car
from lyft.engine.capulet_engine import CapuletEngine
from lyft.engine.sternman_engine import SternmanEngine
from lyft.engine.willoughby_engine import WilloughbyEngine
from lyft.tire.carrigan_tires import CarriganTires
from lyft.tire.octoprime_tires import OctoprimeTires


# The "@staticmethod" is a 'function decorator' that is used to "'group' ''methods (Also known as
# 'functions')' with 'similar functionality' or 'some logical connection' 'between two or more
# classes.''" As per the official Python docs: "A static method does not receive an implicit
# first argument."
# "It can be called either on the class (such as C.f()) or on an instance (such
# as C().f())."


class CarFactory:
    @staticmethod
    def calliope(
        current_date,
        last_service_date,
        current_mileage,
        last_service_mileage,
        x1,
        y1,
        x2,
        y2,
    ):
        engine = CapuletEngine(current_mileage, last_service_mileage)
        battery = SpindlerBattery(current_date, last_service_date)
        tire = CarriganTires(x1, y1, x2, y2) or OctoprimeTires(x1, y1, x2, y2)
        car = Car(engine, battery, tire)
        return car

    @staticmethod
    def glissade(
        current_date,
        last_service_date,
        current_mileage,
        last_service_mileage,
        x1,
        y1,
        x2,
        y2,
    ):
        engine = WilloughbyEngine(current_mileage, last_service_mileage)
        battery = SpindlerBattery(current_date, last_service_date)
        tire = CarriganTires(x1, y1, x2, y2) or OctoprimeTires(x1, y1, x2, y2)
        car = Car(engine, battery, tire)
        return car

    @staticmethod
    def palindrome(
        current_date, last_service_date, warning_light_is_on, x1, y1, x2, y2
    ):
        engine = SternmanEngine(warning_light_is_on)
        battery = SpindlerBattery(current_date, last_service_date)
        tire = CarriganTires(x1, y1, x2, y2) or OctoprimeTires(x1, y1, x2, y2)
        car = Car(engine, battery, tire)
        return car

    @staticmethod
    def rorschach(
        current_date,
        last_service_date,
        current_mileage,
        last_service_mileage,
        x1,
        y1,
        x2,
        y2,
    ):
        engine = WilloughbyEngine(current_mileage, last_service_mileage)
        battery = NubbinBattery(current_date, last_service_date)
        tire = CarriganTires(x1, y1, x2, y2) or OctoprimeTires(x1, y1, x2, y2)
        car = Car(engine, battery, tire)
        return car

    @staticmethod
    def thovex(
        current_date,
        last_service_date,
        current_mileage,
        last_service_mileage,
        x1,
        y1,
        x2,
        y2,
    ):
        engine = CapuletEngine(current_mileage, last_service_mileage)
        battery = NubbinBattery(current_date, last_service_date)
        tire = CarriganTires(x1, y1, x2, y2) or OctoprimeTires(x1, y1, x2, y2)
        car = Car(engine, battery, tire)
        return car
