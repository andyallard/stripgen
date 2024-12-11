import random
import string
from datetime import datetime, timedelta


aircraft_types = [
    "BE20", "BE76", "C150", "C172", "C182", "C185", "C206", "C208", "C210", "C421", "C550",
    "DHC2", "DHC6", "DV20", "PC12", "P28A", "PA31", "PA34", "PAY2",
    "B190", "DH8A", "DH8B", "DH8C", "DH8D", "SW4", "C130", "SF34",
    "A320", "B737", "CRJ1", "CL60", "E175", "LJ35", "B06", "R44", "H46",
]
class Scenario:
    def __init__(self, basic_data, time=None) -> None:
        self.generate_random_time(time)
        self.weather = Weather()
        self.basic_data = basic_data
        self.aircraft = []
        self.determine_runway()
        self.set_circuit_direction()

    def __repr__(self):
        s = f'{self.title} Scenario - Weather: {self.weather}, '
        s += f" {self.aircraft.length} aircraft"

    def __str__(self) -> str:
        s = f'{self.title} Scenario:\n'
        s += f'  {self.formatted_time()}  '
        s += f'  {self.weather}\n'
        s += f'{self.formatted_aircraft(indent=4)}'
        return s

    def set_title(self, title):
        self.title = title

    def generate_random_time(self, time):
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        self.time = datetime.strptime(f"{random_hour:02}:{random_minute:02}", "%H:%M") if time is None else time

    def formatted_time(self):
        return self.time.strftime("%H%M")

    def formatted_aircraft(self, indent=0):
        s = ''
        for aircraft in self.aircraft:
            s += ' ' * indent
            s += f'{repr(aircraft)}\n'
        return s

    def determine_runway(self):
        runways = (90, 140, 270, 320)
        dir = self.weather.direction

        # TODO: need to decide how scenario determines the runway when wind is calm
        # if self.weather.wind_speed >= 5:
        #     dir = self.weather.direction
        # else:
        #     dir = self.track

        differences = [self.bearing_difference(dir, runway) for runway in runways]
        runway = runways[differences.index(min(differences))]
        runway = int(runway / 10)
        self.determined_runway = f'{runway:02}'

    def bearing_difference(self, bearing, runway):
        difference = abs(runway - bearing)
        if difference > 180:
            difference = 360 - difference
        return difference

    def set_circuit_direction(self):
        if self.determined_runway in ['09', '14']:
            self.circuit_direction = 1  # right hand circuits
        elif self.determined_runway in ['27', '32']:
            self.circuit_direction = -1  # left hand circuits

    def generate_name(self, name):
        if name is None:
            return f"aircraft{len(self.aircraft) + 1}"
        else:
            return name

    def add_aircraft(self, name=None, restrictions=dict()):
        self.aircraft.append(Strip(self.basic_data, self.time, self.weather, restrictions))

    def add_distant_arrival(self, name=None, restrictions=dict()):
        self.aircraft.append(Distant_Arrival_Strip(self.basic_data, self.time, self.weather, restrictions))

    def add_departure(self, name=None, restrictions=dict()):
        self.aircraft.append(Departure_Strip(self.basic_data, self.time, self.weather, restrictions))

    def add_circuit(self, name=None, restrictions=dict()):
        self.aircraft.append(Circuit_Strip(self.basic_data, self.time, self.weather, restrictions))

    def add_overflight(self, name=None, restrictions=dict()):
        self.aircraft.append(Overflight_Strip(self.basic_data, self.time, self.weather, restrictions))

class Scenario_DA_DA(Scenario):
    def __init__(self, basic_data, time=None):
        super().__init__(basic_data, time)

        self.add_distant_arrival()
        strip = self.aircraft[len(self.aircraft) - 1]  # get last item in list
        self.restrictions = {}
        self.restrictions['arrive 2 min from'] = strip.eta
        self.add_distant_arrival(restrictions=self.restrictions)

