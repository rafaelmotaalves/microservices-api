from flask import Flask, jsonify, make_response
import json
import os
import sys
import py_eureka_client.eureka_client as eureka_client

app = Flask(__name__)
EUREKA_URL=os.environ["EUREKA_URL"]
PORT=int(sys.argv[1])

eureka_client.init(eureka_server="http://{}/eureka".format(EUREKA_URL), app_name="todo-service", instance_port=PORT)

def read_data():
    with open('./data/todo.json', "r") as jsf:
        return json.load(jsf)

@app.route('/', methods=['GET'])
def hello():
    ''' Greet the user '''

    return "Todo service is up"

@app.route('/lists', methods=['GET'])
def show_lists():
    ''' Displays all the lists '''
    todo_list = read_data();
    tlists = []
    for username in todo_list:
        for lname in todo_list[username]:
            tlists.append(lname)
    return jsonify(lists=tlists)

@app.route('/lists/<username>', methods=['GET'])
def user_list(username):
    ''' Returns a user oriented list '''
    todo_list = read_data();
    if username not in todo_list:
        return "No list found"

    return jsonify(todo_list[username])

if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0',debug=True)