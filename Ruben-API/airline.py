import argparse
import flask
import json
from flask import *
# memory database:
# https://flask-caching.readthedocs.io/en/latest/#explicitly-caching-data
# pip install Flask-Caching
from flask_caching import Cache

# how are these 2 import statement different?
from datetime import datetime, timedelta
import datetime

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

flights = { 1: {'number': 1, 'month': 12, 'day': 7, 'year': 2023, 'time': 500,  
                'combinedTime': '2023-12-7-5', 'status': 'Not Checked In'}, 
            167: {'number': 167, 'month': 12, 'day': 10, 'year': 2022, 'time': 1700,
                'combinedTime': '2022-12-10-17','status': "Not Checked In"}
          }

cache.set("flights", flights)

@app.route('/check_in/<flight_number>', methods=['POST', 'GET'])
def check_in(flight_number):
    #given the flight number, edit the dictionary entry
    flights = cache.get("flights")
    flights[int(flight_number)]['status'] = 'Checked In'

    cache.set("flights", flights)

    # return that the flight has been checked in successfully so the auto retry in app.py can be terminated?
    # what to return here?
    return flights

@app.route('/flights', methods=['GET'])
def get_flights():
    flight_list = []

    flights = cache.get("flights")
    
    # read about list comprehension
    # flight_list = list(flights.values())
    flight_list = flights
    
    # need to provide a header in the API that allows for CORS
    flight_list = flask.jsonify(flight_list)
    flight_list.headers.add('Access-Control-Allow-Origin', '*')

    return flight_list

# add a route that checks if a flight can be checked in
# have the auto check in ping this route from the check in route in app.py

# should this route be combined with the /check_in route?
@app.route('/check_in_eligibility/<flight_number>', methods=['POST'])
def check_in_eligibility(flight_number):

    flights = cache.get("flights")

    flight_time = flights[int(flight_number)]['combinedTime']
    indiv = flight_time.split('-')
    year = int(indiv[0])
    month = int(indiv[1])
    day = int(indiv[2])
    hour = int(indiv[3])
    # can add minutes and seconds later if needed

    flight_time = datetime.datetime(year, month, day, hour)
    current_time = datetime.datetime.now()
    one_day_away = current_time + timedelta(days = 1)

    if flight_time <= one_day_away:
        return redirect('http://127.0.0.1:5001/check_in/' + str(flight_number))

    # NEXT THING TO DO IS CHECK THAT THE FLIGHT IS WITHIN 24 HOURS
    # IF IT IS, FORWARD THE FLIGHT NUNBER TO THE CHECK IN ENDPOINT

    # real return statement should be a redirection to the /check_in enpoint
    # edit the endpoint to take in the flight number 
    else:
        # what should i return? it needs to be something that allows our website to know to keep trying
        return flights

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)