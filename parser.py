import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from loads import fetch_data

porter_stemmer = PorterStemmer()

def html_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator = ' ')
    return text

def tokenize(text):
    text = text.lower()
    cleaned_text = re.sub(r'[^\w\s]', ' ', text)
    words = cleaned_text.split()
    tokens = []
    for i in words:
        if i:
            tokens.append(i)
    return tokens

def calculate_tf(html):
    text = html_to_text(html)
    words = tokenize(text)
    frequencies = {}
    for w in words:
        root = porter_stemmer.stem(w)
        prev = frequencies.get(root, 0)
        frequencies[root] = prev + 1
    return frequencies

if __name__ == "__main__":
    pass