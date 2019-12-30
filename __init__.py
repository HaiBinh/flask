from flask import Flask, request, jsonify, render_template
import requests
import datetime
import slack
import telegram
import telepot
from twilio.rest import Client
# from zato.server.service import Service


app = Flask(__name__)

# TRELLO_API_KEY='8e6c0b5d86a5f60ed6809ecd46ee4625'
# TRELLO_BOARD_ID='demo-zato'
# TRELLO_LIST_ID='5db920be1dd81b7f299cadb0'
# TRELLO_TOKEN='8d2b6ed4a76691cb904428c43c15dbbdd7280r.a108019976157babef3e52cb52c'
# SLACK_TOKEN='xoxb-816489230326-847043291989-eBDqoVcjTfScYBA6vnjwJFRd'

global tele_bot_token
global bot
tele_bot_token = "973337571:AAEE7fX_9N7tmdzsHc0ltp43h-IUZEXKfXE"
tele_bot_name = "hb"
bot = telegram.Bot(token=tele_bot_token)
tele_bot = telepot.Bot(token=tele_bot_token)
URL = "103.56.157.105:5000/"
def get_response(msg):
    """
    you can place your mastermind AI here
    could be a very basic simple response like "معلش"
    or a complex LSTM network that generate appropriate answer
    """
    return "done!"

@app.route('/{}'.format(tele_bot_token), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
# get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id
# Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
# here we call our super AI
    response = get_response(text)
# now just send the message back
    # notice how we specify the chat and the msg we reply to
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    return 'ok'
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=tele_bot_token))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/tele')
def tele():
    return jsonify(tele_bot.getUpdates()[len(tele_bot.getUpdates())-1])

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tem')
def tem():
    # return render_template('form.html')
    # date = datetime.datetime.now()
    # var = request.args.get('var').split()
    # condition = ['api', 'token', 'name', 'list_id']
    # requests.post("https://api.trello.com/1/cards?key=" + \
    #               var[3] + "&token=" + var[2] + \
    #               "&name=" + var[4] + "&idList=" + \
    #               var[5] + "&due=" + str(date) + "&desc=" + \
    #               var[6])
    var = tele_bot.getUpdates()[len(tele_bot.getUpdates()) - 1]['message']['text'].split()
    if var[0] == '/trello':
        api = var[(var.index('api') + 1):var.index('token')]
        token = var[(var.index('token') + 1):var.index('list_id')]
        list_id = var[(var.index('list_id') + 1):var.index('name')]
        name = var[(var.index('name') + 1)::]
        if requests.post("https://api.trello.com/1/cards?key=" + \
                         api[0] + "&token=" + token[0] + \
                         "&idList=" + list_id[0] + "&name=" + convert(name)):
            return var[0]
    if var[0] == '/slack':
        token = var[(var.index('token') + 1):var.index('message')]
        message = var[(var.index('message') + 1)::]
        if token and message:
            client = slack.WebClient(token=token[0])
            client.chat_postMessage(
                channel='#zato',
                text=convert(message))
            return "done!"
    if var[0] == '/whatsapp':
        message = var[(var.index('message') + 1)::]
        client = Client('AC0bd8e1ad8499a17ac894f9236dffa0ed', 'e31a6060ae7eff7b869d22ec6e3cfed9')
        to_whatsapp_number = 'whatsapp:+84819399888'
        from_whatsapp_number = 'whatsapp:+14155238886'
        client.messages.create(body=convert(message),
                               #media_url='https://demo.twilio.com/owl.png',
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)
        return "done!"

def convert(list):
    string = ''
    for r in list:
        string += r + ' '
    return string
@app.route('/get-board')
def getBoard():

    TRELLO_API_KEY = request.args.get('TRELLO_API_KEY')
    TRELLO_TOKEN = request.args.get('TRELLO_TOKEN')
    BOARD_ID = request.args.get('BOARD_ID')
    list_board = findBoard(TRELLO_API_KEY, TRELLO_TOKEN)
    if list_board:
        for r in list_board:
            if r['id'] == BOARD_ID:
                return r

