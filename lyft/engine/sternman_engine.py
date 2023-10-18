from lyft.engine.engine import Engine


# For concrete/child/subclass "WilloughbyEngine" to "'instantiate' the 'abstract parent/base
# class 'Engine,'' its 'parent class' ''must' be called.'"


class SternmanEngine(Engine):
    def __init__(self, warning_light_is_on):
        self.warning_light_is_on = warning_light_is_on

    def needs_service(self):
        if self.warning_light_is_on:
            return True
        else:
            return False
