from flask import Flask, request, jsonify, render_template
import requests
import datetime
import slack
# from zato.server.service import Service


app = Flask(__name__)

# TRELLO_API_KEY='8e6c0b5d86a5f60ed6809ecd46ee4625'
# TRELLO_BOARD_ID='demo-zato'
# TRELLO_LIST_ID='5db920be1dd81b7f299cadb0'
# TRELLO_TOKEN='8d2b6ed4a76691cb904428c43c15dbbdd7280r.a108019976157babef3e52cb52c'
# SLACK_TOKEN='xoxb-816489230326-847043291989-eBDqoVcjTfScYBA6vnjwJFRd'


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tem')
def tem():
    return render_template('form.html')

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

# api = '8e6c0b5d86a5f60ed6809ecd46ee4625'
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