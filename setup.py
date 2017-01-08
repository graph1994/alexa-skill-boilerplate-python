

def handler(event, context):
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    else:
        return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
    """Called when the session starts"""

    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])

def on_launch(launch_request, session):
    """
    Called when the user launches the skill without specifying what they
    want.
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
    if intent_name == "Hello":
        return hello_world(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def get_welcome_response():
    speech_output = ("Hello World is a boiler plate template for creating lamda fucntion for an Alexa Skill in Python.")
    card_title = "Hello World"
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response_session(card_title, speech_output))

def handle_get_help_request(intent, session):
    session_attributes = {}
    card_title = "Hello World Help"
    speech_output = ("Hello world just response hello world with a number")
    return build_response(session_attributes, build_speechlet_response_session(card_title, speech_output))

def handle_finish_session_request(intent, session):
    session_attributes = {}
    card_title = "Hello World Finish"
    speech_output = ("Thanks for using Hello World")
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output))

def hello_world(intent,session):
    session_attributes = create_hello_world(intent)
    speech_output = session_attributes['hello_world_resp']
    card_title = "Hello World with Value"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output))

def create_hello_world(intent):
    if 'value' in intent['slots']['Number']:
        val = intent['slots']['Number']['value']
        if val == "?":
            n = 0
        else:
            n = int(val)
    else:
        n = 0
    hello_world_string = 'Hello World! Value said was ' + str(n)

    return {"hello_world_resp": hello_world_string}

def build_speechlet_response(title, output):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'shouldEndSession': True
    }
def build_speechlet_response_session(title, output):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'shouldEndSession': False
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response

    }
