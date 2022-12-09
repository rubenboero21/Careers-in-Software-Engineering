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
    return flask.render_template('home.html')

# copy the below code to make a get request to get the list of all flights instead of using JS
# (using the requests libe instead of JS)

# https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask
@app.route('/check_in', methods = ["POST"])
def check_in():
    flight_num = int(request.form['flight_number'])
    # make a post to the airline server, give it the id of the flight so we dont need to look through all the flights in the list
    requests.post(url = 'http://127.0.0.1:5001/check_in', data = {"flight_number": flight_num})    
    # flights = airline.flights
    # for count, flight in enumerate(flights):
    #     if flight['number'] == flight_num:
    #         thisDict = airline.flights[count]
    #         thisDict.update({'status': 'Checked In'})
    #         airline.flights[count] = thisDict
    #         print(airline.flights[count])

    return flask.render_template('results.html', flight_num=flight_num)


    # num = request.form["flight_number"]

# @app.route('/', methods = ["POST", "GET"])
# def test_post():
#     if request.method == "POST":
#         user = request.form["nm"]
#         return flask.render_template('post.html', usr = user)
#     else:
#         return flask.render_template('post.html')

# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"

# @app.route('/flights')
# def get_flights():
#     flight_list = []
#     number = flask.request.args.get('number')
#     month = flask.request.args.get('month')
#     day = flask.request.args.get('day')
#     year = flask.request.args.get('year')
#     time = flask.request.args.get('time')
#     for flight in flights:
#         # print(number, flight['number'])
#         if number is not None and int(number) != flight['number']:
#             continue
#         # print(month, flight['month'])
#         if month is not None and int(month) != flight['month']:
#             continue
#         if day is not None and int(day) != flight['day']:
#             continue
#         if year is not None and int(year) != flight['year']:
#             continue
#         if time is not None and int(time) != flight['time']:
#             continue
#         flight_list.append(flight)

#     return json.dumps(flight_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
