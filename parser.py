import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

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
    frequencies: dict[str, int] = {}
    for w in words:
        root = porter_stemmer.stem(w)
        prev = frequencies.get(root, 0)
        frequencies[root] = prev + 1
    return frequencies

if __name__ == "__main__":
    sample = """
    <html>
      <head>
        <title>Artificial Intelligence @ UCI</title>
      </head>
      <body>
        <h1>Welcome to AI@UCI!</h1>
        <p>
          AI@UCI is a <strong>student-run</strong> organization
          focused on <em>machine learning</em> and <em>data science</em>.
        </p>
        <h2>Upcoming Events</h2>
        <ul>
          <li>Workshop: <a href="#">Deep Learning 101</a></li>
          <li>Seminar: Ethics in AI</li>
          <li>Hackathon: Build an AI Agent</li>
        </ul>
        <p>
          Visit our <a href="https://aiclub.ics.uci.edu">website</a>
          or email us at <a href="mailto:aiatuci@gmail.com">aiatuci@gmail.com</a>.
        </p>
      </body>
    </html>
    """
    print(calculate_tf(sample))
