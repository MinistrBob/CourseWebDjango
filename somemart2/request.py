import requests
import json
import pprint
from base64 import b64encode


pp = pprint.PrettyPrinter(indent=4)
url = "http://127.0.0.1:8000/api/v1/goods/"
# url = "http://127.0.0.1:8000/api/v1/goods/1/reviews/"
userAndPass = b64encode(b"worker:P@ssw0rds").decode("ascii")
# userAndPass = b64encode(b"Aladdin:OpenSesame").decode("ascii")
print(userAndPass)
headers = {'Authorization': f"Basic {userAndPass}",
           'Content-type': 'application/json',
           'Accept': 'text/plain'}
data = {
  "title": "Сыр",
  "description": "Очень вкусный сыр, да еще и российский.",
  "price": 100
}
response = requests.post(url,
                         data=json.dumps(data),
                         headers=headers)
# print(response)
print(response.text)
print(response.status_code)
# text1 = json.loads(response.text)
# print(text1)
# pp.pprint(text1)
