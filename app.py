from flask import Flask, render_template, redirect, url_for
import random
import helper

app1 = Flask(__name__)

basic_data = helper.import_basic_data()

# fss09 sim workbook

@app1.route("/")
# @login_required
def index():
    # data = execute_sql(
    #     "SELECT * FROM shopping_list "
    #     # "SELECT * FROM shopping_list AS sl "
    #     # "JOIN stores ON sl.store_id = stores.id "
    #     "WHERE user_id = ?", (current_user.get_id()), empty_return=[]
    #     # "WHERE sl.user_id = ?", (current_user.get_id()), empty_return=[]
    #     # "WHERE sl.status != 0;"
    # )
    data = ''
    return render_template("index.html", data=data)


@app1.route("/arrival")
def arrival():
    data = dict()

    class_data = helper.Scenario()
    data['weather'] = class_data.weather

    print('dir! = ', type(class_data.weather.direction), class_data.weather.direction)

    print(class_data)
    time = helper.generate_random_time()
    data['time'] = time.strftime("%H%M")

    data['determinedrunway'] = f"{helper.determine_runway(class_data.weather.direction, 'wind')}"
    data['striprunway'] = data['determinedrunway']
    data['strip'] = helper.generate_distant_arrival_strip(time, basic_data['locations'], data)
    data['phraseology'] = helper.generate_phraseology(data)
    data['phraseology'] = data['phraseology'].replace('\n', '<br>')
    data['response'] = helper.generate_response(data)
    data['response'] = data['response'].replace('\n', '<br>')
    data['strip']['comments'] = data['strip']['comments'].replace('\n', '<br>')

    if data['strip']['comments'] == '':
        data['strip']['comments'] = f'Pass this as traffic in an advisory to {random.choice(helper.aircraft_types)} {helper.generate_identifier()}'

    return render_template("strip.html", data=data)

@app1.route("/departure")
def departure():
    data = dict()

    class_data = helper.Scenario()
    data['weather'] = class_data.weather
    

    time = helper.generate_random_time()
    data['time'] = time.strftime("%H%M")

    data['strip'] = helper.generate_departure_strip(time, basic_data['locations'])
    # data['strip'] = helper.generate_departure_strip(time)

    data['determinedrunway'] = f"{helper.determine_runway(class_data.weather.direction, 'wind')}"
    data['striprunway'] = data['determinedrunway']
    data['phraseology'] = helper.generate_phraseology(data)


    if data['strip']['comments'] == '':
        data['strip']['comments'] = f'Pass this as traffic in an advisory to {random.choice(helper.aircraft_types)} {helper.generate_identifier()}'

    if data['strip']['timesincedeparture'] >= 0:
        data['strip']['comments'] = f"Expected to depart in {data['strip']['timesincedeparture']} min\n" + data['strip']['comments']
        data['strip']['arrdeptime'] = ''


    data['phraseology'] = data['phraseology'].replace('\n', '<br>')
    data['response'] = helper.generate_response(data)
    data['response'] = data['response'].replace('\n', '<br>')
    data['strip']['comments'] = data['strip']['comments'].replace('\n', '<br>')

    return render_template("strip.html", data=data)

@app1.route("/overflight")
def overflight():
    data = dict()
    class_data = helper.Scenario()
    data['weather'] = class_data.weather

    time = helper.generate_random_time()
    data['time'] = time.strftime("%H%M")
    data['strip'] = helper.generate_overflight_strip(time, basic_data['locations'], basic_data['opposing_directions'])

    data['determinedrunway'] = f"{helper.determine_runway(class_data.weather.direction, 'wind')}"
    data['striprunway'] = f'{88:02}'
    data['phraseology'] = helper.generate_phraseology(data)
    data['phraseology'] = data['phraseology'].replace('\n', '<br>')
    data['response'] = helper.generate_response(data)
    data['response'] = data['response'].replace('\n', '<br>')
    if data['strip']['comments'] == '':
        data['strip']['comments'] = f'Pass this as traffic in an advisory to {random.choice(helper.aircraft_types)} {helper.generate_identifier()}'
    data['strip']['comments'] = data['strip']['comments'].replace('\n', '<br>')
    return render_template("strip.html", data=data)

@app1.route("/random")
def random_strip():
    option = random.choices(
            ['arrival', 'departure', 'overflight'],
            weights = [3, 2, 1],
            k = 1
        )
    return redirect(url_for(option[0]))