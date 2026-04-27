import pickle
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from app import db
from app.models import Ulasan, RiwayatTraining
from imblearn.over_sampling import SMOTE
from app.lib.preprocessing import preprocess_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model_storage', 'sentiment_model.pkl')

def train_naive_bayes(test_size=0.2, train_size=None, split_ratio=None):
    data = Ulasan.query.filter(Ulasan.teks_clean != None, Ulasan.label != None).all()

    if not data:
        return {'status': 'error', 'message': 'Data kosong.'}

    if test_size is None or test_size <= 0 or test_size >= 1:
        return {'status': 'error', 'message': 'Nilai test size tidak valid.'}

    if train_size is not None and (train_size <= 0 or train_size >= 1):
        return {'status': 'error', 'message': 'Nilai train size tidak valid.'}

    if train_size is not None and (train_size + test_size) > 1:
        return {'status': 'error', 'message': 'Total split melebihi 100%.'}

    df = pd.DataFrame([{
        'id': d.id,
        'text': d.teks_clean,
        'label': d.label
    } for d in data])


    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    x = vectorizer.fit_transform(df['text'])
    y = df['label']

    idx_all = np.arange(len(df))

    split_kwargs = {
        'test_size': test_size,
        'random_state': 42,
        'stratify': y
    }
    if train_size is not None:
        split_kwargs['train_size'] = train_size

    idx_train, idx_test, y_train, y_test = train_test_split(idx_all, y, **split_kwargs)
    x_train = x[idx_train]
    x_test = x[idx_test]

    # Tandai data latih dan uji pada tabel ulasan
    all_ids = df['id'].tolist()
    train_ids = df.iloc[idx_train]['id'].tolist()
    test_ids = df.iloc[idx_test]['id'].tolist()

    if all_ids:
        Ulasan.query.filter(Ulasan.id.in_(all_ids)).update(
            {"tipe_data": "uji"},
            synchronize_session=False
        )
    if train_ids:
        Ulasan.query.filter(Ulasan.id.in_(train_ids)).update(
            {"tipe_data": "latih"},
            synchronize_session=False
        )
    if test_ids:
        Ulasan.query.filter(Ulasan.id.in_(test_ids)).update(
            {"tipe_data": "uji"},
            synchronize_session=False
        )
    db.session.commit()

    smote = SMOTE(random_state=42)
    x_train_res, y_train_res = smote.fit_resample(x_train, y_train)

    clf =  ComplementNB()
    clf.fit(x_train_res, y_train_res)

    y_pred = clf.predict(x_test)
    akurasi = accuracy_score(y_test, y_pred)
    laporan = classification_report(y_test, y_pred, output_dict=True)

    labels = clf.classes_ 
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    label_index = {label.lower(): idx for idx, label in enumerate(labels)}

    def cm_value(actual_label, pred_label):
        actual_key = actual_label.lower()
        pred_key = pred_label.lower()
        if actual_key not in label_index or pred_key not in label_index:
            return 0
        return int(cm[label_index[actual_key]][label_index[pred_key]])

    if not split_ratio and train_size is not None and test_size is not None:
        split_ratio = f"{int(train_size * 100)}:{int(test_size * 100)}"

    riwayat = RiwayatTraining(
        jumlah_data=len(df),
        rasio_split=split_ratio or "",
        akurasi=round(akurasi * 100, 2),
        presisi=laporan['weighted avg']['precision'],
        recall=laporan['weighted avg']['recall'],
        f1_score=laporan['weighted avg']['f1-score'],
        neg_neg=cm_value('negatif', 'negatif'),
        neg_neu=cm_value('negatif', 'netral'),
        neg_pos=cm_value('negatif', 'positif'),
        neu_neg=cm_value('netral', 'negatif'),
        neu_neu=cm_value('netral', 'netral'),
        neu_pos=cm_value('netral', 'positif'),
        pos_neg=cm_value('positif', 'negatif'),
        pos_neu=cm_value('positif', 'netral'),
        pos_pos=cm_value('positif', 'positif')
    )
    db.session.add(riwayat)
    db.session.commit()

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump((vectorizer, clf), f)

    return {
        'status': 'success',
        'akurasi': round(akurasi * 100, 2),
        'detail': laporan,
        'confusion_matrix': cm.tolist(),
        'labels': labels.tolist(),
        "jumlah_data_awal": len(df),
        "jumlah_data_setelah_smote": len(y_train_res),
        "split_train": train_size,
        "split_test": test_size
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