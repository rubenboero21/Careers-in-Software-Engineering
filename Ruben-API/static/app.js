window.onload = initialize;

function initialize() {
    loadFlights();
}

function loadFlights() {
    // this means that the airline server needs to be run on port 5001
    let url = 'http://127.0.0.1:5001/flights';

    fetch(url, {method: 'get'})

    .then((response) => response.json())
    
    .then(function(flights) {
        let flightsList = '';

        for (let k = 0; k < flights.length; k++) {
            let flight = flights[k];
            flightsList += '<p>' + flight['number'] + ': ' + flight['month'] + '/' + flight['day'] + 
            '/' + flight['year'] + ' @' + flight['time'] + ' | Status: ' + flight['status'] + '</p>'
        }

        let selector = document.getElementById('flights');
        if (selector) {
            selector.innerHTML = flightsList;
        }
    })
}
