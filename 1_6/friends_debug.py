import requests
import json
from datetime import date
from collections import Counter

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'


def calc_age(uid):
    id_ = get_users(uid)
    print(id_)
    dd = get_friends(id_)
    print(dd)
    print(len(dd))
    cc = Counter(dd)
    print(cc)
    print(type(cc))
    print(cc.most_common())
    print([v[0] for v in sorted(cc.items(), key=lambda kv: (-kv[1], kv[0]))])
    l = sorted(cc.items(), key=lambda kv: (-kv[1], kv[0]))

    return l


def get_users(uid):
    url = "https://api.vk.com/method/users.get"
    payload = {'v': '5.71', 'access_token': ACCESS_TOKEN, 'user_ids': uid}
    r = requests.get(url, params=payload)
    if r.status_code == requests.codes.ok:
        # print(f"r.text={r.text}")
        d = json.loads(r.text)
        # print(d)
        # for u in d["response"]:
        #     print(u)
        #     print(u["id"])
        # print(d["response"][0]["id"])
        # return d["response"][0]["id"]
    else:
        r.raise_for_status()
    return d["response"][0]["id"]


def get_friends(id_):
    url = "https://api.vk.com/method/friends.get"
    payload = {'v': '5.71', 'access_token': ACCESS_TOKEN, 'user_id': id_, 'fields': 'bdate'}
    r = requests.get(url, params=payload)
    if r.status_code == requests.codes.ok:
        print(f"r.text={r.text}")
        d = json.loads(r.text)
        print(f"d={d}")
        print(f"x={d['response']['items']}")
        dd = []
        year_ = int(date.today().year)
        print(f"year_={year_}")
        for f in d['response']['items']:
            try:
                try:
                    year2 = int(f['bdate'].split(".")[2])
                    print(year2)
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
    # res = calc_age('ministrbob')
    print(res)

