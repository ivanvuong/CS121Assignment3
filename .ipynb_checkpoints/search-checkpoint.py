import json, math, time 
from parser import tokenize, porter_stemmer

def load_postings(query):
    first_letter = ord(query[0])    
    file_name = ""
    if first_letter >= 97 and first_letter <= 102:
        file_name = "a-f.json"
    elif first_letter >= 103 and first_letter <= 108:
        file_name = "g-l.json"
    elif first_letter >= 109 and first_letter <= 114:
        file_name = "m-r.json"
    elif first_letter >= 115 and first_letter <= 122:
        file_name = "s-z.json" 
    with open(file_name, 'r', encoding='utf-8') as f:
        index = json.load(f)
        return index[query]
    
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
    for doc_id, freq in postings:
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

def document_tfidf(stems):
    scores = {}
    documents = and_query(stems)
    total_documents = 55093 ## Report Number 

    postings_map = {}
    for stem in stems:
        postings_map[stem] = dict(load_postings(stem))

    for document in documents:
        score = 0
        for stem in stems:
            postings_dict = postings_map[stem]
            term_frequency = postings_dict.get(document, 0)
            document_frequency = len(postings_dict)
            score += term_frequency * (math.log(total_documents / (1 + document_frequency)))
        scores[document] = score

    return scores

if __name__ == "__main__":
    query = input("Enter search query: ")
    stems = query_parsing(query)
    hits = document_tfidf(stems)
    top5 = sorted(hits.items(), key=lambda item: item[1], reverse=True)[:5]

    print("stems =", stems)
    print("total hits =", len(hits))
    print("top 5 URLs:")
    for document in top5:
        print("    ", document[0])