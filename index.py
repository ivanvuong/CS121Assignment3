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
from parser import compute_tf

def create_inverted_index():
    '''
    Map with a token as a key and its list of its corresponding postings 

    Example:

    "the" : {DOCUMENTID/DOCUMENTNAME, TERM FREQUENCY}
    '''
    docs = fetch_data()
    inverted_index = {}

    for doc_id, html in docs.items():
        tf = calculate_tf(html)
        for term, frequency in tf.items():
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append((doc_id, frequency))
    return inverted_index

def number_of_indexed_documents():
    pass

def number_of_unique_tokens():
    pass

def total_size():
    pass 


def main():
    pass

if __name__ == "__main__":
    print("hello")
