#!/usr/bin/env python3
'''
    app.py
    Ruben Boero 12/10/2022

    Thanks to David Lonoff for the massive help with this project.
'''
import argparse
import flask
import airline_client

app = flask.Flask(__name__)

@app.route('/')
def home():
    flightList = airline_client.get_all_flights('http://127.0.0.1:5001/flights')

    return flask.render_template('home.html', flights=flightList)

@app.route('/check_in', methods = ["POST", "GET"]) # why dont i need to include the GET method?
def check_in():
    return airline_client.check_in_flight()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
