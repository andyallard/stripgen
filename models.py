import random

class Weather:
    def __init__(self, wind_speed=None, direction=None, gust=None, altimeter=None) -> None:
        if wind_speed is not None:
            self.wind_speed = wind_speed
        else:
            self.generate_wind_speed()

        if direction is not None:
            self.direction = direction
        else:
            self.generate_direction()

        if gust is not None:
            self.gust = gust
        else:
            self.generate_gust()

        if altimeter is not None:
            self.altimeter = altimeter
        else:
            self.generate_altimeter()

    def generate_wind_speed(self):
        # Wind is assumed to be most commonly light (5), with lower probability
        # of being anything else, decaying on either side of 5 knots

        # Define the peak and decay rates
        peak = 5
        left_decay = 1  # Faster decay on the left
        right_decay = 0.5  # Slower decay on the right
        values = list(range(0, 30))

        # Compute weights with a custom decay function
        weights = [
            100 / (abs(i - peak) + 1)**(left_decay if i < peak else right_decay)
            for i in values
        ]

        # Normalize weights to make them a proper probability distribution
        weights = [w / sum(weights) for w in weights]

        # Generate a random number with the specified weights
        self.wind_speed = random.choices(values, weights=weights, k=1)[0]

    def generate_direction(self):
        self.direction = random.randint(0, 36) * 10
        if self.wind_speed > 0 and self.direction == 0:
            self.direction = 360

    def generate_gust(self):
        # the stronger the wind, the more likely it is to have gusts
        if self.wind_speed < 10:
            self.gust = random.choice([0, 0, random.randint(5, 20)])
        elif self.wind_speed < 15:
            self.gust = random.choice([0, random.randint(5, 20)])
        else:
            self.gust = random.choice([0, random.randint(5, 20), random.randint(5, 20)])

        # print(' wind: ', wind, 'gust: ', gust)  # for debugging

        # if gust > 0 and (wind + gust) < 15:
        if self.gust > 0 and (self.wind_speed + self.gust) < 15:
            self.gust = 15 - self.wind_speed

        if self.gust > 0:
            self.gust += self.wind_speed  # gust is calculated as an amount over the wind speed, then finally it's converted to actual gust speed

    def generate_altimeter(self):
        self.altimeter = random.randint(2885, 3115)

    def set_calm_wind(self):
        if self.wind_speed < 3:
            self.wind_speed = 0
            self.gust = 0
            self.direction = 0

    def __repr__(self):
        s = f'wind speed: {self.wind_speed}'
        s += f'\ngust speed: {self.gust}'
        s += f'\naltimeter: {self.altimeter}'
        return s

    def __str__(self):
        s = f'{self.direction:03}/{self.wind_speed:02}'
        if self.gust > 0:
            s += f'G{self.gust:02}'
        s += f'   A{self.altimeter:04}'
        return s