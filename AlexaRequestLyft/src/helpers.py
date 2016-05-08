'''
Created on May 7, 2016

@author: Andrii Usov
'''
import json, requests, urllib2, urllib
from geopy.geocoders import Nominatim

# --------------- Helpers that process requests ----------------------

def get_stage_number(session):
    if session.has_key('attributes') == False or session['attributes'].has_key('stage') == False:
        return "0"
    else:
        return session['attributes']['stage']


data = { "new": "False", "attributes":{"stage": "1"}}
print(get_stage_number(data))
def get_access_token(session):
    try:
        token = session['user']['accessToken'] 
        return token
    except:
        raise ValueError("Session should contain access token")

def get_bearer_token(session):
    try:
        token = session['user']['bearerToken'] 
        return token
    except:
        token = request_bearer_token()
        session['user']['bearerToken'] = token
        return token
        
def request_bearer_token():
 data={"grant_type": "client_credentials", "scope": "public"}
 data=json.dumps(data)

 header={
 'Content-Type': 'application/json',
 }

 client_id="9hSQ_cQtVmlr"
 client_secret="qEUMe7sCOV4_-wVAlfOTF8qc-1sRoiLm"
 
 req=requests.post('https://api.lyft.com/oauth/token',auth=(client_id, client_secret), data=data, headers=header)
 req.status_code
 return req.json()['access_token']
 

def send_request(session, request_string): 

 headers = {
    'Authorization': "Bearer " + get_bearer_token(session),
 }
 URL="https://api.lyft.com/v1/" + request_string
 
 req = urllib2.Request(URL, headers=headers)
 response = urllib2.urlopen(req)
 the_page = response.read()
 data = json.loads(the_page)
 #for key, value in data.items():
# print key, value
 return data
 

def geo(address="72 Bowne St, Brooklyn"):
 geolocator = Nominatim()
 location = geolocator.geocode(address)
 print(location.address)
 print((location.latitude, location.longitude))
 return location.latitude, location.longitude

def new_geo(address="72 Bowne St, Brooklyn"):
 URL="http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find?text=" + address + "&forStorage=true&token='1qy2qStzlXL-wgxROBy9d5p8eicSuhmBxYFZ2wwOhB-RF006gMETEUmc_IoV1rmAR6poqEl8yfJp7Ez8PJMTuiBV3VNtP1Evd_o8DmETQnVPBFiorBXhpr74_rslMlFWI7sLkv2l7ipLSGjWdTd67w..'&f=pjson"
 req=requests.post(URL)
 req.status_code
 return "{}".format(req.json()['locations'][0]['feature']['geometry']['y']), "{}".format(req.json()['locations'][0]['feature']['geometry']['x'])
