import requests
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
# url = "http://127.0.0.1:8000/api/v1/goods/"
url = "http://127.0.0.1:8000/api/v1/goods/1/reviews/"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {"text": 456, "grade": 9}
response = requests.post(url,
                         data=json.dumps(data),
                         headers=headers)
# print(response)
print(response.text)
# text1 = json.loads(response.text)
# print(text1)
# pp.pprint(text1)
