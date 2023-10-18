import numpy as np

from lyft.tire.tire import Tire


# For concrete/child/subclass "CarriganTires" to "'instantiate' the 'abstract parent/base class
# 'Tire,'' its 'parent class' ''must' be called.'"


class CarriganTires(Tire):
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.new_tire_wear_sensors = np.asfarray([self.x1, self.y1, self.x2, self.y2])

    def needs_service(self):
        return (self.new_tire_wear_sensors >= 0.9).any()
