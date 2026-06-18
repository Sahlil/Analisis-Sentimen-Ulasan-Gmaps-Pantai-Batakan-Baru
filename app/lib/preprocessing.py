import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import nltk
from app.lib.dictionary import (
    NORMALISASI,
    LEXICON,
    LEXICON_COMPONENT_TOKENS,
    LEXICON_PATTERN_LENGTHS,
    STOPWORD_TAMBAHAN,
    KATA_NEGASI,
)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

list_stopwords = set(stopwords.words('indonesian'))
list_stopwords = list_stopwords - KATA_NEGASI


def _score_tokens_with_lexicon(tokens):
    lexicon_lengths = LEXICON_PATTERN_LENGTHS or [1]
    matches = []
    total_score = 0

    i = 0
    while i < len(tokens):
        matched = False

        for length in lexicon_lengths:
            if length <= 0 or i + length > len(tokens):
                continue

            candidate = '_'.join(tokens[i:i + length])
            if candidate in LEXICON:
                score = LEXICON[candidate]
                matches.append({'token': candidate, 'score': score})
                total_score += score
                i += length
                matched = True
                break

        if not matched:
            i += 1

    return matches, total_score

def preprocess_text(text):
    if not isinstance(text, str) or not text.strip():
        return []

    # 1. Case Folding & Pembersihan Karakter
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text) 
    text = re.sub(r'\s+', ' ', text).strip()
    
    tokens = text.split()

    # 2. Normalisasi (Memperbaiki typo / bahasa gaul)
    tokens = [NORMALISASI.get(word, word) for word in tokens]

    # 3. Penanganan Negasi (Menggabungkan kata "tidak" dengan kata setelahnya)
    new_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i] in KATA_NEGASI and (i + 1) < len(tokens):
            word_next = tokens[i+1]
            
            # --- TAMBAHAN LOGIKA KHUSUS UNTUK KATA "ADA" ---
            if word_next == "ada" and (i + 2) < len(tokens):
                word_after_ada = tokens[i+2]
                if word_after_ada.strip():
                    # Gabungkan menjadi 3 kata: "tidak_ada_sampah"
                    new_tokens.append(f"{tokens[i]}_ada_{word_after_ada}")
                    i += 3
                    continue # Lompat 3 langkah dan lanjut ke iterasi berikutnya
            # -----------------------------------------------

            # Jika bukan kata "ada", lakukan penggabungan normal (2 kata)
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

    # 4. Stemming & Stopword Removal (Dengan Proteksi Lexicon)
    processed_tokens = []
    for token in tokens:
        # Lakukan stemming, perhatikan jika token adalah kata negasi gabungan
        if '_' in token:
            parts = token.split('_')
            if len(parts) > 1 and parts[1]: 
                kata_dasar = stemmer.stem(parts[1])
                stemmed_token = f"{parts[0]}_{kata_dasar}"
            else:
                stemmed_token = token
        else:
            stemmed_token = stemmer.stem(token)

        # -- LOGIKA PROTEKSI STOPWORD BARU --
        # Cek apakah kata ini masuk dalam daftar stopword
        is_stopword = (stemmed_token in list_stopwords) or (stemmed_token in STOPWORD_TAMBAHAN)
        is_protected = (stemmed_token in LEXICON_COMPONENT_TOKENS) or (stemmed_token in LEXICON)

        # Hanya simpan kata yang BUKAN stopword, ATAU merupakan kata yang dilindungi
        if not is_stopword or is_protected:
            if stemmed_token.strip():
                processed_tokens.append(stemmed_token)

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
            'final_tokens': [],
            'lexicon_scores': [],
            'total_score': 0
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
        if (
            stemmed_word not in list_stopwords
            and stemmed_word not in STOPWORD_TAMBAHAN
        ) or (stemmed_word in LEXICON) or (stemmed_word in LEXICON_COMPONENT_TOKENS):
            if stemmed_word.strip():
                final_tokens.append(stemmed_word)

    lexicon_scores, total_score = _score_tokens_with_lexicon(final_tokens)

    return {
        'original': original,
        'lowercased': lowercased,
        'filtered': filtered,
        'collapsed_spaces': collapsed_spaces,
        'tokens': tokens,
        'normalized_tokens': normalized_tokens,
        'negation_tokens': negation_tokens,
        'stemmed_tokens': stemmed_tokens,
        'final_tokens': final_tokens,
        'lexicon_scores': lexicon_scores,
        'total_score': total_score
    }

def label_sentiment(tokens):
    score = _score_tokens_with_lexicon(tokens)[1]
            
    if score > 0:
        return "positif"
    elif score < 0:
        return "negatif"
    else:
        return "netral"