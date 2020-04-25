from bs4 import BeautifulSoup
import re
import os


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    # Искать ссылки можно как угодно, не обязательно через re
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    # Словарь вида {"filename1": None, "filename2": None, ...}
    files = dict.fromkeys(os.listdir(path))
    # TODO Проставить всем ключам в files правильного родителя в значение, начиная от start
    for file in files:
        with open(path + '/' + file) as f:
            read_data = f.read()
        f.closed
        # Найти в файле все ссылки /wiki/, присутствующие в папке с файлами;
        # добавить их в словарь
        links = link_re.findall(read_data)
        links_for_file = []
        for link in links:
            if link in files:
                if link not in links_for_file and link != file:
                    links_for_file.append(link)
        files[file] = links_for_file
    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    bridge = []
    # TODO Добавить нужные страницы в bridge
    # Для поиска кратчайшего пути применяется алгоритм обхода графа в ширину
    # Создает очередь и помещает туда вершину, с которой необходимо начать
    queue = list([start])
    used = list([start])    # Вершины, которые уже горят
    parents = dict()        # Массив предков
    parents[start] = None
    # Пока очередь не пуста
    while len(queue) > 0:
        # Взять элемент в начале очереди
        vertex = queue.pop(0)
        # Осматривает соседей
        for neighbour in files[vertex]:
            # Если соседня вершина еще не горит
            if neighbour not in used:
                # Поджечь и поставить в очередь
                used.append(neighbour)
                queue.append(neighbour)
                parents[neighbour] = vertex
    # Определение пути от start до end
    item = end
    bridge.append(item)
    while item != start:
        item = parents[item]
        bridge.append(item)
    bridge.reverse()
    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно
    добраться от start до end, то по крайней мере, известны сами start и end, и можно
    распарсить только их. Оценка за тест, в этом случае, будет сильно снижена, но на
    минимальный проходной балл наберется, и тест будет пройден. Чтобы получить
    максимальный балл, придется искать все страницы. Удачи!
    """

    # Искать список страниц можно как угодно, даже так:
    # bridge = [start,] if start == end else [start, end]
    bridge = build_bridge(start, end, path)
    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open(os.path.join(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        # Количество картинок (img) с шириной (width) не меньше 200
        imgs = 0
        image_tags = body.find_all('img')
        for image_tag in image_tags:
            image_width = image_tag.get('width')
            if image_width:
                if int(image_width) >= 200:
                    imgs += 1

        # Количество заголовков, первая буква текста внутри которого: E, T или C
        headers = 0
        header_tags = body.find_all(re.compile(r'h\d+'))
        for header in header_tags:
            for child in header.children:
                if re.search('^[ETC].*', str(child.string)):
                    headers += 1

        # Длина максимальной последовательности ссылок, между которыми нет других тегов
        # С помощью регулярных выражений составляется список всех тегов.
        # Предполагается, что для подсчета последовательных ссылок за тегом </a>
        # должен идти тег <a>, либо ничего, если это последняя ссылка документа.
        re_tags = re.compile(r"\<[a-zA-Z]+.*?\>|\</[a-zA-Z]+.*?\>")
        all_tags = re_tags.findall(str(body))
        start = 0
        currenct_consec = 0
        linkslen = 0
        for tag in all_tags:
            if tag == '</a>':
                index = all_tags.index(tag, start)
                next_tag = all_tags[index + 1]
                # print(str(index) + ': ' + tag + ': ' + next_tag)
                if next_tag[0] == '<' and next_tag[1] == 'a':
                    currenct_consec += 1
                    if currenct_consec > linkslen:
                        linkslen = currenct_consec
                else:
                    currenct_consec = 0
            start += 1
        linkslen += 1

        # Количество списков, не вложенных в другие списки
        # Состявляется список всех списков. Если родитель
        # списка - не пункт списка, учитывать при подсчете.
        lists = 0
        list_tag = body.find_all('ul')
        list_tag.extend(body.find_all('ol'))
        for tag in list_tag:
            if tag.parent.name != 'li':
                lists += 1

        out[file] = [imgs, headers, linkslen, lists]

    return out
