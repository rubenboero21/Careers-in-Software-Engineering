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

@app.route('/')
def home():
    response = requests.get('http://127.0.0.1:5001/flights')
    flights = json.loads(response.text)
    flightsDict = dict(flights)
    flightList = []
    
    for flight in flightsDict:
        flightList.append({'number': flightsDict[flight]['number'], 'status': flightsDict[flight]['status']})

    return flask.render_template('home.html', flights=flightList)

# https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask
@app.route('/check_in', methods = ["POST"]) # why dont i need to include the GET method?
def check_in():

    # is there a way to only get the flights that match the number instead of getting a list of all flights?
    # yes -- optional parameters -- ?number=x
    # DO THIS AFTER CHECK IN LOGIC IS WORKING
    response = requests.get('http://127.0.0.1:5001/flights')
    flights = json.loads(response.text)
    flightsDict = dict(flights)

    # get the flight number from the form
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

    # if the flight is outside of 24 hours, dont allow check in
    if flight_time <= one_day_away:
        print('within 24 hrs')
        # make a post to the airline server, give it the id of the flight so we dont need to look through all the flights in the list
        requests.post(url = 'http://127.0.0.1:5001/check_in', data = {"flight_number": flight_num})    

        # make a get req to show the update to the user
        response = requests.get('http://127.0.0.1:5001/flights')

        flights = json.loads(response.text)
        flightsDict = dict(flights)
        flightList = []
        for flight in flightsDict:
            flightList.append({'number': flightsDict[flight]['number'], 'status': flightsDict[flight]['status']})
        return flask.render_template('results.html', flights=flightList)
    else:
        print('outside of 24 hours')
        # provide a better message to the user
        return redirect('http://127.0.0.1:5000/')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
