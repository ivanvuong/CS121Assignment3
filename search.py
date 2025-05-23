import json
from parser import tokenize, porter_stemmer

INDEX_FILE = "inverted_index.json"
result = {}
with open('inverted_index.json', 'r') as f:
    result = json.load(f)

def load_postings(term):
    return result[term]
    
def query_parsing(query):
    tokens = tokenize(query)
    stems = []
    for t in tokens:
        stem_t = porter_stemmer.stem(t)
        stems.append(stem_t)
    return stems

def get_docs(term):
    postings = load_postings(term)  
    doc_ids = set()
    for doc_id, _ in postings:
        doc_ids.add(doc_id)
    return doc_ids

def intersect(sets):
    if not sets:
        return set()
    result = sets[0]
    for i in sets[1:]:
        result = result.intersection(i)
        if not result:
            break
    return result

def and_query(terms):
    posting_sets = []
    for stem in terms:
        docs = get_docs(stem)
        posting_sets.append(docs)
    return intersect(posting_sets)

if __name__ == "__main__":
    queries = ["cristina lopes", "machine learning", "acm", "master of software engineering"]

    for query in queries:
        stems = query_parsing(query)
        hits = and_query(stems)
        top5 = sorted(hits)[:5]  

        print(f"Query: {query}")
        print("stems =", stems)
        print("total hits =", len(hits))
        print("top 5 URLs:")
        for url in top5:
            print("    ", url)