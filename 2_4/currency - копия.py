from bs4 import BeautifulSoup
from decimal import Decimal


def get_data(val_tag):
    kurs = Decimal(val_tag.find_next_sibling('Value').string.replace(',', '.'))
    nominal = Decimal(val_tag.find_next_sibling('Nominal').string.replace(',', '.'))
    one_coin = kurs / nominal
    return kurs, nominal, one_coin


def convert_rur_to(amount, val_tag):
    print("RUR=>XXX")
    kurs, nominal, one_coin = get_data(val_tag)
    result = amount / one_coin
    print(f"kurs={kurs};nominal={nominal};one_coin={one_coin};result={amount}/{one_coin}={result}")
    return result


def convert_to_rur(amount, val_tag):
    print("XXX=>RUR")
    kurs = Decimal(val_tag.find_next_sibling('Value').string.replace(',', '.'))
    nominal = Decimal(val_tag.find_next_sibling('Nominal').string.replace(',', '.'))
    one_coin = kurs / nominal
    result = amount * one_coin
    print(f"kurs={kurs};nominal={nominal};one_coin={one_coin};result={amount}*{one_coin}={result}")
    return result


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")
    # response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp")
    # response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req=23/04/2020")
    soup = BeautifulSoup(response.content, 'xml')
    print(soup.prettify())
    if cur_from == "RUR":
        val_tag = soup.find('CharCode', text=cur_to)
        result = convert_rur_to(amount, val_tag)
    elif cur_to == "RUR":
        val_tag = soup.find('CharCode', text=cur_from)
        result = convert_to_rur(amount, val_tag)
    else:
        val_tag = soup.find('CharCode', text=cur_from)
        amount = convert_to_rur(amount, val_tag)
        val_tag = soup.find('CharCode', text=cur_to)
        result = convert_rur_to(amount, val_tag)
    # soup.find(ID='R01239').Value.string
    # print(kurs)
    # print(nominal)
    # # result = kurs * amount
    # result = round((kurs * amount / nominal), 4)
    print(result)
    # result = Decimal('3754.8057')
    return round(result, 4)  # не забыть про округление до 4х знаков после запятой
