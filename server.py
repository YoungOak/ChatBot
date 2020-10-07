from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from messengerbot import MessengerClient, messages, attachments, templates, elements
import json, wikipedia, urllib, os
from chatbot import Chat, register_call

ACCESS_TOKEN = 'EAAJJC9XzVbABAE8X09HE4lv3HcGu43SkLlHPEGtEktIhivLsDfIeoOEGmCCjn0Uqd42jyLmiGIRRZAGUkfoQXD7X8I65ETb4rHf6BWdD9zOGgZCSKVlwt0Y9AgyZBAIQq0oXC73HOzL1p16D4NJF5gLBGYGzNdS9fs2aCfD4QZDZD'
VALIDATION_TOKEN = "First Chatbot Demo"
API_KEY = "643265136383408"

messenger = MessengerClient(access_token=ACCESS_TOKEN)

@register_call('whoIs')
def who_is(query, session_id):
    try:
        return wikipedia.summary(query)
    except Exception:
        for newquery in wikipedia.search(query):
            try:
                return wikipedia.summary(newquery)
            except Exception:
                pass
    return "I don't know about " + query

@csrf_exempt
def webhook(request):
    if request.method != "POST":
        if request.GET['hub.verify_token'] == VALIDATION_TOKEN:
            return HttpResponse(request.GET['hub.challenge'])
        return HttpResponse("Failed validation. Make sure the validation tokens match.")
    return chathandler(request)

def chathandler(request):
    data = json.loads(request.body)
    sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]
    recipient = messages.Recipient(recipient_id=sender_id)
    for i in data["entry"][0]["messaging"]:
        if "message" in i:
            if not sender_id in chat.conversation:
                initiateChat()
            respondToClient(sender_id, i["message"]["text"])
    return HttpResponse("It's Working")

def initiateChat(sender_id):
    chat._startNewSession(sender_id)
    chat.conversation[sender_id].append('Say "Hello"')
    url = "https://graph.facebook.com/v2.6/"+sender_id+\
          "?fields=first_name,last_name,gender&access_token="+ACCESS_TOKEN
    userInfo = json.load(urllib.urlopen(url))
    userInfo["name"] = userInfo["first_name"]
    chat._memory[sender_id].update(userInfo)
    
def respondToClient(sender_id, message):
    chat.conversation[sender_ïd].append(message)
    while message[-1] in ".!": message = message[:-1]
    result = chat.respond(message, sessionID=sender_id)
    chat.conversation[sender_id].append(result)
    response = messages.messageRequest(recipient, messages.Message(text=result))
    messenger.send(response)
    
template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "examples",
                                  "Example.template")

chat = Chat(template_file_path)