from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'                                # SECRET KEY CAN BE ANYTHING



# OPEN-AI CHAT GPT

openai.api_key = "API-KEY"                                              # OPEN-AI API KEY
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
        prompt=prompt, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0.0, best_of=1,
        max_tokens=1024)
    answer = response.choices[0].text.strip()
    return answer

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'

account_sid = 'ACCOUNT-SID'                                                 # Twilio Account SID
auth_token = 'AUTH-TOKEN'                                                   # Twilio Account Auth Token
client = Client(account_sid, auth_token)



# TWILIO

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values['Body']
    print(incoming_msg)

    r = MessagingResponse()
    if incoming_msg:
        chat_log = session.get('chat_log')
        answer = ask(incoming_msg, chat_log)
        session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
        r.message(answer)
        responded = True
    else:
        responded = False
    if not responded:
        r.message("Message Cannot Be Empty!")
    return str(r) 
    

if __name__ == '__main__':
    app.run()