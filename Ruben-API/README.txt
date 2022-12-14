Setup of virtual environment:
    1. Create the virtual environment
        * python3 -m venv myvenv
            * where myvenv is whatever name you want to give it
        * source myvenv/bin/activate
    2. Install the dependencies
        * pip install -r requirements.txt
    3. To view all the libraries installed in the virtual environment, type 'pip freeze' into the terminal
    3. When finished with the virtual environment, type 'deactivate' into the terminal

Get the flask server running:
    1. Navigate to the directory that contains the flask app
    2. In the terminal type the following
        python3 <name of the flask app> 127.0.0.1 <port number>
    3. To deactivate the server, type 'control + c' in the terminal that is running the server

NOTE:
    The airline_client.py assumes that the website server is running on port 5001.

