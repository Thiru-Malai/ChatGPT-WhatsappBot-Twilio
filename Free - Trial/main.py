from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import openai
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'                                # SECRET KEY CAN BE ANYTHING



# OPEN-AI CHAT GPT

openai.api_key = "open-ai-api-key"                                              # OPEN-AI API KEY
completion = openai.Completion()

start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    prompt = question
    response = completion.create(
        prompt=prompt, engine="text-davinci-003", stop=['\nHuman'], temperature=0.2,
        top_p=1, frequency_penalty=0.1, presence_penalty=0.0, best_of=1,
        max_tokens=256)
    answer = response.choices[0].text.strip()
    return answer

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'



# TWILIO

account_sid = 'account_sid'                                                 # Twilio Account SID
auth_token = 'auth_token'                                                    # Twilio Account Auth Token
client = Client(account_sid, auth_token)

def sendMessage(body_mess, phone_number):
    print("BODY MESSAGE " + body_mess)
    message = client.messages.create(
                                from_='whatsapp:+14155238886',                  # With Country Code
                                body=body_mess,
                                to='whatsapp:' + phone_number                   # With Country Code
                            )
    print(message)                                                              # Print Response


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values['Body']
    phone_number = (request.values['WaId'])

    if incoming_msg:
        chat_log = session.get('chat_log')
        answer = ask(incoming_msg, chat_log)
        session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
        sendMessage(answer, phone_number)
        print(answer)
    else:
        sendMessage("Message Cannot Be Empty!")
        print("Message Is Empty")
    r = MessagingResponse()
    r.message("")        
    return str(r)
    


if __name__ == '__main__':
    app.run()
