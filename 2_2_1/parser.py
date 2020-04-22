from bs4 import BeautifulSoup
import unittest


def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    imgs = 0
    headers = 0
    linkslen = 0
    lists = 0
    with open(path_to_file, 'r', encoding='utf-8') as html_file:
        html = html_file.read()
        soup = BeautifulSoup(html, "lxml")
    body = soup.find("div", id="bodyContent")
    # ---------------------------------------
    for i in body.find_all("img", width=True):
        if int(i['width']) >= 200:
            imgs += 1
    # ---------------------------------------
    for i in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        char = str(i.string)[0]
        if char in ["E", "T", "C"]:
            headers += 1
    # ---------------------------------------
    sum_ = 0
    max_ = 0
    for tag in body.find_all(True):
        if tag.name == "a":
            sum_ += 1
            if sum_ > max_:
                max_ = sum_
        else:
            sum_ = 0
    linkslen = max_
    # ---------------------------------------
    for i in body.find_all(True):
        if i.name == "ul" or i.name == "ol":
            lists += 1
            i.decompose()

    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
