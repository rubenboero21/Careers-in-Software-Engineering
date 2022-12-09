#!/usr/bin/env python3
'''
    flask_sample.py
    Jeff Ondich, 22 April 2016
    Updated 7 October 2020

    A slightly more complicated Flask sample app than the
    "hello world" app found at http://flask.pocoo.org/.
'''
import sys
import argparse
import flask
import json
from flask import *
# import airline
# pip install requests
import requests

app = flask.Flask(__name__)

# come up with a system to combine the month, day, year thing into 1 entry
# flights = [
#     {'number': 1, 'month': 12, 'day': 7, 'year': 2022, 'time': 500},
#     {'number': 167, 'month': 12, 'day': 10, 'year': 2001, 'time': 1700}
# ]

@app.route('/')
def home():
    response = requests.get('http://127.0.0.1:5001/flights')

    flights = json.loads(response.text)
    flightList = []
    for flight in flights:
        flightList.append({'number': flight['number'], 'status': flight['status']})

    return flask.render_template('home.html', flights=flightList)

# https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask
@app.route('/check_in', methods = ["POST"])
def check_in():
    flight_num = int(request.form['flight_number'])
    # make a post to the airline server, give it the id of the flight so we dont need to look through all the flights in the list
    requests.post(url = 'http://127.0.0.1:5001/check_in', data = {"flight_number": flight_num})    

    response = requests.get('http://127.0.0.1:5001/flights')

    flights = json.loads(response.text)
    flightList = []
    for flight in flights:
        flightList.append({'number': flight['number'], 'status': flight['status']})
    # print(flightList)
    return flask.render_template('results.html', flights=flightList)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
