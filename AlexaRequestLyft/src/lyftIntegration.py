'''
Created on May 7, 2016

@author: Pavlo Danchuk
'''
import httplib, urllib2, urllib, json, requests
from geopy.geocoders import Nominatim
from helpers import get_bearer_token

address="72 Bowne St, Brooklyn"
intervals = (
    ('weeks', 604800),  # 60  60  24 * 7
    ('days', 86400),    # 60  60  24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

#headers = {
#   'Authorization': 'Bearer gAAAAABXLl70nF3DltGdK32gvOMwcBYyp2TAKQbzsenCvRcDPVJ54PcU9_t0zris5EJm-UJIDpZZvSyOhWNXfNioMkyi1es5f30yMaV-0AihBs8rWh-AhBt-gPQlrl6RoTWyDR2QgHlrab7IhqgXtYjpajBCKv9h-u1C4JjylbG8NJz38Iqi5fV-7W4063qAadKoTD-hdgigflkWcPAvrsf_JblbHWWMhQ==',
#}

#token = "gAAAAABXLl70nF3DltGdK32gvOMwcBYyp2TAKQbzsenCvRcDPVJ54PcU9_t0zris5EJm-UJIDpZZvSyOhWNXfNioMkyi1es5f30yMaV-0AihBs8rWh-AhBt-gPQlrl6RoTWyDR2QgHlrab7IhqgXtYjpajBCKv9h-u1C4JjylbG8NJz38Iqi5fV-7W4063qAadKoTD-hdgigflkWcPAvrsf_JblbHWWMhQ=="
  
#headers = {
#     'Authorization': "Bearer " + token
# }


 

def get_ride_info(session,start_latitude,start_longitude,end_latitude,end_longitude):

 headers = {
    'Authorization': "Bearer " + get_bearer_token(session),
 }
 URL='https://api.lyft.com/v1/cost?start_lat={}&start_lng={}&end_lat={}&end_lng={}'.format(start_latitude,start_longitude,end_latitude,end_longitude)
 req = urllib2.Request(URL, headers=headers)
 response = urllib2.urlopen(req)
 the_page = response.read()
 data = json.loads(the_page)
 #for key, value in data.items():
# print key, value
 return data

def cost(data):
 estimated_cost_cents_max=data['cost_estimates'][1]['estimated_cost_cents_max']
 total_max=estimated_cost_cents_max/100
 if str(data['cost_estimates'][1]['currency']) == 'USD':
  currency='dollars'
 else:
    currency='of unknown currency'
 print total_max 
 return "Your estimated cost is {}".format(total_max)+ " " +currency

def estimated_distance_miles(data):
 print "Your estimated miles is {}".format(data['cost_estimates'][1]['estimated_distance_miles'])

def estimated_duration_seconds(data):
 print "Your estimated duration is {}".format(display_time(data['cost_estimates'][1]['estimated_duration_seconds']))

def closest_driver(heades,start_latitude,start_longitude,end_latitude,end_longitude):
 print "Checking for it"



def geo(address="175 5th Avenue NYC"):
 geolocator = Nominatim()
 location = geolocator.geocode(address)
 print(location.address)
 print((location.latitude, location.longitude))
 return location.latitude, location.longitude
