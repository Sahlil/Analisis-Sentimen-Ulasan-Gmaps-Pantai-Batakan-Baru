import pickle
import os
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neighbors import NearestNeighbors
from app import db
from app.models import Ulasan, RiwayatTraining
from imblearn.over_sampling import SMOTE
from collections import Counter
from app.lib.preprocessing import preprocess_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model_storage', 'sentiment_model.pkl')
SMOTE_METADATA_PATH = os.path.join(BASE_DIR, 'smote_metadata.json')

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


    y = df['label']

    split_kwargs = {
        'test_size': test_size,
        'random_state': 42,
        'stratify': y
    }
    if train_size is not None:
        split_kwargs['train_size'] = train_size

    df_train, df_test, y_train, y_test = train_test_split(df, y, **split_kwargs)

    # fit_transform hanya pada data training, transform saja pada data testing
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    x_train = vectorizer.fit_transform(df_train['text'])
    x_test = vectorizer.transform(df_test['text'])

    # Tandai data latih dan uji pada tabel ulasan
    all_ids = df['id'].tolist()
    train_ids = df_train['id'].tolist()
    test_ids = df_test['id'].tolist()

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

    distribusi_sebelum = dict(Counter(y_train))

    smote = SMOTE(random_state=42)
    x_train_res, y_train_res = smote.fit_resample(x_train, y_train)

    distribusi_sesudah = dict(Counter(y_train_res))

    clf = MultinomialNB()
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

    save_smote_metadata(distribusi_sebelum, distribusi_sesudah)

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
        "split_test": test_size,
        "distribusi_kelas_sebelum_smote": distribusi_sebelum,
        "distribusi_kelas_sesudah_smote": distribusi_sesudah
    }


def save_smote_metadata(data_before, data_after):
    payload = {
        "sebelum": data_before,
        "sesudah": data_after,
    }

    with open(SMOTE_METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _format_top_terms(vector_row, feature_names, top_n=5):
    dense_vector = vector_row.toarray().ravel() if hasattr(vector_row, 'toarray') else np.asarray(vector_row).ravel()
    nonzero_indices = np.flatnonzero(dense_vector)

    if nonzero_indices.size == 0:
        return []

    ranked_indices = nonzero_indices[np.argsort(dense_vector[nonzero_indices])[::-1][:top_n]]
    return [
        {
            'term': feature_names[index],
            'weight': float(dense_vector[index])
        }
        for index in ranked_indices
    ]


def _terms_to_text(top_terms):
    if not top_terms:
        return '-'

    return ', '.join(
        f"{item['term']} ({item['weight']:.4f})"
        for item in top_terms
    )


def build_smote_simulation_details(vectorizer, top_n=5, preferred_label='Netral'):
    data = Ulasan.query.filter(Ulasan.teks_clean != None, Ulasan.label != None).all()

    if not data:
        return None

    df = pd.DataFrame([{
        'id': row.id,
        'text': row.teks_clean,
        'label': row.label,
        'text_raw': row.teks_asli
    } for row in data])

    label_counts = df['label'].value_counts()
    if label_counts.empty:
        return None

    minority_label = None
    if preferred_label and preferred_label in label_counts and label_counts[preferred_label] >= 2:
        minority_label = preferred_label
    else:
        valid_labels = label_counts[label_counts >= 2].sort_values(kind='mergesort')
        if not valid_labels.empty:
            minority_label = valid_labels.index[0]

    if minority_label is None:
        return None

    minority_df = df[df['label'] == minority_label].sort_values('id').reset_index(drop=True)
    if len(minority_df) < 2:
        return None

    minority_vectors = vectorizer.transform(minority_df['text'])
    if minority_vectors.shape[0] < 2:
        return None

    nearest_neighbors = NearestNeighbors(n_neighbors=2, metric='cosine')
    nearest_neighbors.fit(minority_vectors)

    anchor_position = 0
    anchor_vector = minority_vectors[anchor_position]
    _, neighbor_indices = nearest_neighbors.kneighbors(anchor_vector, n_neighbors=2)

    if neighbor_indices.shape[1] < 2:
        return None

    neighbor_position = int(neighbor_indices[0][1])
    if neighbor_position == anchor_position:
        return None

    feature_names = vectorizer.get_feature_names_out()
    anchor_dense = anchor_vector.toarray().ravel()
    neighbor_vector = minority_vectors[neighbor_position]
    neighbor_dense = neighbor_vector.toarray().ravel()

    interpolation_factor = 0.5
    synthetic_dense = anchor_dense + interpolation_factor * (neighbor_dense - anchor_dense)

    anchor_terms = _format_top_terms(anchor_vector, feature_names, top_n=top_n)
    neighbor_terms = _format_top_terms(neighbor_vector, feature_names, top_n=top_n)
    synthetic_terms = _format_top_terms(synthetic_dense, feature_names, top_n=top_n)

    return {
        'minority_label': minority_label,
        'interpolation_factor': interpolation_factor,
        'rows': [
            {
                'status_data': 'Data Asli',
                'label_sentimen': minority_df.iloc[anchor_position]['label'],
                'fitur_kata_bobot': _terms_to_text(anchor_terms),
                'top_terms': anchor_terms,
                'teks_asli': minority_df.iloc[anchor_position]['text_raw']
            },
            {
                'status_data': 'Data Tetangga',
                'label_sentimen': minority_df.iloc[neighbor_position]['label'],
                'fitur_kata_bobot': _terms_to_text(neighbor_terms),
                'top_terms': neighbor_terms,
                'teks_asli': minority_df.iloc[neighbor_position]['text_raw']
            },
            {
                'status_data': 'Hasil SMOTE Sintetis',
                'label_sentimen': minority_label,
                'fitur_kata_bobot': _terms_to_text(synthetic_terms),
                'top_terms': synthetic_terms,
                'teks_asli': None
            }
        ]
    }
 
def predict_single(text_raw):
    try:
        with open(MODEL_PATH, 'rb') as f:
            vectorizer, clf = pickle.load(f)

        tokens = kw(text_raw)
        text_clean = " ".join(tokens)

        vec = vectorizer.transform([text_clean])

        if vec.nnz == 0:
            return "Netral"

        prediksi = clf.predict(vec)[0]

        return prediksi
    except FileNotFoundError:
        return "Model belum dilatih. Silakan latih model terlebih dahulu."

def predict_single_clean(text_clean):
    try:
        with open(MODEL_PATH, 'rb') as f:
            vectorizer, clf = pickle.load(f)

        vec = vectorizer.transform([text_clean])

        if vec.nnz == 0:
            return "Netral"

        prediksi = clf.predict(vec)[0]

        return prediksi
    except FileNotFoundError:
        return "Model belum dilatih. Silakan latih model terlebih dahulu."