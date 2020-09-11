# Install dependencies first
#     pip install spacy wikipedia
#     python -m spacy download en
# Run
#     python tfidf.py

from collections import Counter
import math

import wikipedia
import spacy

nlp = spacy.load('en')

pages = [
  "The Tigger Movie 2000", "Dinosaur 2000 Movie", "The Emperor's New Groove 2000", "Recess School's Out", "Atlantis: The Lost Empire", "Monsters, Inc", "Return to Never Land", "Lilo & Stitch", "Treasure Planet 2002", "The Jungle Book 2 2003", "Piglet's Big Movie 2003", "Finding Nemo 2003", "Brother Bear 2003", "Teacher's Pet 2004", "Home on the Range 2004", "The Incredibles 2004", "Pooh's Heffalump Movie 2005", "Valiant 2005", "Chicken Little 2005", "The Wild 2006", "Cars 2006", "The Nightmare Before Christmas", "Meet the Robinsons 2007", "Ratatouille 2007", "WALL-E 2008", "Roadside Romeo 2008", "Bolt 2008", "Up 2009",
  "A Christmas Carol 2009", "The Princess and the Frog 2009", "Toy Story", "Toy Story 2", "Toy Story 3", "Tangled", "Mars Needs Moms", "Cars 2", "Winnie the Pooh 2011", "Arjun: The Warrior Prince", "Brave 2012", "Frankenweenie", "Wreck-It Ralph", "Monsters University", "Planes film", "Frozen 2013", "Planes: Fire & Rescue", "Big Hero 6", "Inside Out", "The Good Dinosaur", "Zootopia", "Finding Dory", "Moana 2016", "Cars 3", "Coco 2017 film", "Incredibles 2",
  "Shrek", "Shrek 2", "Shrek 3", "Antz", "A bugs life", "Bee movie", "Madagascar 2005 film", "Madagascar 2", "Kung fu panda", "Kung fu panda 2","Kung fu panda 3",
]

def valid_token(tk):
    is_valid = tk.is_alpha
    return is_valid and not tk.is_stop

def get_lemma(tk):
    if tk.pos_ == 'PRON' or tk.lemma_ == '-PRON-':
        return tk.text.lower()
    return tk.lemma_.lower()

def read_wikipedia_page(page_name):
    page = wikipedia.page(page_name)
    content = page.content
    return content

def tokenize_page(page_name):
  text = read_wikipedia_page(page_name)
  return [
    get_lemma(t)
    for t in nlp(text)
    if valid_token(t)
  ]

vocabulary = set()
idf_counter = Counter()

for page in pages:
  print("   Processing page {}...".format(page))
  page_words = set(tokenize_page(page))
  vocabulary = vocabulary | page_words
  idf_counter.update(page_words)

print("All pages processed")

idf = {
  word: math.log(len(pages)/df, 2)
  for word, df in idf_counter.items()
}

print("vocabulary size: {}".format(len(vocabulary)))


def analyze_page(target_page):
  target_words = tokenize_page(target_page)
  tfidf =  {
    word: (1 + math.log(_tf, 2)) * idf[word]
    for word, _tf in Counter(target_words).items()
  }
  num_words = 20
  most_frequent = [
    w  for (w, _) in Counter(target_words).most_common(num_words)
  ]
  sorted_tfidf = [
    w  for (w, _) in sorted(tfidf.items(), key=lambda kv: kv[1], reverse=True)
  ]
  print(target_page)
  print("Most frequent: {}".format(most_frequent))
  print("Higher TF-IDF: {}".format(sorted_tfidf[:num_words]))


analyze_page("Moana")
analyze_page("The Incredibles 2004")
analyze_page("Monsters, Inc")
