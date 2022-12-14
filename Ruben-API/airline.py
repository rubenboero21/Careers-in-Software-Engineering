'''
    airline.py
    Ruben Boero 12/10/2022

    Thanks to David Lonoff for the massive help with this project.
'''

import argparse
import json
import flask
from flask import Flask, request
# memory database:
# https://flask-caching.readthedocs.io/en/latest/#explicitly-caching-data
from flask_caching import Cache

from datetime import datetime, timedelta
import datetime

import requests

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)

# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

# combined_time is year-month-day-hour-minute
flights = { 1: {'number': 1,'combined_time': '2022-12-15-10-37', 'status': 'Not Checked In'}, 
            167: {'number': 167, 'combined_time': '2022-12-10-17-0','status': 'Not Checked In'}
          }

cache.set("flights", flights)

def check_in_eligibility(flight_info):
    flight_time = flight_info['combined_time']
    
    indiv = flight_time.split('-')
    year = int(indiv[0])
    month = int(indiv[1])
    day = int(indiv[2])
    hour = int(indiv[3])
    minute = int(indiv[4])

    flight_time = datetime.datetime(year, month, day, hour, minute)

    current_time = datetime.datetime.now()
    one_day_away = current_time + timedelta(days = 1)

    # right now, a flight can be checked in as long as its 24 hours away or less
    if flight_time <= one_day_away:
        # check in allowed
        return True
    else:
        # check in not allowed
        return False

@app.route('/check_in_status/<flight_number>', methods=['GET'])
# check the date for eligibility and return CHECKIN_AVAILABLE etc but don't actually check in
def get_check_in_status(flight_number):
    flights = cache.get("flights")
    flight_number = int(flight_number)

    if check_in_eligibility(flights[flight_number]):
        return {'availability_status': 'CHECKIN_AVAILABLE'}
    else:
        return {'availability_status': 'CHECKIN_UNAVAILABLE'}

@app.route('/check_in', methods=['POST'])
# check in the flight if it can be checked in
def check_in():
    flight_number = int(request.form['flight_number'])

    eligibility_response = requests.get(url = 'http://127.0.0.1:5001/check_in_status/'+str(flight_number))
    eligibility = eligibility_response.json()['availability_status']

    if eligibility == 'CHECKIN_AVAILABLE':
        print('available')
        flights[int(flight_number)]['status'] = 'Checked In'

        cache.set("flights", flights)

        return json.dumps({'status': 'succeeded'})
    
    elif eligibility == 'CHECKIN_UNAVAILABLE':
        print('unavailable')
        return json.dumps({'status': 'failed'})

@app.route('/flights', methods=['GET'])
def get_flights():
    flight_list = cache.get("flights")
    
    # need to provide a header in the API that allows for CORS
    flight_list = flask.jsonify(flight_list)
    flight_list.headers.add('Access-Control-Allow-Origin', '*')

    return flight_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A mock airline API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)