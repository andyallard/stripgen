from flask import Flask, render_template, redirect, url_for
import random
import utils
from models import Scenario, Scenario_DA_DA

app1 = Flask(__name__)

basic_data = utils.import_basic_data()


@app1.route("/")
# @login_required
def index():
    data = ''
    return render_template("index.html", data=data)

@app1.route("/random")
def random_strip():
    option = random.choices(
            ['arrival', 'departure', 'overflight'],
            weights = [4, 3, 1],
            k = 1
        )
    return redirect(url_for(option[0]))

@app1.route("/arrival")
def arrival():
    data = dict()

    scenario = Scenario(basic_data)
    scenario.set_title('Distant Arrival')
    scenario.add_aircraft()
    scenario.add_departure()
    scenario.add_distant_arrival()
    scenario.add_distant_arrival()
    scenario.add_overflight()
    scenario.add_overflight()
    scenario.add_circuit()
    scenario.add_departure()
    scenario.add_departure()

    print(scenario)

    data['determinedrunway'] = f"{utils.determine_runway(scenario.weather.direction, 'wind')}"
    data['striprunway'] = data['determinedrunway']
    data['strip'] = utils.generate_distant_arrival_strip(scenario.time, basic_data['locations'], data)
    data['phraseology'] = utils.generate_phraseology(data, scenario)
    data['phraseology'] = data['phraseology'].replace('\n', '<br>')
    data['response'] = utils.generate_response(data)
    data['response'] = data['response'].replace('\n', '<br>')
    data['strip']['comments'] = data['strip']['comments'].replace('\n', '<br>')

    if data['strip']['comments'] == '':
        data['strip']['comments'] = f'Pass this as traffic in an advisory to {random.choice(utils.aircraft_types)} {scenario.aircraft['aircraft2'].ident}'

    return render_template("scenario.html", data=data, scenario=scenario)


@app1.route("/departure")
def departure():
    scenario = Scenario(basic_data)
    scenario.set_title('Departure')
    
    data = dict()

    data['strip'] = utils.generate_departure_strip(scenario.time, basic_data['locations'])

    data['determinedrunway'] = f"{utils.determine_runway(scenario.weather.direction, 'wind')}"
    data['striprunway'] = data['determinedrunway']
    data['phraseology'] = utils.generate_phraseology(data, scenario)


    if data['strip']['comments'] == '':
        data['strip']['comments'] = f'Pass this as traffic in an advisory to {random.choice(utils.aircraft_types)} {utils.generate_identifier()}'

    if data['strip']['timesincedeparture'] >= 0:
        data['strip']['comments'] = f"Expected to depart in {data['strip']['timesincedeparture']} min\n" + data['strip']['comments']
        data['strip']['arrdeptime'] = ''


    data['phraseology'] = data['phraseology'].replace('\n', '<br>')
    data['response'] = utils.generate_response(data)
    data['response'] = data['response'].replace('\n', '<br>')
    data['strip']['comments'] = data['strip']['comments'].replace('\n', '<br>')

    return render_template("scenario.html", data=data, scenario=scenario)


@app1.route("/circuit")
def circuit():
    scenario = Scenario(basic_data)
    scenario.set_title('Circuit')
    scenario.add_circuit()
    return render_template("scenario.html", scenario=scenario, show_circuit=True)


@app1.route("/overflight")
def overflight():
    scenario = utils.Scenario(basic_data)
    scenario.set_title('Overflight')
    print(scenario)
    data = dict()

    data['strip'] = utils.generate_overflight_strip(scenario.time, basic_data['locations'], basic_data['opposing_directions'])

    data['determinedrunway'] = f"{utils.determine_runway(scenario.weather.direction, 'wind')}"
    data['striprunway'] = f'{88:02}'
    data['phraseology'] = utils.generate_phraseology(data, scenario)
    data['phraseology'] = data['phraseology'].replace('\n', '<br>')
    data['response'] = utils.generate_response(data)
    data['response'] = data['response'].replace('\n', '<br>')
    if data['strip']['comments'] == '':
        data['strip']['comments'] = f'Pass this as traffic in an advisory to {random.choice(utils.aircraft_types)} {utils.generate_identifier()}'
    data['strip']['comments'] = data['strip']['comments'].replace('\n', '<br>')
    return render_template("scenario.html", data=data, scenario=scenario, time=scenario.time)

@app1.route("/createscenario")
def create_scenario():
    scenario = Scenario_DA_DA(basic_data)
    scenario.set_title('Distant Arrival > Distant Arrival')
    # scenario.add_aircraft()
    # scenario.add_distant_arrival()
    # scenario.add_overflight()
    # scenario.add_circuit()
    # scenario.add_departure()
    # scenario.add_departure()
    # scenario.add_departure()
    # scenario.add_departure()

    print(scenario)
    return render_template("createscenario.html", scenario=scenario)