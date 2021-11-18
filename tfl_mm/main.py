from webex_skills.api import MindmeldAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState, ProcessedQuery
import requests
import re

api = MindmeldAPI()



@api.handle(intent='greet', default=True)
async def greet(current_state: DialogueState) -> DialogueState:
    text = 'Hello I am a super simple skill using NLP'
    new_state = current_state.copy()

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state


@api.handle(intent='exit')
async def goodbye(current_state: DialogueState) -> DialogueState:
    text = 'Have a nice day!'
    new_state = current_state.copy()

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state

@api.handle(intent='train_status')
async def turn_off(current_state: DialogueState, processed_query: ProcessedQuery) -> DialogueState:
    new_state = current_state.copy()
    text = new_state.text
    print(new_state)
    print('omer')
    print(processed_query.text)
   
    
    print("How are you")
    
    print(text)
        
    a = re.findall('.*?(\w*?)\sline\s?.*',text)[0]
    print(a)
    headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    'Content-type' : 'application/json'
            }
    url = f'https://api.tfl.gov.uk/Line/{a}/Status'
    print(url)
    req1 = requests.get(url= url , headers = headers)
    req1 = req1.json()
    
    ser = req1[0]['lineStatuses'][0]['statusSeverityDescription']
    
    if ser == 'Severe Delays':
        ser = f"There are {ser} on {a} line"
    else:
        ser = f"There is a {ser} on {a} line"
    # print(ser)
    

    # Call lights API to turn off your light here.

    new_state.directives = [
        responses.Reply(ser),
        responses.Speak(ser),
        responses.Sleep(10),
        responses.DisplayWebView('https://codepen.io/chrisgannon/pen/vjNNew',ser)
    ]

    return new_state