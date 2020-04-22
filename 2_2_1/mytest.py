from bs4 import BeautifulSoup


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
        span = i.find("span", string=True)
        if span:
            char = str(span.string)[0]
        else:
            char = str(i.string)[0]
        if char in ["E", "T", "C"]:
            headers += 1
    # ---------------------------------------
    max_ = 0
    tag = body.find_next('a')
    while tag is not None:
        sum_ = 1
        subtags = tag.find_next_siblings()
        for i in subtags:
            if i.name == "a":
                sum_ += 1
                if sum_ > max_:
                    max_ = sum_
            else:
                sum_ = 1
                continue
        tag = tag.find_next('a')
    linkslen = max_
    # ---------------------------------------
    for i in body.find_all(True):
        if i.name == "ul" or i.name == "ol":
            lists += 1
            i.decompose()

    return [imgs, headers, linkslen, lists]


if __name__ == '__main__':
    print(parse(r'c:\MyGit\CourseWebDjango\2_2_1\wiki\Stone_Age'))
    print([13, 10, 12, 40])
    print(parse(r'c:\MyGit\CourseWebDjango\2_2_1\wiki\Brain'))
    print([19, 5, 25, 11])
    print(parse(r'c:\MyGit\CourseWebDjango\2_2_1\wiki\Artificial_intelligence'))
    print([8, 19, 13, 198])
    print(parse(r'c:\MyGit\CourseWebDjango\2_2_1\wiki\Python_(programming_language)'))
    print([2, 5, 17, 41])
    print(parse(r'c:\MyGit\CourseWebDjango\2_2_1\wiki\Spectrogram'))
    print([1, 2, 4, 7])
