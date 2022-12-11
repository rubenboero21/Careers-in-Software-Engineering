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

    # is there a way to only get the flights that match the number instead of getting a list of all flights?
    # yes -- optional parameters -- ?number=x
    # DO THIS AFTER CHECK IN LOGIC IS WORKING
    # or could leave it as is and store the flights in a DB, then query the DB
    response = requests.get('http://127.0.0.1:5001/flights')
    flights = json.loads(response.text)
    flightsDict = dict(flights)

    # get the flight number from the form
    flight_num = request.form['flight_number']

    # check that the user has input an integer
    if not flight_num.isdigit():  
        flightList = getAllFlights('http://127.0.0.1:5001/flights')
     
        return flask.render_template('error.html', inputError=True, flights=flightList)
    
    flight_num = int(request.form['flight_number'])

    # only check the flight that matches the number input from the form
    current_time = datetime.datetime.now()

    flight_time = flightsDict[str(flight_num)]['combinedTime']
    indiv = flight_time.split('-')
    year = int(indiv[0])
    month = int(indiv[1])
    day = int(indiv[2])
    hour = int(indiv[3])
    # can add minutes and seconds later if needed

    flight_time = datetime.datetime(year, month, day, hour)

    one_day_away = current_time + timedelta(days = 1)

    # when implementing automation, allow the check in process to occur more than 24 hours out, but 
    # only start pinging the airline API within 24 hoursCHECKIN_UNAVAILABLE, CHECKIN_AVAILABLE, or CHECKED_IN
    # only allow check in if flight is within 24 hours
    if flight_time <= one_day_away: 
        # add the auto retry here
        # need to come up with a way to know that the flight has been successfully checked in
        requests.post(url = 'http://127.0.0.1:5001/check_in/'+str(flight_num), data = {"flight_number": flight_num})    

        # make a get req to show the update to the user
        flightList = getAllFlights('http://127.0.0.1:5001/flights')
        
        return flask.render_template('results.html', flights=flightList)
    else:
        flightList = getAllFlights('http://127.0.0.1:5001/flights')

        return flask.render_template('error.html', timeError=True, number=flight_num, flights=flightList)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
