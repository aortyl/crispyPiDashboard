import requests
import json
import os

ROOT = 'http://api.wunderground.com/api'
API_KEY = os.environ['WU_API_KEY']
ACTION = '/geolookup/conditions/q'
LOCATION = '/PA/Pennsburg'
DATA_TYPE = '.json'
URL = ROOT + '/' + API_KEY + ACTION + LOCATION + DATA_TYPE

response = requests.get(URL)
current_observation = response.json()['current_observation']

print "Weather for: {}".format(current_observation['display_location']['full'])
print "Temp: {}f".format(current_observation['temp_f'])
print "Feels like: {}f".format(current_observation['feelslike_f'])
