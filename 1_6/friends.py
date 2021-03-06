import requests
import json
from datetime import date
from collections import Counter

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'


def calc_age(uid):
    id_ = get_users(uid)
    dd = get_friends(id_)
    cc = Counter(dd)
    ll = sorted(cc.items(), key=lambda kv: (-kv[1], kv[0]))
    return ll


def get_users(uid):
    url = "https://api.vk.com/method/users.get"
    payload = {'v': '5.71', 'access_token': ACCESS_TOKEN, 'user_ids': uid}
    r = requests.get(url, params=payload)
    if r.status_code == requests.codes.ok:
        d = json.loads(r.text)
    else:
        r.raise_for_status()
    return d["response"][0]["id"]


def get_friends(id_):
    url = "https://api.vk.com/method/friends.get"
    payload = {'v': '5.71', 'access_token': ACCESS_TOKEN, 'user_id': id_, 'fields': 'bdate'}
    r = requests.get(url, params=payload)
    if r.status_code == requests.codes.ok:
        d = json.loads(r.text)
        dd = []
        year_ = int(date.today().year)
        for f in d['response']['items']:
            try:
                try:
                    year2 = int(f['bdate'].split(".")[2])
                    dd.append(year_ - year2)
                except:
                    pass
            except:
                pass
    else:
        r.raise_for_status()
    return dd


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
