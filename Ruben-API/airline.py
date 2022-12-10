import argparse
import flask
import json
from flask import *
# memory database:
# https://flask-caching.readthedocs.io/en/latest/#explicitly-caching-data
# pip install Flask-Caching
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

flights = { 1: {'number': 1, 'month': 12, 'day': 7, 'year': 2023, 'time': 500,  
                'combinedTime': '2023-12-7-5', 'status': 'Not Checked In'}, 
            167: {'number': 167, 'month': 12, 'day': 10, 'year': 2022, 'time': 1700,
                'combinedTime': '2022-12-10-17','status': "Not Checked In"}
          }

cache.set("flights", flights)

@app.route('/check_in', methods=['POST'])
def check_in():
    print('made it')
    #given the flight number, edit the dictionary entry
    flight_num = int(request.form['flight_number'])
    flights = cache.get("flights")
    flights[flight_num]['status'] = 'Checked In'
    cache.set("flights", flights)

    print(cache)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)