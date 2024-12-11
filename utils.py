import random
import csv
import os
import string
from datetime import datetime, timedelta

aircraft_types = [
    "BE20", "BE76", "C150", "C172", "C182", "C185", "C206", "C208", "C210", "C421", "C550",
    "DHC2", "DHC6", "DV20", "PC12", "P28A", "PA31", "PA34", "PAY2",
    "B190", "DH8A", "DH8B", "DH8C", "DH8D", "SW4", "C130", "SF34",
    "A320", "B737", "CRJ1", "CL60", "E175", "LJ35", "B06", "R44", "H46",
]

march = {
        "location": "CYMR", "common name": "MARCH", "compass point": "N", "distance (NM)": 0, "bearing": 0
    }


# Get the absolute path to the current directory of helper.py
base_dir = os.path.dirname(__file__)

def import_basic_data():

    csv_file_path = os.path.join(base_dir, 'data', 'joining_procedures.csv')
    with open(csv_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        joining_procedures = {
            (row["Runway"], row["Direction"]): row["Procedure"]
            for row in reader
        }

    csv_file_path = os.path.join(base_dir, 'data', 'opposing_directions.csv')
    opposing_directions = {}
    with open(csv_file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:  # Ensure that the row has two columns
                key, value = row
                opposing_directions[key] = value

    csv_file_path = os.path.join(base_dir, 'data', 'locations.csv')
    with open(csv_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        int_fields = ['distance (NM)', 'bearing']
        locations = [
            {key: int(value) if key in int_fields else value for key, value in row.items()}
            for row in reader
        ]

    march = {
        "location": "CYMR", "common name": "MARCH", "compass point": "N", "distance (NM)": 0, "bearing": 0
    }

    basic_data = {
        'joining_procedures': joining_procedures,
        'opposing_directions': opposing_directions,
        'locations': locations,
        'march': march
    }

    return basic_data






















def generate_phraseology(data, class_data):
    strip = data['strip']
    phraseology = f"RUNWAY {data['determinedrunway']}"
    wind = str(class_data.weather.print_wind()) if class_data.weather.wind_speed >= 3 else 'CALM'
    phraseology += f'\nWIND {wind}'
    phraseology += f"\nALTIMETER {class_data.weather.print_altimeter()}"
    
    if (2899 >= class_data.weather.altimeter) or (class_data.weather.altimeter >= 3100):
        phraseology +=f" I SAY AGAIN ALTIMETER {class_data.weather.print_altimeter()}"
    phraseology += '\n\nTRAFFIC'

    if strip['type'] == 'A':
        if strip['exactpositionrequired']:
            phraseology += f'[say exact position] [how long ago they reported]'
        else:
            phraseology += f"\nINBOUND FROM THE {strip['pointofdeparture']['compass point']}"
        phraseology += f"\n{strip['aircrafttype']}"
        if strip['needaltitude']:
            phraseology += f"\nALTITUDE {strip['altitude'] * 100}"
        phraseology += f"\nESTIMATING IN {strip['estimatingin']} MINUTE"
        if strip['estimatingin'] != 1:
            phraseology += 'S'
        phraseology += f'\nWILL JOIN [how they will join]'
    elif strip['type'] == 'D':
        if strip['timesincedeparture'] == 0:
            phraseology += f"\n(ABOUT TO DEPART / ENTERING) RUNWAY {data['determinedrunway']}"
        elif strip['timesincedeparture'] < 0:
            phraseology += f"\nDEPARTED {-strip['timesincedeparture']} MINUTE"
            if -strip['timesincedeparture'] != 1:
                phraseology += 'S'
            phraseology += ' AGO'
        else:
            phraseology += f"\nTAXIING FOR DEPARTURE RUNWAY {data['determinedrunway']}"
        phraseology += f"\n{strip['destination']['compass point']} BOUND"
        phraseology += f"\n{strip['aircrafttype']}"
        if strip['needaltitude']:
            phraseology += f"\nPLANNING {strip['altitude'] * 100}"
    elif strip['type'] == 'O':
        phraseology += f"\nINBOUND FROM THE {strip['pointofdeparture']['compass point']}"
        phraseology += f"\n{strip['destination']['compass point']} BOUND"
        phraseology += f"\n{strip['aircrafttype']}"
        phraseology += f"\nESTIMATING OVERHEAD IN {strip['estimatingin']} MINUTE"
        if strip['estimatingin'] != 1:
            phraseology += 'S'
        phraseology += f'\nTRANSITING THE ZONE'

    return phraseology

def generate_response(data):
    strip = data['strip']
    response = 'ROGER RUNWAY [their intended runway]\n'
    if strip['reportingpointrequired']:
        response += f'REPORT (over/abeam/etc) [reporting point]\n'
    return response



def generate_strip():
    strip = dict()
    strip['identifier'] = generate_identifier()
    strip['aircrafttype'] = random.choice(aircraft_types)
    strip['comments'] = ''
    strip['needaltitude'] = False
    strip['reportingpointrequired'] = False
    strip['exactpositionrequired'] = False
    strip['timesincedeparture'] = ''
    return strip



def generate_departure_strip(time, locations):
    strip = generate_strip()
    strip['pointofdeparture'] = march
    strip['destination'] = random.choice(locations)
    # print(strip['destination'])
    strip['type'] = 'D'
    strip['arrdeptime'], strip['timesincedeparture'] = generate_departure_time(time)

    if 0 <= strip['destination']['bearing'] < 180:
        strip['FLdirection'] = 'east'
    else:
        strip['FLdirection'] = 'west'
    strip['altitude'] = generate_altitude(strip['FLdirection'])

    if random.random() > 0.667:
        strip['comments'] += f"We are passing this aircraft as traffic in an advisory to {random.choice(aircraft_types)} {generate_identifier()} at {generate_altitude() * 100} feet inbound from the {strip['destination']['compass point']}\n"
        strip['needaltitude'] = True
        strip['reportingpointrequired'] = True

    # strip['determinedrunway'] = f"\n{determine_runway(strip['destination'], 'location')}"

    # print(strip)

    return strip

def generate_overflight_strip(time, locations, opposing_directions):
    strip = generate_strip()
    strip['destination'] = random.choice(locations)
    strip['type'] = 'O'
    strip['estimatedarrival'], strip['estimatingin'] = generate_arrival_time(time)

    possible_opposing_departures = [l for l in locations if opposing_directions[l['compass point']] == strip['destination']['compass point']]

    strip['pointofdeparture'] = random.choice(possible_opposing_departures)

    if 180 <= strip['destination']['bearing'] < 360:
        strip['FLdirection'] = 'west'
    else:
        strip['FLdirection'] = 'east'
    strip['altitude'] = generate_overflight_altitude(strip['FLdirection'])

    # if random.random() > 0.667:
    #     strip['comments'] += f"We are passing this aircraft as traffic in an advisory to to a departing {strip['pointofdeparture']['compass point']} bound aircraft\n"
    #     strip['needaltitude'] = True
    # else:
    #     inbound_location = random.choice(locations)
    #     if inbound_location['compass point'] == strip['pointofdeparture']['compass point']:
    #         strip['exactpositionrequired'] = True
    #     strip['comments'] += f"We are passing this aircraft as traffic in an advisory to to {generate_identifier()} inbound from the {inbound_location['compass point']}\n"
    #     strip['reportingpointrequired'] = True

    return strip


def generate_distant_arrival_strip(time, locations, data):
    strip = generate_strip()
    strip['pointofdeparture'] = random.choice(locations)
    strip['destination'] = march
    strip['type'] = 'A'
    strip['estimatedarrival'], strip['estimatingin'] = generate_arrival_time(time)
    # strip['joining'] = determine_joining_procedure(data)

    if 0 <= strip['pointofdeparture']['bearing'] < 180:
        strip['FLdirection'] = 'west'
    else:
        strip['FLdirection'] = 'east'
    strip['altitude'] = generate_altitude(strip['FLdirection'])

    if random.random() > 0.667:
        strip['comments'] += f"We are passing this aircraft as traffic in an advisory to {random.choice(aircraft_types)} {generate_identifier()}, a departing {strip['pointofdeparture']['compass point']} bound aircraft planning {generate_altitude() * 100} feet\n"
        strip['needaltitude'] = True
    else:
        inbound_location = random.choice(locations)
        if inbound_location['compass point'] == strip['pointofdeparture']['compass point']:
            strip['exactpositionrequired'] = True
        strip['comments'] += f"We are passing this aircraft as traffic in an advisory to {random.choice(aircraft_types)} {generate_identifier()} at {generate_altitude() * 100} feet inbound from the {inbound_location['compass point']}\n"
        strip['reportingpointrequired'] = True

    # print(strip)

    return strip



# def determine_joining_procedure(data):
#     joining = joining_procedures[(data['determinedrunway'], data['strip']['location']['compass point'])]
#     print(joining)
#     return joining























def generate_departure_time(time):
    estimating = random.randint(-2, 3)
    departure_time = time + timedelta(minutes=estimating)
    return departure_time.strftime("%H%M"), estimating

def determine_runway(value, type):
    if type == 'location':
        dir = value['bearing']
    elif type == 'wind':
        dir = int(value)
    runways = (90, 140, 270, 320)
    differences = [bearing_difference(dir, runway) for runway in runways]
    runway = runways[differences.index(min(differences))]
    # print(f'runway, differences = {runway}, {differences}')
    runway = int(runway / 10)
    return f'{runway:02}'

def bearing_difference(bearing1, runway):
    difference = abs(runway - bearing1)
    if difference > 180:
         difference = 360 - difference
    # print(f'difference between {bearing1} and {runway} is {difference}')
    return difference
    


def generate_identifier():
    first_letter = 'C'
    second_letter = random.choice(['F', 'G'])
    remaining_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    return f"{first_letter}{second_letter}{remaining_letters}"


def generate_arrival_time(time):
    values = list(range(5, 20))
    weights = [(20 - i) for i in values]

    # Normalize weights to make them a proper probability distribution
    weights = [w / sum(weights) for w in weights]

    # Generate a random number with the specified weights
    estimating = random.choices(values, weights=weights, k=1)[0]
    arrival_time = time + timedelta(minutes=estimating)
    return arrival_time.strftime("%H%M"), estimating


def generate_altitude(FLdirection=None):
    if FLdirection is None:
        FLdirection = random.choice(['east', 'west'])
    altitude = random.randint(2, 6)
    altitude *= 20
    altitude += 5
    if FLdirection == 'east':
        altitude -= 10
    return altitude

def generate_overflight_altitude(FLdirection):
    options = [28, 29, 30]
    if FLdirection == 'east':
        options += [35]
    elif FLdirection == 'west':
        options += [45]
    # print(options)
    return random.choice(options)



