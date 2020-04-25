from bs4 import BeautifulSoup


def parse(path_to_file):
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
    tagsa = body.find_all('a')
    for t in tagsa:
        sum_ = 1
        subtags = t.find_next_siblings()
        for i in subtags:
            if i.name == "a":
                sum_ += 1
                if sum_ > max_:
                    max_ = sum_
            else:
                sum_ = 0
                continue
    linkslen = max_
    # ---------------------------------------
    for i in body.find_all(True):
        if i.name == "ul" or i.name == "ol":
            lists += 1
            i.decompose()
    # ---------------------------------------

    return [imgs, headers, linkslen, lists]
