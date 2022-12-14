'''
    airline_client.py
    Ruben Boero 12/10/2022

    Thanks to David Lonoff for the massive help with this project.
'''

import json
import requests
import flask
from flask import request, redirect
import time

def get_all_flights(endpoint):
    response = requests.get(endpoint)
    flights = json.loads(response.text)
    flightsDict = dict(flights)
    flightList = []
    
    for flight in flightsDict:
        flightList.append({'number': flightsDict[flight]['number'], 'status': flightsDict[flight]['status']})

    return flightList

def check_in_flight():
    # get the flight number from the form
    flight_num = request.form['flight_number']

    # check that the user has input an integer
    if not flight_num.isdigit():  
        # is there a way to only get the flights that match the number instead of getting a list of all flights?
        # yes -- optional parameters -- ?number=x
        # DO THIS AFTER CHECK IN LOGIC IS WORKING
        flightList = get_all_flights('http://127.0.0.1:5001/flights')
     
        return flask.render_template('error.html', inputError=True, flights=flightList)
    
    flight_num = int(request.form['flight_number'])

    check_in_response = requests.post(url = 'http://127.0.0.1:5001/check_in', data = {"flight_number": flight_num})    
    eligibility = check_in_response.json()['status']
    
    if eligibility == 'succeeded':
        return redirect('/')
    
    else:
        print('flight not checked in. checking again in 60 seconds')
        time.sleep(60)

        while True:
            print('attempting checkin')
            check_in_response = requests.post(url = 'http://127.0.0.1:5001/check_in', data = {"flight_number": flight_num})    
            eligibility = check_in_response.json()['status']
            if eligibility == 'succeeded':
                print('successfully checked in')
                break
            else:
                time.sleep(60)

        return redirect('/')