import json, math, time, pickle
from parser import tokenize, porter_stemmer

def read_postings(letter, offset, query):
    with open(f"{letter}.pkl", "rb") as f:
        f.seek(offset)
        s_term, postings = pickle.load(f)
        if s_term == query:
            return postings
    return None

def load_postings(query):
    first_letter_ascii = ord(query[0].lower())
    if 97 <= first_letter_ascii <= 122:
        first_letter = query[0].lower()
        with open(f"{first_letter}_offsets.pkl", "rb") as f:
            offsets = pickle.load(f)
        if query not in offsets:
            return None
        offset = offsets[query]
        return read_postings(first_letter, offset, query)
    return None      
    
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
    total_documents = 55093 ## Report Number 

    postings_map = {}
    for stem in stems:
        postings = load_postings(stem)
        if postings is None:
            continue 
        postings_map[stem] = dict(postings)

    if not postings_map:
        return {}  
        
    sets = []
    for p in postings_map.values():
        sets.append(set(p.keys()))
    documents = intersect(sets)

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
    start_time = time.time()
    stems = query_parsing(query)
    hits = document_tfidf(stems)
    top5 = sorted(hits.items(), key=lambda item: item[1], reverse=True)[:5]

    print("stems =", stems)
    print("total hits =", len(hits))
    print("top 5 URLs:")
    for document in top5:
        print("    ", document[0])

    end_time = time.time()
    elapsed_ms = (end_time - start_time) * 1000
    print(elapsed_ms)