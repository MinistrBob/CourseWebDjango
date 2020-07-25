import requests
import json
import pprint
from requests.auth import HTTPBasicAuth


pp = pprint.PrettyPrinter(indent=4)
# url = "https://datasend.webpython.graders.eldf.ru/submissions/1/"
# headers = {
#             'authorization': "Basic YWxsYWRpbjpvcGVuc2VzYW1l",
#             'content-type': "application/json"
#         }
#
# response = requests.request("POST", url, headers=headers)
# # print(response)
# print(response.text)
# text1 = json.loads(response.text)
# # print(text1)
# pp.pprint(text1)
"""
{   'instructions': 'Сделайте PUT запрос на тот же хост, но на path указанный '
                    'в этом документе c логином и паролем из этого документа. '
                    'Логин и пароль также передайте в заголовке Authorization.',
    'login': 'galchonok',
    'password': 'ktotama',
    'path': 'submissions/super/duper/secret/'}
"""
url = "https://datasend.webpython.graders.eldf.ru/submissions/super/duper/secret/"
# headers = {
#     'authorization': "Basic YWxsYWRpbjpvcGVuc2VzYW1l",
#     'login': 'galchonok',
#     'password': 'ktotama'
# }

response = requests.request("PUT", url, auth=HTTPBasicAuth('galchonok', 'ktotama'))
print(response)
print(response.text)
text1 = json.loads(response.text)
# print(text1)
pp.pprint(text1)
