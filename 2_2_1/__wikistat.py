from bs4 import BeautifulSoup
import re
import os

get_links_cache = {}

def get_links(file, path, os_path_exists):
    result = []
    if file in get_links_cache: return get_links_cache[file]
    if not file: return result

    ### mine - slow
    # if not os.path.exists(os.path.join(path, file)): return result
    # with open(os.path.join(path, file), encoding='utf-8') as data:
    #     soup = BeautifulSoup(data.read(), "lxml")
    # links = soup.find(id="bodyContent").find_all('a')
    # for each in links:
    #     link = each.get('href', '')
    #     if '/wiki/' in link:
    #         link = link[link.rfind('/')+1:]
    #         if not os.path.exists(os.path.join(path, link)): continue
    #         if link not in result: result.append(link)

    ### sample
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    with open(os.path.join(path, file), encoding='utf-8') as data:
        links = re.findall(link_re, data.read())
    for link in links:
        if link not in result and link in os_path_exists: result.append(link)

    get_links_cache[file] = result
    # print(f'{file} : {len(result)}')
    return result

def deeper(tree, level, max_level, start, end, path, os_path_exists):
    if level > max_level: return 'None'
    for each in start:
        tmp = get_links(each, path, os_path_exists)
        start[each] = dict.fromkeys(tmp)
        if end in tmp: return f'{each}|{end}'
        result = each + '|' + deeper(tree, level + 1, max_level, start[each], end, path, os_path_exists)
        if 'None' not in result: return result
    return 'None'

def build_tree(start, end, path):
    tree = {}
    os_path_exists = os.listdir('wiki/')
    if start == end: return [start]
    tree[start] = dict.fromkeys(get_links(start, path, os_path_exists))
    if end in tree[start]: return [start, end]

    max_level = 1
    while True:
        # print(i)
        result = deeper(tree, 1, max_level, tree[start], end, path, os_path_exists)
        max_level += 1
        if 'None' not in result:
            result = f'{start}|{result}'
            return result.split('|')
        # if max_level > 10: return None

def parse(start, end, path):
    out = {}
    for file in build_tree(start, end, path):
        with open(os.path.join(path, file), encoding='utf-8') as data:
            soup = BeautifulSoup(data.read(), "lxml")
        body = soup.find(id="bodyContent")

        # Количество картинок (img) с шириной (width) не меньше 200
        imgs = 0
        for each in body.find_all('img'):
            width = int(each.attrs.get('width', 0))
            if width >= 200: imgs += 1

        # Количество заголовков, первая буква текста внутри которого: E, T или C
        headers = 0
        for each in body.find_all(['h1','h2','h3','h4','h5','h6']):
            if each.text[0] in 'ETC': headers += 1

        # Длина максимальной последовательности ссылок, между которыми нет других тегов
        linkslen = 0
        linkslen_tmp = 1
        for each in body.find_all('a'):
            if each.next_sibling and each.next_sibling.next_sibling and each.next_sibling.next_sibling.name == 'a':
                linkslen_tmp += 1
                linkslen = max(linkslen, linkslen_tmp)
            else:
                linkslen_tmp = 1

        # Количество списков, не вложенных в другие списки
        lists = 0
        for each in body.find_all(['ul', 'ol']):
            tags = [tag.name for tag in each.parents]
            if 'ul' not in tags and 'ol' not in tags: lists += 1

        out[file] = [imgs, headers, linkslen, lists]

    return out

if __name__ == '__main__':
    print(parse("Stone_Age", "Python_(programming_language)", 'wiki/'))
