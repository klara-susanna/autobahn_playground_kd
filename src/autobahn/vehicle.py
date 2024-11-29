import random


class Car:

    def __init__(self):
        self.speed = self._default_speed()

    def _default_speed(self):
        return random.uniform(105.0, 135.0)

    def get_speed(self):
        return self.speed

    def update_speed(self, traffic_info):
        if traffic_info.get("averageSpeed") is not None:
            self.speed = traffic_info["averageSpeed"]
        else:
            self.speed = 80.0
