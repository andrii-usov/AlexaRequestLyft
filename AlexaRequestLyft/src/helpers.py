'''
Created on May 7, 2016

@author: Andrii Usov
'''
import json, requests
# --------------- Helpers that process requests ----------------------

def get_stage_number(session):
    if (hasattr(session, 'stage') == False or session['new'] == 'true'):
        return 0;
    else:
        return session['stage']

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