import re
import sys
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

def get_args(args):
    ans = {}
    for arg in args:
        if arg.split("=")[0] == '--url':
            ans['url'] = arg.split("=")[1]
        elif arg.split("=")[0] == '--words':
            ans['words'] = arg.split("=")[1].lower().split(',')
    return ans

def scrap(url) -> list:
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    page_elements = soup.findAll(text=True)
    page_text = filter(visible_text, page_elements)
    page_words = []
    for string in page_text:
        string = re.sub(r'[^\w]', ' ', string).strip().lower()
        if string: page_words.extend(string.split())
    return page_words

def visible_text(element):
    skip_elements = {'style', 'script', 'head', 'title', 'meta', '[document]'}
    if element.parent.name in skip_elements: return False
    if isinstance(element, Comment): return False
    return True

if __name__ == '__main__':
    args = get_args(sys.argv[1:])
    url, given_words = args['url'], args['words']

    word_count = {}
    for word in given_words:
        word_count[word] = 0
    
    page_words = scrap(url)
    given_words_set = set(given_words)
    for page_word in page_words:
        if page_word in given_words_set:
            word_count[page_word] += 1

    for word in given_words:
        print(f'{word.capitalize()}: {word_count[word]}')