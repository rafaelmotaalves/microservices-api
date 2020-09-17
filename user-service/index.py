from flask import Flask, jsonify, make_response
import requests
import os
import simplejson as json
import py_eureka_client.eureka_client as eureka_client
import sys

app = Flask(__name__)
GATEWAY_URL=os.environ["GATEWAY_URL"]
EUREKA_URL=os.environ["EUREKA_URL"]
PORT=int(sys.argv[1])

eureka_client.init(eureka_server="http://{}/eureka".format(EUREKA_URL), app_name="user-service", instance_port=PORT)

def read_data():
    with open("./data/users.json", "r") as f:
        return json.load(f)

@app.route("/", methods=['GET'])
def hello():
    ''' Greet the user '''

    return "User service is up"

@app.route('/users', methods=['GET'])
def users():
    ''' Returns the list of users '''

    resp = make_response(json.dumps(read_data(), sort_keys=True, indent=4))
    resp.headers['Content-Type']="application/json"
    return resp

@app.route('/users/<username>', methods=['GET'])
def user_data(username):
    ''' Returns info about a specific user '''
    usr = read_data()
    
    if username not in usr:
        return "Not found"

    return jsonify(usr[username])

@app.route('/users/<username>/lists', methods=['GET'])
def user_lists(username):
    ''' Get lists based on username '''

    try:
        url = "http://{host}/todo-service/lists/{username}".format(host=GATEWAY_URL, username=username)
        
        res = requests.get(url)
    except requests.exceptions.ConnectionError:
        return "Service unavailable"

    return jsonify(res.json())

if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0', debug=True)