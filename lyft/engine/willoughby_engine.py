from lyft.engine.engine import Engine


# For concrete/child/subclass "WilloughbyEngine" to "'instantiate' the 'abstract parent/base
# class 'Engine,'' its 'parent class' ''must' be called.'"


class WilloughbyEngine(Engine):
    def __init__(self, current_mileage, last_service_mileage):
        self.current_mileage = current_mileage
        self.last_service_mileage = last_service_mileage

    def needs_service(self):
        return self.current_mileage - self.last_service_mileage > 60000
