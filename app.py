#Price Model Predection using IBM Watson
from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib3, json, requests, calendar

app = Flask(__name__)
CORS(app)

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

@app.route('/price/v1', methods=['GET', 'POST'])
def getPrice():
    #getting month and year from POST request
    month = request.args.get('month')
    year = request.args.get('year')

    payload_scoring = {"fields":["MONTH","YEAR"],"values":[[int(month),int(year)]]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/1d441776-58fb-4e22-8975-aa9b1c4a40a9/online', json=payload_scoring, headers=header)
    print("Scoring response")
    print(json.loads(response_scoring.text)) 
    response = json.loads(response_scoring.text)

    #get result from the response 
    month_num = int(response['values'][0][0])
    month = calendar.month_name[month_num]
    year = str(response['values'][0][1])
    pre_prams = str(response['values'][0][2])
    price_round = ("%.2f" % round(response['values'][0][3],2))
    price = str(price_round + " GHS (250KG)")

    return jsonify(month=month,year=year,pre_prams=pre_prams,price=price)



@app.route('/price/v2', methods=['GET', 'POST'])
def getPriceV2():
    #getting month and year from POST request
    month = request.args.get('month')
    year = request.args.get('year')
    temp = request.args.get('temp')
    rain = request.args.get('rain')

    payload_scoring = {"fields":["MONTH","YEAR","TEMP","Rainfall - (MM)"],"values":[[int(month),int(year),float(temp),float(rain)]]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/dab8060f-b1f4-49d7-bd69-8ca833cc2d3d/online', json=payload_scoring, headers=header)
    print("Scoring response")
    print(json.loads(response_scoring.text))
    response = json.loads(response_scoring.text)

    #get result from the response 
    month_num = int(response['values'][0][0])
    month = calendar.month_name[month_num]
    year = str(response['values'][0][1])
    pre_prams = str(response['values'][0][2])
    price_round = ("%.2f" % round(response['values'][0][3],2))
    price = str(price_round + " GHS")

    return jsonify(month=month,year=year,pre_prams=pre_prams,price=price)



@app.route('/price/v3', methods=['GET', 'POST'])
def getPriceV3():
    #getting crop , month and year from POST request
    month = request.args.get('month')
    year = request.args.get('year')
    crop = request.args.get('crop')


    payload_scoring = {"fields":["YEAR","MONTH","CROP"],"values":[[int(year),int(month),int(crop)]]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/a4263b57-a6f0-4592-83ac-68f2625647f3/online', json=payload_scoring, headers=header)
    print("Scoring response")
    print(json.loads(response_scoring.text)) 
    response = json.loads(response_scoring.text)

    # get result from the response 
    year = int(response['values'][0][0])
    month_num = int(response['values'][0][1])
    month = calendar.month_name[month_num]
    crop = int(response['values'][0][2])
    price_round = ("%.2f" % round(response['values'][0][4]))
    price = str(price_round + " GHS")

    # return str(response)
    return jsonify(month=month,year=year,price=price,crop=crop)

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)