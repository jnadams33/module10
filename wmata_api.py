from flask import Flask
import json
import requests

# API endpoint URL's and access keys
WMATA_API_KEY = "29f27952decd422e901f8c8f5f2bba77"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"]) # http://127.0.0.1:5000/incidents/ELEVATOR
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents_list = []
    unit_type = unit_type[:-1].upper()

    # use 'requests' to do a GET request to the WMATA Incidents API
    # retrieve the JSON from the response
    response_incidents = requests.get(INCIDENTS_URL, headers=headers)
    incidents = response_incidents.json()["ElevatorIncidents"]

    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
    # StationCode, StationName, UnitType, UnitName
    # add each incident dictionary object to the 'incidents' list
    for incident in incidents:
        if incident["UnitType"] == unit_type:
            incident_dict = {
                'StationCode': incident['StationCode'],
                'StationName': incident['StationName'],
                'UnitType': incident['UnitType'],
                'UnitName': incident['UnitName']
            }
            incidents_list.append(incident_dict)

    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents_list)

if __name__ == '__main__':
    app.run(debug=True)

