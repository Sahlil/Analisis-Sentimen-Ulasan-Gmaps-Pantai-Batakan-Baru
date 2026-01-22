import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import accuracy_score, classification_report
from app.models import Ulasan
from imblearn.over_sampling import SMOTE
from app.lib.preprocessing import preprocess_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model_storage', 'sentiment_model.pkl')

def train_naive_bayes():
    data = Ulasan.query.filter(Ulasan.teks_clean != None, Ulasan.label != None).all()

    if not data:
        return {'status': 'error', 'message': 'Data kosong.'}

    df = pd.DataFrame([{
        'text': d.teks_clean,
        'label': d.label
    } for d in data])


    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    x = vectorizer.fit_transform(df['text'])
    y = df['label']

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    smote = SMOTE(random_state=42)
    x_train_res, y_train_res = smote.fit_resample(x_train, y_train)

    clf =  ComplementNB()
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    akurasi = accuracy_score(y_test, y_pred)
    laporan = classification_report(y_test, y_pred, output_dict=True)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump((vectorizer, clf), f)

    return {
        'status': 'success',
        'akurasi': round(akurasi * 100, 2),
        'detail': laporan,
        "jumlah_data_awal": len(df),
        "jumlah_data_setelah_smote": len(y_train_res)
    }

def predict_single(text_raw):
    try:
        with open(MODEL_PATH, 'rb') as f:
            vectorizer, clf = pickle.load(f)

        tokens = preprocess_text(text_raw)
        text_clean = " ".join(tokens)

        vec = vectorizer.transform([text_clean])

        if vec.nnz == 0:
            return "Netral"

        prediksi = clf.predict(vec)[0]

        return prediksi
    except FileNotFoundError:
        return "Model belum dilatih. Silakan latih model terlebih dahulu."