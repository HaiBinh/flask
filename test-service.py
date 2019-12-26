from flask import Flask
import requests
import datetime
from zato.server.service import Service
from __future__ import absolute_import, division, print_function, unicode_literals
from json import dumps

class Trello(Service):
    def get_info(self, cust_id):
        return 'done!'
    def handle(self):
        api = '8e6c0b5d86a5f60ed6809ecd46ee4625'
        token = '8d2b6ed4a76691cb904428c43c15dbbdd7280a108019976157babef3e52cb52c'
        name = 'flask adding'
        list_id = '5db88d71c5aa0007336dd364'
        description = 'first time'
        date = datetime.datetime.now()
        r = requests.post("https://api.trello.com/1/cards?key=" + \
                          api + "&token=" + token + \
                          "&name=" + name + "&idList=" + \
                          list_id + "&due=" + str(date) + "&desc=" + \
                          description)
        self.response.payload = dumps({'name': name})


# app = Flask(__name__)
#
# TRELLO_API_KEY='8e6c0b5d86a5f60ed6809ecd46ee4625'
# TRELLO_BOARD_ID='demo-zato'
# TRELLO_LIST_ID='5db920be1dd81b7f299cadb0'
# TRELLO_TOKEN='8d2b6ed4a76691cb904428c43c15dbbdd7280a108019976157babef3e52cb52c'
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
# @app.route('/get-board')
# def findBoard(api, token):
#     get_boards_url = "https://api.trello.com/1/members/me/boards?key=" + \
#                      api + "&token=" + token + "&response_type=token"
#
#     r = requests.get(get_boards_url)
#
#     for boards in r.json():
#
#         board_id = ""
#         board_name = ""
#
#         for key, value in boards.items():
#
#             if key == "id":
#
#                 board_id = value
#
#             elif key == "name":
#
#                 board_name = value
#
#         if board_name == TRELLO_BOARD_ID:
#             print("Found board.")
#             return board_id
#         else:
#             print("Didn't find board.")
#             return False
#
#
# # api = '8e6c0b5d86a5f60ed6809ecd46ee4625'
# # token = '8d2b6ed4a76691cb904428c43c15dbbdd7280a108019976157babef3e52cb52c'
# # name = 'flask adding'
# # list_id = '5db88d71c5aa0007336dd364'
# # description = 'first time'
# @app.route('/add-card')
# def add_card(api, token, name, list_id, description):
#     date = datetime.datetime.now()
#     r = requests.post("https://api.trello.com/1/cards?key=" + \
#                   api + "&token=" + token + \
#                   "&name=" + name + "&idList=" + \
#                   list_id + "&due=" + str(date) + "&desc=" + \
#                   description)
#     return 'done!'
#
# if __name__ == '__main__':
#     app.run()