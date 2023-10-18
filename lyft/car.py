from lyft.serviceable import Serviceable


# For concrete/child/subclass "Car" to "'instantiate' the 'abstract parent/base class
# 'Serviceable,'' its 'parent function/method (Which, in this case is specifically
# 'def needs_service(self)')' ''must' be called.'" its 'parent class' ''must' be called.'"


class Car(Serviceable):
    def __init__(self, engine, battery, tire):
        self.engine = engine
        self.battery = battery
        self.tire = tire

    def needs_service(self):
        return (
            self.engine.needs_service()
            or self.battery.needs_service()
            or self.tire.needs_service()
        )
