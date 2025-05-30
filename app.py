from flask import Flask, request, render_template
from search import query_parsing, document_tfidf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    stems = []
    hits = {}
    top5 = []

    if request.method == "POST":
        query = request.form["query"]
        stems = query_parsing(query)
        hits = document_tfidf(stems)
        top5 = sorted(hits.items(), key=lambda item: item[1], reverse=True)[:5]

    return render_template("index.html", stems=stems, hits=hits, top5=top5)

if __name__ == "__main__":
    app.run(debug=True)