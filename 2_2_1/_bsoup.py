#!/usr/bin/python3

from bs4 import BeautifulSoup, SoupStrainer
import unittest
import re


def parse(path_to_file):
    imgs, headers, linkslen, lists = 0, 0, 0, 0

    with open(path_to_file, 'r', encoding='utf-8') as f:
        html = f.read()
        div = SoupStrainer('div', {'id': 'bodyContent'})
        soup = BeautifulSoup(html, parse_only=div, features="lxml")        
        
        imgs = len(soup.find_all(lambda tag:tag.name == "img" and tag.has_attr("width") and int(tag["width"]) >= 200))

        headers = len(soup.find_all(lambda tag: re.match(r'^h[1-6]', tag.name) and re.match(r'^[ETC]', tag.text)))

        a = soup.find('div').find_next('a')
        while a is not None:
            sibs = a.find_next_siblings()
            i = 1
            for tag in sibs:
                if tag.name == 'a':
                    i += 1
                else:
                    break
            if i > linkslen:
                linkslen = i
            a = a.find_next('a')
            
        for l in soup.find_all(['ol', 'ul']):
            if l.find_parent(['ol', 'ul']) is None:
                lists += 1
                
    return [imgs, headers, linkslen, lists]
    
