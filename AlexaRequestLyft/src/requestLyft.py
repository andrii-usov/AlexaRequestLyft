'''
Created on May 7, 2016

@author: Andrii Usov
'''
from __future__ import print_function
import httplib, urllib2, urllib, json
from geopy.geocoders import Nominatim

applicationId="amzn1.echo-sdk-ams.app.6dc928c8-e705-4b14-b76d-7ba83e372ce7"

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
            applicationId):
        raise ValueError("Invalid Application ID")
    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    stage = get_stage_number(session)
    
    # Dispatch to your skill's intent handlers
    if intent_name == "RequestLyft":
        return request_lyft(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.YesIntent":
        return call_a_cab(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Lyft service. " \
                    "To request a ride from Lyft say, " \
                    "ask Lyft for a ride"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please say, ask Lyft for a ride, " \
                    "to request a ride from Lyft."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Alexa Lyft service. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# Entry point for ride request
def request_lyft(intent, session):
    """ gets estimates from Lyft
    """

    card_title = intent['name']
    
    should_end_session = False
    
    speech_output = "There is a Lyft cab 2 minutes away, "  \
                    "would you like me to order it?"
    reprompt_text = "I will try one more time"
    
    session_attributes = {'lyft_cab_id':'123'}

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# Entry point for ride request
def call_a_cab(intent, session):
    """ gets estimates from Lyft
    """

    card_title = intent['name']
    
    should_end_session = False
    
    cab_id = session['attributes']['lyft_cab_id']
    
    speech_output = "Ok, calling"
    reprompt_text = "I will try one more time"
    
    session_attributes = {'lyft_cab_id':'123'}

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Helpers that process requests ----------------------

def get_stage_number(session):
    if (hasattr(session, 'stage') == False or session['new'] == 'true'):
        return 0;
    else:
        return session['stage']

def get_access_token(session):
    if hasattr(session['user'], 'accessToken') == True:
        return session['user']['accessToken']
    else:
        raise ValueError("Session should contain access token")

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': "Simple",
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '2.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }