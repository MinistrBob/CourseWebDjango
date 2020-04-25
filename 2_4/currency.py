from bs4 import BeautifulSoup
from decimal import Decimal


def get_data(val_tag):
    kurs = Decimal(val_tag.find_next_sibling('Value').string.replace(',', '.'))
    nominal = Decimal(val_tag.find_next_sibling('Nominal').string.replace(',', '.'))
    one_coin = kurs / nominal
    return kurs, nominal, one_coin


def convert_rur_to(amount, val_tag):
    kurs, nominal, one_coin = get_data(val_tag)
    result = amount / one_coin
    return result


def convert_to_rur(amount, val_tag):
    kurs = Decimal(val_tag.find_next_sibling('Value').string.replace(',', '.'))
    nominal = Decimal(val_tag.find_next_sibling('Nominal').string.replace(',', '.'))
    one_coin = kurs / nominal
    result = amount * one_coin
    return result


def convert(amount, cur_from, cur_to, date, requests):
    # response = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")
    host = r"http://www.cbr.ru/scripts/XML_daily.asp"
    params = {"date_req": date}
    response = requests.get(host, params)
    soup = BeautifulSoup(response.content, 'xml')
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
    return round(result, 4)