class Weather:
    def __init__(self, wind_speed=None, direction=None, gust=None, altimeter=None) -> None:
        self.generate_wind_speed(wind_speed)
        self.generate_direction(direction)
        self.generate_gust(gust)
        self.generate_altimeter(altimeter)

        self.check_calm_wind()

    def generate_wind_speed(self, wind_speed=None):
        if wind_speed is not None:
            self.wind_speed = wind_speed
            return
        
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

    def generate_direction(self, direction=None):
        if direction is not None:
            self.direction = direction
            return
        
        self.direction = random.randint(0, 36) * 10
        if self.wind_speed > 0 and self.direction == 0:
            self.direction = 360

    def generate_gust(self, gust=None):
        if gust is not None:
            self.gust = gust
            return
        
        # the stronger the wind, the more likely it is to have gusts
        if self.wind_speed < 10:
            self.gust = random.choice([0, 0, random.randint(5, 20)])
        elif self.wind_speed < 15:
            self.gust = random.choice([0, random.randint(5, 20)])
        else:
            self.gust = random.choice([0, random.randint(5, 20), random.randint(5, 20)])

        if self.gust > 0 and (self.wind_speed + self.gust) < 15:
            self.gust = 15 - self.wind_speed

        if self.gust > 0:
            self.gust += self.wind_speed  # gust is calculated as an amount over the wind speed, then finally it's converted to actual gust speed

    def generate_altimeter(self, altimeter=None):
        if altimeter is not None:
            self.altimeter = altimeter
            return

        self.altimeter = random.randint(2885, 3115)

    def check_calm_wind(self):
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
        return f'{self.print_wind()}  {self.print_altimeter()}'

    def print_wind(self):
        s = f'{self.direction:03}/{self.wind_speed:02}'
        if self.gust > 0:
            s += f'G{self.gust:02}'
        return s

    def print_altimeter(self):
        return f'A{self.altimeter:04}'


class Strip:
    def __init__(self, basic_data, scenario_time, weather, restrictions=dict()):
        self.scenario_time = scenario_time
        self.restrictions = restrictions
        self.generate_identifier()
        self.generate_aircraft_type(aircraft_types)
        self.flight_rules = 'V'
        self.set_type()
        self.set_destination(basic_data)
        self.set_point_of_departure(basic_data)
        self.determine_track()
        self.determine_runway(weather)
        self.set_actual_runway()
        self.set_departure_time()
        self.set_departed_flag()
        self.determine_fl_direction()
        self.generate_altitude()
        self.eta = None

    def __repr__(self):
        s = f"{self.type} - {self.ident}: {self.aircraft_type} | "
        s += f"DR: {self.determined_runway} AR: {self.actual_runway} | "
        s += f"{self.point_of_departure['location']} > "
        s += f"{self.destination['location']}, "
        s += f"arr: {self.formatted_time(self.eta)}, "
        s += f"dep: {self.formatted_time(self.departure_time)}, "
        s += f" alt: {self.altitude}"
        return s
    
    def __str__(self):
        s = 'Flight Data Entry (strip)'
        s += f"\n   identifier: {self.ident}"
        s += f"\n   aircraft type: {self.aircraft_type}"
        s += f"\n   flight type: {self.type}"
        s += f"\n   point of departure: {self.point_of_departure['location']}"
        s += f"\n   destination: {self.destination['location']}"
        return s

    def generate_identifier(self):
        first_letter = 'C'
        second_letter = random.choice(['F', 'G'])
        remaining_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        self.ident = f"{first_letter}{second_letter}{remaining_letters}"
    
    def generate_aircraft_type(self, types):
        self.aircraft_type = random.choice(types)

    def set_type(self):
        self.type = None

    def set_destination(self, basic_data):
        self.destination = basic_data['march']

    def set_point_of_departure(self, basic_data):
        self.point_of_departure = basic_data['march']

    def generate_eta(self):
        sync_to = self.restrictions.get('arrive 2 min from')
        if sync_to:
            delta = int((sync_to - self.scenario_time).total_seconds() / 60)
            values = list(range(delta - 2, delta + 2))
        else:
            values = list(range(5, 20))

        weights = [(20 - i) for i in values]

        # Normalize weights to make them a proper probability distribution
        weights = [w / sum(weights) for w in weights]

        # Generate a random number with the specified weights
        estimating = random.choices(values, weights=weights, k=1)[0]
        self.eta = self.scenario_time + timedelta(minutes=estimating)
    
    def generate_altitude(self):
        if self._fl_direction == '':
            self.altitude = ''
        else:
            self.altitude = random.randint(2, 6)
            self.altitude *= 20
            self.altitude += 5
            if self._fl_direction == 'east':
                self.altitude -= 10

    def determine_track(self):
        self.track = 0

    def set_departure_time(self):
        self.departure_time = None

    def formatted_time(self, time):
        if time is None:
            return ''
        else:
            return time.strftime("%H%M")

    def determine_fl_direction(self):
        self._fl_direction = ''

    def determine_runway(self, weather):
        runways = (90, 140, 270, 320)

        if weather.wind_speed >= 5:
            dir = weather.direction
        else:
            dir = self.track

        differences = [self.bearing_difference(dir, runway) for runway in runways]
        runway = runways[differences.index(min(differences))]
        runway = int(runway / 10)
        self.determined_runway = f'{runway:02}'

    def bearing_difference(self, bearing, runway):
        difference = abs(runway - bearing)
        if difference > 180:
            difference = 360 - difference
        return difference

    def set_actual_runway(self):
        self.actual_runway = self.determined_runway

    def set_departed_flag(self):
        if self.departure_time is None:
            self.departed = None
        elif self.departure_time < self.scenario_time:
            self.departed = True
        else:
            self.departed = False
        
