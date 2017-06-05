import sys
import requests
import time
import json
import datetime
from optparse import OptionParser

sparkpost_key = 'e2108ac9af6c244f192003ff5ea51a791cb755b3'

url = 'https://api.sparkpost.com/api/v1/transmissions'

data = {'content': {'from': 'postmaster@birdcall.tech', 'subject': 'Bird Sighting!', 'text': 'Found a bird'},
        'recipients': [{'address': 'matis.kleidman@gmail.com'}]}

#response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json", "Authorization": sparkpost_key})
#print "response", response.status_code, response.content

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--days", dest="back", help="number of days back to search for", type="int", default=3)
    parser.add_option("-z", "--zip", dest="zip", help="zip code to center search on", type="str", default=20902)
    parser.add_option("-r", "--radius", dest="radius", help="number of miles around the center to search for", type="int", default=20)
    parser.add_option("-s", "--sort", dest="sort", help="which column to sort by (options are 'species', 'location', 'time')", default="time")
    (options, args) = parser.parse_args()
    skip_list = ['shorebird sp.', 'sparrow sp.', 'swallow sp.', 'Turkey Vulture', 'House Sparrow', 'House Finch', 'crow sp.',
                 'Carolina Chickadee', 'Blue Jay', 'Mourning Dove', 'duck sp.', 'European Starling', 'Canada Goose',
                 'Rock Pigeon', 'Tufted Titmouse', 'gull sp.', 'Song Sparrow', 'Common Grackle', 'American Robin',
                 'American Crow', 'Gray Catbird', 'hawk sp.', 'Ring-billed Gull', 'Black Vulture']
    token = '9srotnmom2PWzfEojPRgmDrAj8plJjZTLqieNEDaGs6fHLE1BvhY9JysRXOBhNv2'
    response = requests.get("https://www.zipcodeapi.com/rest/" + token + '/info.json/' + str(options.zip) + '/degrees').json()
    params = {"lat": response['lat'], "lng": response['lng'], "fmt": "json", "dist": options.radius, "back": options.back}
    response = requests.get("http://ebird.org/ws1.1/data/obs/geo/recent", params=params).json()
    sort_map = {'species': 'comName', 'location': 'locName', 'time': 'obsDt'}
    for obs in sorted(response, key=lambda x: x[sort_map[options.sort]], reverse=True):
        if obs['comName'] in skip_list:
            continue
        print '%s\t  %s\t  %s' %(obs['comName'], obs['locName'], obs['obsDt'])
     
