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
from parser import calculate_tf, html_to_text
from urllib.parse import urldefrag
import json, os, pickle

def create_inverted_index():
    '''
    Map with a token as a key and its list of its corresponding postings 
    '''
    inverted_index = {}
    visited_sites = set() 

    for doc_id, html in fetch_data():
        defragmented_link, fragment = urldefrag(doc_id)
        if (defragmented_link not in visited_sites and len(html_to_text(html)) > 1000):
            tf = calculate_tf(html)
            for term, frequency in tf.items():
                if term not in inverted_index:
                    inverted_index[term] = []
                inverted_index[term].append([defragmented_link, frequency])
            visited_sites.add(defragmented_link)

    return inverted_index

def save_index_to_split_pickle(inverted_index: dict):
    index = {}
    for i in range(97, 123):
        index[chr(i)] = {}

    for term, postings in inverted_index.items():
        first_letter_ascii = ord(term[0].lower())
        if first_letter_ascii >= 97 and first_letter_ascii <= 122:
            index[term[0].lower()][term] = postings
    
    for letter, postings in index.items():
        offsets = {}
        with open(f"{letter}.pkl", "wb") as f:
            pickle.dump(postings, f)    
            for term, postings in postings.items():
                offset = f.tell()
                offsets[term] = offset
                pickle.dump((term, postings), f)
        with open(f"{letter}_offsets.pkl", "wb") as f:
            pickle.dump(offsets, f)

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
    save_index_to_split_pickle(inverted_index)
    # print(f"Number of indexed documents: {number_of_indexed_documents(inverted_index)}")
    # print(f"Number of unique tokens: {number_of_unique_tokens(inverted_index)}")
    # print(f"Total Size in KB: {total_size()}")
