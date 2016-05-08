'''
Created on May 7, 2016

@author: Andrii Usov
'''
from __future__ import print_function
from helpers import get_stage_number
from lyftIntegration import get_eta_data,get_closest_driver, get_cost_data, get_cost


applicationId="amzn1.echo-sdk-ams.app.6dc928c8-e705-4b14-b76d-7ba83e372ce7"

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    print(event)
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
    return get_welcome_response(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    stage = get_stage_number(session)
    
    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.YesIntent" and stage == "1":
        return ask_for_destination(session)
    if intent_name == "AMAZON.YesIntent" and stage == "3":
        return request_ride(session)
    elif intent_name == "SetDestination":
        return set_destination(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help(session)
    
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.NoIntent":
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

def get_help(session):
    stage = get_stage_number(session)
    speech_output=""
    if (stage == 0):
        speech_output="You can"

def ask_for_destination(session):
    speech_output="What is your destination?"
    card_title = "Destination?"
    reprompt_text="Sorry, what is the address you want a ride to?"
    should_end_session=False
    session['attributes']['stage']="2"
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    card_title = "Lyft driver is near"
    
    should_end_session = False
    data = get_eta_data(session)
    time_away = get_closest_driver(data)
    speech_output = "Sure, your Lyft Line is " +  time_away  + " away. "\
        "Do you want to request it?"
    reprompt_text = "Do you want to request a Lyft Line, which is " + time_away + " away?" 
    
    session_attributes = {"stage":"1"}

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

def set_destination(intent, session):
    card_title = "Destination set"
    
    should_end_session = False
    
    destination = intent['slots']['Destination']['value']
    session['attributes']['destination']=destination
    
    data = get_cost_data(session)
    cost = get_cost(data)
    
    speech_output = "Thank you! The ride to " + destination + " will cost you around " + cost + "." \
        "Do you still want to request it?"
    reprompt_text = "Do you want to request a Lyft?"
    
    session['attributes']['stage']="3"
    
    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def request_ride(session):
    card_title = "Requesting ride"
    
    should_end_session = True
    
    data = get_cost_data(session)
    cost = get_cost(data)
    
    speech_output = "Ok, requesting a ride." \
        "Good bye!"
    reprompt_text = ""
    
    session['attributes']['stage']=3

    return build_response(session['attributes'], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
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
