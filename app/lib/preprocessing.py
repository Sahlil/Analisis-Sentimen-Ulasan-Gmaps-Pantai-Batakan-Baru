import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import nltk
from app.lib.dictionary import NORMALISASI, LEXICON, STOPWORD_TAMBAHAN, KATA_NEGASI

factory = StemmerFactory()
stemmer = factory.create_stemmer()

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

list_stopwords = set(stopwords.words('indonesian'))
list_stopwords = list_stopwords - KATA_NEGASI

def preprocess_text(text):
    if not isinstance(text, str) or not text.strip():
        return []

    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text) 
    text = re.sub(r'\s+', ' ', text).strip()
    
    tokens = text.split()

    tokens = [NORMALISASI.get(word, word) for word in tokens]

    new_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i] in KATA_NEGASI and (i + 1) < len(tokens):
            word_next = tokens[i+1]
            if word_next.strip():
                new_tokens.append(f"{tokens[i]}_{word_next}")
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        else:
            new_tokens.append(tokens[i])
            i += 1
    
    tokens = new_tokens

    processed_tokens = []
    for token in tokens:
        stemmed_word = token 

        if '_' in token:
            parts = token.split('_')
            if len(parts) > 1 and parts[1]: 
                kata_dasar = stemmer.stem(parts[1])
                stemmed_word = f"{parts[0]}_{kata_dasar}"
            else:
                stemmed_word = token
        else:
            if token: 
                stemmed_word = stemmer.stem(token)

        if (stemmed_word not in list_stopwords and 
            stemmed_word not in STOPWORD_TAMBAHAN) or (stemmed_word in LEXICON):
            if stemmed_word.strip():
                processed_tokens.append(stemmed_word)

    return processed_tokens

def label_sentiment(tokens):
    score = 0
    for token in tokens:
        if token in LEXICON:
            score += LEXICON[token]
            
    if score > 0:
        return "Positif"
    elif score < 0:
        return "Negatif"
    else:
        return "Netral"