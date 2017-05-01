"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib2, json
from datetime import datetime as dt

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

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

    # Dispatch to your skill's intent handlers
    if intent_name == "matrix":
        return doMatrix(intent, session)
    elif intent_name == "chill":
        return doChill(intent, session)
    elif intent_name == "end session":
        return endSession(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# ------------------------- custom skill Functions -----------------------------

def defaultGet(command,parameters={}):
    key = ""
    paramString = ""

    for i in parameters.keys():
        paramString +=  "&" + i + "=" + parameters[i]

    url = "ip:port/API/alexa/" + command + "?key=" + key + paramString
    raw_data = urllib2.urlopen(url)
    json_data = json.load(raw_data)

def successMessage(command):
    messages = [
                "command executed",
                "now showing %s",
                "there you go!",
                "ok, everything went well. Can I do something else?",
                "Can I help you with something else?",
                ""
                ]
    return messages[random.randint(0,len(messages)-1)].replace("%s",command)

def interpret(response):
    if not "response" in response:
        return (3,"I am very sorry, but it seems like something went wrong")
    status = response["response"]["status"]
    keystatus == response["response"]["key"]
    if keystatus == "invalid":
        return (1,"I am very sorry, but it seems like the security key or your device is invalid")
    elif status = "failed":
        return (2,"I am very sorry, something went wrong")
    elif status == "success" and keystatus == "valid":
        return (0,successMessage(""))
    else:
        return (4,"something went really wrong. Please contact the Developer")


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Pixelwall control system " \
                    "Please ask me to change the content of your PixelWall by saying, " \
                    "PixelWall show Matrix!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me to change the content of your PixelWall by saying, " \
                    "PixelWall show Matrix!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def doChill(intent,session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    resp = defaultGet("show/chill")
    status,retMsg = interpret(resp)
    print ("HTTP response status:",status)

def doMatrix(intent,session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    defaultGet("show/matrix")
    status,retMsg = interpret(resp)

    reprompt_text = "Please ask me to change the content of your PixelWall by saying, " \
                    "PixelWall show Matrix!"

    return build_response(session_attributes, build_speechlet_response(
        card_title, retMsg, reprompt_text, should_end_session))

def endSession(intent,session):
    session_attributes = {}
    card_title = "Bye"
    speech_output = "Disconnecting to PixelWall"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me to change the content of your PixelWall by saying, " \
                    "PixelWall show Matrix!"
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
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
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
