'''
nltk library

Not allowed to use Lucene, PyLucene, or ElasticSearch.

Indexer:
Create an inverted index for the given corpus with data structures designed by you.

Tokens: all alphanumeric sequences in the dataset.
Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.

The inverted index is simply a map with the token as a key and a list of its corresponding postings.
A posting is the representation of the token’s occurrence in a document.

'''

from loads import fetch_data
from parser import calculate_tf
import json, os

def create_inverted_index():
    '''
    Map with a token as a key and its list of its corresponding postings 
    '''
    inverted_index = {}

    for doc_id, html in fetch_data():
        tf = calculate_tf(html)
        for term, frequency in tf.items():
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append([doc_id, frequency])

    return inverted_index

def save_index_to_json(inverted_index: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(inverted_index, f)

def number_of_indexed_documents(inverted_index: dict):
    docs = set()
    for posting in inverted_index.values():
        for doc_id, html in posting:
            docs.add(doc_id)
    return len(docs)

def number_of_unique_tokens(inverted_index: dict):
    return len(inverted_index.keys())

def total_size():
    file_path = "inverted_index.json"
    if os.path.exists(file_path):
        size_kb = os.path.getsize(file_path) / 1024 
        return size_kb

if __name__ == "__main__":
    inverted_index = create_inverted_index()
    save_index_to_json(inverted_index)
    print(f"Number of indexed documents: {number_of_indexed_documents(inverted_index)}")
    print(f"Number of unique tokens: {number_of_unique_tokens(inverted_index)}")
    print(f"Total Size in KB: {total_size()}")
