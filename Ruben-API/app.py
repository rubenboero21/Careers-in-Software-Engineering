#!/usr/bin/env python3
'''
    app.py
    Ruben Boero 12/10/2022
'''
import sys
import argparse
import flask
import json
from flask import *

# pip install requests
import requests

# how are these 2 import statement different?
from datetime import datetime, timedelta
import datetime

app = flask.Flask(__name__)

def getAllFlights(endpoint):
    response = requests.get(endpoint)
    flights = json.loads(response.text)
    flightsDict = dict(flights)
    flightList = []
    
    for flight in flightsDict:
        flightList.append({'number': flightsDict[flight]['number'], 'status': flightsDict[flight]['status']})

    return flightList

@app.route('/')
def home():
    flightList = getAllFlights('http://127.0.0.1:5001/flights')

    return flask.render_template('home.html', flights=flightList)

# https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask
@app.route('/check_in', methods = ["POST", "GET"]) # why dont i need to include the GET method?
def check_in():
    # get the flight number from the form
    flight_num = request.form['flight_number']

    # check that the user has input an integer
    if not flight_num.isdigit():  
        # is there a way to only get the flights that match the number instead of getting a list of all flights?
        # yes -- optional parameters -- ?number=x
        # DO THIS AFTER CHECK IN LOGIC IS WORKING
        flightList = getAllFlights('http://127.0.0.1:5001/flights')
     
        return flask.render_template('error.html', inputError=True, flights=flightList)
    
    flight_num = int(request.form['flight_number'])

    # when implementing automation, allow the check in process to occur more than 24 hours out, but 
    # only start pinging the airline API within 24 hoursCHECKIN_UNAVAILABLE, CHECKIN_AVAILABLE, or CHECKED_IN
    # only allow check in if flight is within 24 hours
    check_in_response = requests.post(url = 'http://127.0.0.1:5001/check_in', data = {"flight_number": flight_num})    
    eligibility = check_in_response.json()['status']
    
    if eligibility == 'succeeded':
        return redirect('/')
    
    else:
        # what actually needs to happen here is to wait, then attempt to check in again
        print('flight not checked in')
        return redirect('/')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
