import argparse
import flask
import json
from flask import *
# memory database:
# https://flask-caching.readthedocs.io/en/latest/#explicitly-caching-data
from flask_caching import Cache

# use a virtual environment when downloading all the libraries

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

# come up with a system to combine the month, day, year thing into 1 entry
# can parse out month/day/year/time in the JS
# flights = [
#     {'number': 1, 'month': 12, 'day': 7, 'year': 2022, 'time': 500, 'status': 'Not Checked In'},
#     {'number': 167, 'month': 12, 'day': 10, 'year': 2001, 'time': 1700, 'status': "Not Checked In"}
# ]

flights = { 1: {'number': 1, 'month': 12, 'day': 7, 'year': 2022, 'time': 500, 'status': 'Not Checked In'}, 
            167: {'number': 167, 'month': 12, 'day': 10, 'year': 2001, 'time': 1700, 'status': "Not Checked In"}}

cache.set("flights", flights)

@app.route('/check_in')
def check_in():
    #given the flight number, edit the dictionary entry
    flight_num = int(request.form['flight_number'])
    flights = cache.get("flights")
    flights[flight_num]['status'] = 'Checked In'
    cache.set("flights", flights)









@app.route('/', methods = ["POST", "GET"])
def test_post():
    if request.method == "POST":
        user = request.form["nm"]
        return flask.render_template('post.html', usr = user)
    else:
        return flask.render_template('post.html')

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route('/flights', methods=['GET'])
def get_flights():
    flight_list = []
    number = flask.request.args.get('number')
    month = flask.request.args.get('month')
    day = flask.request.args.get('day')
    year = flask.request.args.get('year')
    time = flask.request.args.get('time')

    flights = cache.get("flights")
    
    # read about list comprehension
    flight_list = list(flights.values())
    # for flight in flights:
    #     if number is not None and int(number) != flight['number']:
    #         continue
    #     if month is not None and int(month) != flight['month']:
    #         continue
    #     if day is not None and int(day) != flight['day']:
    #         continue
    #     if year is not None and int(year) != flight['year']:
    #         continue
    #     if time is not None and int(time) != flight['time']:
    #         continue
    #     flight_list.append(flight)
    
    # need to provide a header in the API that allows for CORS
    flight_list = flask.jsonify(flight_list)
    flight_list.headers.add('Access-Control-Allow-Origin', '*')

    return flight_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)