@app.route('/get-list')
def getList():

    TRELLO_API_KEY = request.args.get('TRELLO_API_KEY')
    TRELLO_TOKEN = request.args.get('TRELLO_TOKEN')
    BOARD_ID = request.args.get('BOARD_ID')
    board_id = findBoard(TRELLO_API_KEY, TRELLO_TOKEN)
    get_lists_url = "https://api.trello.com/1/boards/" + BOARD_ID + \
                    "/lists?key=" + TRELLO_API_KEY + "&token=" + TRELLO_TOKEN + \
                    "&response_type=token"

    r = requests.get(get_lists_url)
    # list = jsonify(r.json())
    list = []
    for m in r.json():
        list.append({'name': m['name'], 'id': m['id']})
    return jsonify(list)

# api = 'a'
# token = '8d2b6ed4a76691cb904428c43c15dbbdd7280a108019976157babef3e52cb52c'
# name = 'flask adding'
# list_id = '5db88d71c5aa0007336dd364'
# description = 'first time'
@app.route('/add-card')
def add_card(api, token, name, list_id, description):
    date = datetime.datetime.now()
    r = requests.post("https://api.trello.com/1/cards?key=" + \
                  api + "&token=" + token + \
                  "&name=" + name + "&idList=" + \
                  list_id + "&due=" + str(date) + "&desc=" + \
                  description)
    return 'done!'

@app.route('/hello-slack', methods=['POST'])
def helloSlack():

    api = request.headers['api']
    token = request.headers['token']

    client = slack.WebClient(token='xoxb-816489230326-847043291989-eBDqoVcjTfScYBA6vnjwJFRd')
    if api and token:
        response = client.chat_postMessage(
            channel='#zato',
            text="Successful!")
        # assert response["message"]["text"] == "Successful!"
    return 'ok!'



def findBoard(api, token):
    get_boards_url = "https://api.trello.com/1/members/me/boards?key=" + \
                     api + "&token=" + token + "&response_type=token"

    r = requests.get(get_boards_url)
    return r.json()
    # for boards in r.json():
    #
    #     board_id = ""
    #     board_name = ""
    #
    #     for key, value in boards.items():
    #
    #         if key == "id":
    #
    #             board_id = value
    #
    #         elif key == "name":
    #
    #             board_name = value
    #
    #     if board_name == TRELLO_BOARD_ID:
    #         print("Found board.")
    #         return board_id
    #     else:
    #         print("Didn't find board.")
    #         return False


def findList(board_id, TRELLO_API_KEY, TRELLO_TOKEN):
    get_lists_url = "https://api.trello.com/1/boards/" + board_id + \
                    "/lists?key=" + TRELLO_API_KEY + "&token=" + TRELLO_TOKEN + \
                    "&response_type=token"

    r = requests.get(get_lists_url)

    for lists in r.json():

        list_id = ""
        list_name = ""

        for key, value in lists.items():

            if key == "id":

                list_id = value

            elif key == "name":

                list_name = value

        if list_name == TRELLO_LIST_ID:

            print("Found list.")

            return list_id

        else:

            print("Didn't find list.")

            return False

def findCards(list_id):
    get_cards_url = "https://api.trello.com/1/lists/" + "5db88d71c5aa0007336dd364" + \
                    "/cards?key=" + TRELLO_API_KEY + "&token=" + TRELLO_TOKEN + \
                    "&response_type=token"

    list_of_cards = []

    r = requests.get(get_cards_url)

    for cards in r.json():

        card_id = ""
        card_name = ""
        card_due = ""
        card_desc = ""

        for key, value in cards.items():

            if key == "id":

                card_id = value

            elif key == "name":

                card_name = value

            elif key == "due":

                card_due = value

            elif key == "desc":

                card_desc = value

        list_of_cards.append([card_id, card_name, card_due, card_desc])

    if len(list_of_cards) > 0:

        return list_of_cards

    else:

        return False




if __name__ == '__main__':
    app.run(debug=True)