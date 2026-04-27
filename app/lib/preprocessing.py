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

def preprocess_debug_steps(text):
    if not isinstance(text, str) or not text.strip():
        return {
            'original': text or '',
            'lowercased': '',
            'filtered': '',
            'collapsed_spaces': '',
            'tokens': [],
            'normalized_tokens': [],
            'negation_tokens': [],
            'stemmed_tokens': [],
            'final_tokens': []
        }

    original = text
    lowercased = text.lower()
    filtered = re.sub(r'[^a-z\s]', ' ', lowercased)
    collapsed_spaces = re.sub(r'\s+', ' ', filtered).strip()

    tokens = collapsed_spaces.split()

    normalized_tokens = [NORMALISASI.get(word, word) for word in tokens]

    negation_tokens = []
    i = 0
    while i < len(normalized_tokens):
        if normalized_tokens[i] in KATA_NEGASI and (i + 1) < len(normalized_tokens):
            word_next = normalized_tokens[i + 1]
            if word_next.strip():
                negation_tokens.append(f"{normalized_tokens[i]}_{word_next}")
                i += 2
            else:
                negation_tokens.append(normalized_tokens[i])
                i += 1
        else:
            negation_tokens.append(normalized_tokens[i])
            i += 1

    stemmed_tokens = []
    for token in negation_tokens:
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

        stemmed_tokens.append(stemmed_word)

    final_tokens = []
    for stemmed_word in stemmed_tokens:
        if (stemmed_word not in list_stopwords and
            stemmed_word not in STOPWORD_TAMBAHAN) or (stemmed_word in LEXICON):
            if stemmed_word.strip():
                final_tokens.append(stemmed_word)

    return {
        'original': original,
        'lowercased': lowercased,
        'filtered': filtered,
        'collapsed_spaces': collapsed_spaces,
        'tokens': tokens,
        'normalized_tokens': normalized_tokens,
        'negation_tokens': negation_tokens,
        'stemmed_tokens': stemmed_tokens,
        'final_tokens': final_tokens
    }

def label_sentiment(tokens):
    score = 0
    for token in tokens:
        if token in LEXICON:
            score += LEXICON[token]
            
    if score > 0:
        return "positif"
    elif score < 0:
        return "negatif"
    else:
        return "netral"