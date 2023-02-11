import requests
import json

url = "http://localhost:5000/crop-recommedation"

payload = {
    "N": 100,
    "P": 50,
    "K": 75,
    "ph": 6.5,
    "rainfall": 25,
    "humidity" : 2.1,
    "temperature" : 44.0,
    "lang": "en",
}

headers = {
  'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.text)
