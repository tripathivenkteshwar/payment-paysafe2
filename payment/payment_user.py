import requests
import json
from base64 import b64encode
base_url="https://api.test.paysafe.com/paymenthub/v1"
def create_customer(data, mer_ref, SECRET_KEY):

  values ={
      "merchantCustomerId": mer_ref,
      "locale": "en_US",
      "firstName": data['firstName'],
      "middleName": "",
      "lastName": data["lastName"],
      "dateOfBirth": {
        "year": 1981,
        "month": 10,
        "day": 24
      },
      "email": data["email"],
      "phone": data["phone"],
      "ip": "192.0.126.111",
      "gender": "M",
      "nationality": "Canadian",
      "cellPhone": "7775558888"
    }

  aut=SECRET_KEY
  values = json.dumps(values)
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic {}'.format(aut),
    'Simulator': '\'EXTERNAL\''
  }
  res = requests.post(base_url+"/customers",
                      data=values, headers=headers)
  return res.json()


def single_use_token(cust_id, mer_ref, SECRET_KEY):

    url= base_url+"/customers/"+cust_id+"/singleusecustomertokens"

    payload ={
        "merchantRefNum": mer_ref,
        "paymentTypes": [
          "CARD"
        ]
      }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic {}'.format(SECRET_KEY),
        'Simulator': '\'EXTERNAL\''
    }
    payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    r = response.json()
    return r

def pay_for_product(paymentHandleToken, amount, mer_ref, SECRET_KEY):

    url = base_url+"/payments"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic {}'.format(SECRET_KEY),
        'Simulator': '"EXTERNAL"'
    }
    payload = {
        "merchantRefNum": mer_ref,
        "amount": amount,
        "currencyCode": "USD",
        "dupCheck": "true",
        "settleWithAuth": "false",
        "paymentHandleToken": paymentHandleToken,
        "customerIp": "192.0.126.111"
    }
    payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()
