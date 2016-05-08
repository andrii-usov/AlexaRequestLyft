'''
Created on May 7, 2016

@author: Pavlo Danchuk
'''
from helpers import send_request, new_geo


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

to_address="175 5th Avenue NYC"
ride_type="lyft_line"

def get_cost_data(session):
 ride_type="lyft_line"
 start_latitude, start_longitude=new_geo() #geo()
 to_address = session['attributes']['destination']
 end_latitude, end_longitude = new_geo(to_address) #geo(to_address)
 request_string = 'cost?start_lat={}&start_lng={}&end_lat={}&end_lng={}&ride_type={}'.format(start_latitude,start_longitude,end_latitude,end_longitude,ride_type)
 data = send_request(session, request_string)
 return data

def get_cost(data): 
 estimated_cost_cents_max=data['cost_estimates'][0]['estimated_cost_cents_max']
 total_max=estimated_cost_cents_max/100
 if str(data['cost_estimates'][0]['currency']) == 'USD':
  currency='dollars'
 else:
    currency='of unknown currency'
 print total_max 
 print "Your estimated cost is {}".format(total_max)+ " " +currency
 return "{} {}".format(total_max, currency)

def estimated_distance_miles(data):
# return "Your estimated miles is {}".format(data['cost_estimates'][0]['estimated_distance_miles'])
  return data['cost_estimates'][0]['estimated_distance_miles']

def estimated_duration_seconds(data):
# return "Your estimated duration is {}".format(display_time(data['cost_estimates'][0]['estimated_duration_seconds']))
  return display_time(data['cost_estimates'][0]['estimated_duration_seconds'], granularity=0)

def get_eta_data(session):
  
 start_latitude, start_longitude=new_geo() #geo()

 request_string = 'eta?lat={}&lng={}&ride_type={}'.format(start_latitude,start_longitude,ride_type)
 data = send_request(session, request_string)
 return data
 
def get_closest_driver(data):
 return display_time(data['eta_estimates'][0]['eta_seconds'])
