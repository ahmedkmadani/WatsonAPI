from flask import Flask, request, jsonify
import urllib3, json, requests

app = Flask(__name__)

#IBM Watson Credenials 
wml_credentials={
    "url":'https://eu-gb.ml.cloud.ibm.com',
    "username": '461336f2-8984-492a-b72a-9376b8e9d1c2',
    "password": 'de3136e2-2a65-48cd-85f7-77dd03715ba3'
    }

#init header and request and getting response 
headers = urllib3.util.make_headers(basic_auth='{username}:{password}'.format(username=wml_credentials['username'], password=wml_credentials['password']))
url = '{}/v3/identity/token'.format(wml_credentials['url'])
response = requests.get(url, headers=headers)
mltoken = json.loads(response.text).get('token')

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/price', methods=['GET'])
def getPrice():
    return ' Hello from Yfarm'