class Distant_Arrival_Strip(Strip):
    def __init__(self, basic_data, time, weather, restrictions=None):
        super().__init__(basic_data, time, weather, restrictions)        
        self.generate_eta()

    def set_type(self):
        self.type = 'A'

    def set_point_of_departure(self, basic_data):
        self.point_of_departure = random.choice(basic_data['locations'])

    def determine_track(self):
        self.track = self.point_of_departure['bearing']

    def determine_fl_direction(self):
        if 0 <= self.point_of_departure['bearing'] < 180:
            self._fl_direction = 'west'
        else:
            self._fl_direction = 'east'
        

class Departure_Strip(Strip):

    def set_type(self):
        self.type = 'D'

    def set_destination(self, basic_data):
        self.destination = random.choice(basic_data['locations'])

    def determine_track(self):
        self.track = self.destination['bearing']

    def determine_fl_direction(self):
        if 0 <= self.destination['bearing'] < 180:
            self._fl_direction = 'east'
        else:
            self._fl_direction = 'west'

    def set_departure_time(self):
        estimating = random.randint(-2, 3)
        self.departure_time = self.scenario_time + timedelta(minutes=estimating)

class Circuit_Strip(Strip):

    def set_type(self):
        self.type = 'C'

    def set_departure_time(self):
        offset = -random.randint(5, 90)
        self.departure_time = self.scenario_time + timedelta(minutes=offset)

class Overflight_Strip(Strip):
    def __init__(self, basic_data, time, weather, restrictions=None):
        super().__init__(basic_data, time, weather, restrictions)        
        self.generate_eta(time)

    def set_type(self):
        self.type = 'O'

    def set_actual_runway(self):
        self.actual_runway = '88'

    def determine_fl_direction(self):
        # technically this could be inaccurate for overflights
        # (ex. flying from a destination at 160 to one at 009)
        # but for the purpose of this application, it's not too important
        if 0 <= self.destination['bearing'] < 180:
            self._fl_direction = 'east'
        else:
            self._fl_direction = 'west'

    def generate_altitude(self):
        options = [28, 29, 30]
        if self._fl_direction == 'east':
            options += [35]
        elif self._fl_direction == 'west':
            options += [45]
        self.altitude = random.choice(options)