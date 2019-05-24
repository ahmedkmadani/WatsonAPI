#Price Model Predection using IBM Watson
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

@app.route('/price', methods=['GET', 'POST'])
def getPrice():
    #getting month and year from POST request
    month = request.args.get('month')
    year = request.args.get('year')

    payload_scoring = {"fields":["MONTH","YEAR"],"values":[[int(month),int(year)]]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/1d441776-58fb-4e22-8975-aa9b1c4a40a9/online', json=payload_scoring, headers=header)
    print("Scoring response")
    print(json.loads(response_scoring.text)) 
    response = json.loads(response_scoring.text)

    # #get result from the response 
    month = str(response['values'][0][0])
    year = str(response['values'][0][1])
    pre_prams = str(response['values'][0][2])
    price = str(response['values'][0][3])

    return price