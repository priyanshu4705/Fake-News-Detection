from bs4 import BeautifulSoup
import requests
import re

from app.config import HEADERS, STOPWORDS

def clean_data(x: str) -> str:
    '''
        - remove square brackets\n
        - remove punctuation\n
        - remove words containing numbers\n
        - remove links\n
        - remove newlines\n
    '''

    text = x
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)  
    text = re.sub(r'[^\w\s]', '', text) 
    text = re.sub(r'\w*\d\w*', '', text)  
    text = re.sub(r'http\S+', '', text)
    text = re.sub('\n', ' ', text)
    return text


def remove_stop_word(text: str) -> str:
    '''
        remove stopwords from a set of selected stopwords
    '''
    filtered_text = [w for w in text.split() if not w in STOPWORDS]
    return ' '.join(filtered_text)


def scrape(url: str) -> tuple:
    '''
        web scrapper
    '''
    content = requests.get(url, headers=HEADERS).content.decode()
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.text
    text = ''

    if url.find('timesofindia') > 0:
        para = soup.find_all('div', {'class': 'Normal'})
    elif url.find('bbc') > 0:
        para = soup.body.find_all('div', {'data-component': 'text-block'})
    elif url.find('nytimes') > 0:
        para = soup.body.find_all('section', {'name': 'articleBody'})
    else:
        para = soup.body.find_all('p')

    for p in para:
        text += p.text

    text = clean_data(text)
    title = clean_data(title)
    text = remove_stop_word(text)

    return (title, text)
