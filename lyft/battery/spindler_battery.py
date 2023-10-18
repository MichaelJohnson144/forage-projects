from lyft.battery.battery import Battery
from lyft.utils.utils import add_years_to_date


# For concrete/child/subclass "SpindlerBattery" to "'instantiate' the 'abstract parent/base class
# 'Battery,'' its 'parent class' ''must' be called.'"


class SpindlerBattery(Battery):
    def __init__(self, current_date, last_service_date):
        self.current_date = current_date
        self.last_service_date = last_service_date

    def needs_service(self):
        date_which_battery_should_be_serviced_by = add_years_to_date(
            self.last_service_date, 3
        )
        if date_which_battery_should_be_serviced_by < self.current_date:
            return True
        else:
            return False
