import os
import pickle
import pandas as pd
import numpy as np
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models import Ulasan, RiwayatTraining
from app.lib.preprocessing import preprocess_text, label_sentiment, preprocess_debug_steps
from app.lib.machine_learning import train_naive_bayes, predict_single, predict_single_clean, MODEL_PATH

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def build_hasil_from_riwayat(riwayat):
    labels = ['Negatif', 'Netral', 'Positif']
    cm = [
        [riwayat.neg_neg, riwayat.neg_neu, riwayat.neg_pos],
        [riwayat.neu_neg, riwayat.neu_neu, riwayat.neu_pos],
        [riwayat.pos_neg, riwayat.pos_neu, riwayat.pos_pos]
    ]

    total = sum(sum(row) for row in cm)
    detail = {}
    precisions = []
    recalls = []
    f1_scores = []
    supports = []

    for i, label in enumerate(labels):
        tp = cm[i][i]
        fp = sum(cm[r][i] for r in range(3)) - tp
        fn = sum(cm[i]) - tp
        support = sum(cm[i])

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

        detail[label] = {
            'precision': precision,
            'recall': recall,
            'f1-score': f1,
            'support': support
        }

        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
        supports.append(support)

    if supports and total > 0:
        weighted_precision = sum(p * s for p, s in zip(precisions, supports)) / total
        weighted_recall = sum(r * s for r, s in zip(recalls, supports)) / total
        weighted_f1 = sum(f * s for f, s in zip(f1_scores, supports)) / total
    else:
        weighted_precision = 0
        weighted_recall = 0
        weighted_f1 = 0

    macro_precision = sum(precisions) / 3 if precisions else 0
    macro_recall = sum(recalls) / 3 if recalls else 0
    macro_f1 = sum(f1_scores) / 3 if f1_scores else 0

    detail['macro avg'] = {
        'precision': macro_precision,
        'recall': macro_recall,
        'f1-score': macro_f1,
        'support': total
    }
    detail['weighted avg'] = {
        'precision': weighted_precision,
        'recall': weighted_recall,
        'f1-score': weighted_f1,
        'support': total
    }

    return {
        'akurasi': riwayat.akurasi,
        'detail': detail,
        'confusion_matrix': cm,
        'labels': labels
    }

def load_model_details(top_n=10, likelihood_top_n=5):
    if not os.path.exists(MODEL_PATH):
        return None

    with open(MODEL_PATH, 'rb') as f:
        vectorizer, clf = pickle.load(f)

    feature_names = vectorizer.get_feature_names_out()
    idf_values = vectorizer.idf_
    top_tfidf_idx = np.argsort(idf_values)[::-1][:top_n]
    tfidf_top = [
        {'term': feature_names[i], 'idf': float(idf_values[i])}
        for i in top_tfidf_idx
    ]

    priors = [
        {
            'label': label,
            'log_prior': float(clf.class_log_prior_[idx]),
            'prior': float(np.exp(clf.class_log_prior_[idx]))
        }
        for idx, label in enumerate(clf.classes_)
    ]

    likelihoods = []
    for class_idx, label in enumerate(clf.classes_):
        weights = clf.feature_log_prob_[class_idx]
        top_idx = np.argsort(weights)[::-1][:likelihood_top_n]
        words = [
            {'term': feature_names[i], 'weight': float(weights[i])}
            for i in top_idx
        ]
        likelihoods.append({'label': label, 'words': words})

    simulation = None
    sample = (
        Ulasan.query.filter_by(tipe_data='uji')
        .filter(Ulasan.teks_clean != None)
        .order_by(func.rand())
        .first()
    )

    if sample:
        tokens = preprocess_text(sample.teks_asli)
        vocab = vectorizer.vocabulary_
        class_scores = []

        for class_idx, label in enumerate(clf.classes_):
            log_prior = float(clf.class_log_prior_[class_idx])
            token_logs = []
            weight_sum = 0.0

            for token in tokens:
                token_idx = vocab.get(token)
                if token_idx is None:
                    continue
                weight = float(clf.feature_log_prob_[class_idx][token_idx])
                weight_sum += weight
                token_logs.append({'token': token, 'weight': weight})

            score = log_prior + weight_sum
            class_scores.append({
                'label': label,
                'log_prior': log_prior,
                'weight_sum': weight_sum,
                'score': score,
                'token_logs': token_logs
            })

        simulation = {
            'text': sample.teks_asli,
            'tokens': tokens,
            'class_scores': class_scores
        }

    return {
        'tfidf_top': tfidf_top,
        'priors': priors,
        'likelihoods': likelihoods,
        'simulation': simulation
    }

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_ulasan = Ulasan.query.count()
    jml_positif = Ulasan.query.filter_by(label='Positif').count()
    jml_negatif = Ulasan.query.filter_by(label='Negatif').count()
    jml_netral = Ulasan.query.filter_by(label='Netral').count()
    jml_belum = Ulasan.query.filter_by(label=None).count()

    return render_template('admin/dashboard.html', 
                            total=total_ulasan,
                            positif=jml_positif,
                            negatif=jml_negatif,
                            netral=jml_netral,
                            belum=jml_belum)


@admin_bp.route('/data_ulasan')
@login_required
def data_ulasan():
    ulasan_list = Ulasan.query.all()
    return render_template('admin/data_ulasan.html', ulasan_list=ulasan_list)

@admin_bp.route('/data_ulasan/<int:id>')
@login_required
def detail_ulasan(id):
    ulasan = Ulasan.query.get_or_404(id)
    steps = preprocess_debug_steps(ulasan.teks_asli)
    final_label = label_sentiment(steps['final_tokens']) if steps['final_tokens'] else None
    return render_template(
        'admin/detail_ulasan.html',
        ulasan=ulasan,
        steps=steps,
        final_label=final_label
    )

@admin_bp.route('/data_split')
@login_required
def data_split():
    data_latih = Ulasan.query.filter_by(tipe_data='latih').order_by(Ulasan.tanggal_input.desc()).all()
    data_uji = Ulasan.query.filter_by(tipe_data='uji').order_by(Ulasan.tanggal_input.desc()).all()
    return render_template('admin/data_split.html', data_latih=data_latih, data_uji=data_uji)


@admin_bp.route('/import', methods=['POST'])
@login_required
def import_ulasan():
    file = request.files.get('file_excel')

    if not file:
        flash('Tidak ada file yang diunggah.', 'danger')
        return redirect(url_for('admin.data_ulasan'))

    try:
        if file.filename.endswith   ('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
    
        if 'Ulasan' not in df.columns:
            flash("File harus memiliki kolom 'Ulasan'.", 'danger')
            return redirect(url_for('admin.data_ulasan'))

        jumlah_masuk = 0
        for index, row in df.iterrows():
            teks = row['Ulasan']

            if pd.notna(teks) and str(teks).strip() != '':
                baru = Ulasan(teks_asli=str(teks))
                db.session.add(baru)
                jumlah_masuk += 1

        db.session.commit()
        flash(f'Berhasil mengimpor {jumlah_masuk} ulasan.', 'success')

    except Exception as e:
        flash(f'Gagal mengimpor ulasan: {str(e)}', 'danger')

    return redirect(url_for('admin.data_ulasan'))

@admin_bp.route('/hapus_ulasan/<int:id>', methods=['POST'])
@login_required
def hapus_ulasan(id):
    data = Ulasan.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    flash('Ulasan berhasil dihapus.', 'success')
    return redirect(url_for('admin.data_ulasan'))
    
@admin_bp.route('/tambah_manual', methods=['GET', 'POST'])
@login_required
def tambah_manual():
    if request.method == 'POST':
        daftar_ulasan = request.form.getlist('ulasan[]')

        jumlah_suskses = 0

        for teks in daftar_ulasan:
            if teks.strip():
                baru = Ulasan(teks_asli=teks)
                db.session.add(baru)
                jumlah_suskses += 1

        if jumlah_suskses > 0:
            db.session.commit()
            flash(f'Berhasil menambahkan {jumlah_suskses} ulasan.', 'success')
        else:
            flash('Tidak ada ulasan yang ditambahkan.', 'warning')
            
    return render_template('admin/tambah_manual.html')

@admin_bp.route('/proses_preprocessing')
@login_required
def proses_preprocessing():
    data_mentah = Ulasan.query.filter(Ulasan.teks_clean == None).all()

    if not data_mentah:
        flash('Tidak ada data ulasan mentah yang perlu diproses.', 'info')
        return redirect(url_for('admin.data_ulasan'))

    total = len(data_mentah)
    batch_size = 50
    jumlah = 0

    for i in range(0, total, batch_size):
        batch = data_mentah[i:i+batch_size]
        
        for item in batch:
            tokens = preprocess_text(item.teks_asli)
            clean_text = ' '.join(tokens)
            label = label_sentiment(tokens)

            item.teks_clean = clean_text
            item.label = label
            jumlah += 1
            
            # Log progress setiap 10 item
            if jumlah % 10 == 0:
                print(f"Progress: {jumlah}/{total} ({jumlah/total*100:.1f}%)")
        
        # Commit per batch untuk mencegah memory overflow
        db.session.commit()
        print(f"✅ Batch {i//batch_size + 1} selesai ({jumlah}/{total})")

    flash(f'Berhasil memproses {jumlah} ulasan.', 'success')
    return redirect(url_for('admin.data_ulasan'))

@admin_bp.route('/training_model')
@login_required
def training_model():
    riwayat_list = RiwayatTraining.query.order_by(RiwayatTraining.tanggal_training.desc()).all()
    latest = riwayat_list[0] if riwayat_list else None
    hasil = build_hasil_from_riwayat(latest) if latest else None
    split_ratio = latest.rasio_split if latest else '80:20'
    total_data = latest.jumlah_data if latest else None
    model_details = load_model_details()
    return render_template(
        'admin/training_model.html',
        hasil=hasil,
        split_ratio=split_ratio,
        riwayat_list=riwayat_list,
        total_data=total_data,
        model_details=model_details
    )

@admin_bp.route('/riwayat_training/<int:riwayat_id>')
@login_required
def riwayat_training_detail(riwayat_id):
    riwayat = RiwayatTraining.query.get_or_404(riwayat_id)
    riwayat_list = RiwayatTraining.query.order_by(RiwayatTraining.tanggal_training.desc()).all()
    hasil = build_hasil_from_riwayat(riwayat)
    model_details = load_model_details()
    return render_template(
        'admin/training_model.html',
        hasil=hasil,
        split_ratio=riwayat.rasio_split,
        riwayat_list=riwayat_list,
        selected_riwayat=riwayat,
        total_data=riwayat.jumlah_data,
        model_details=model_details
    )

@admin_bp.route('/proses_training', methods=['POST'])
@login_required
def proses_training():
    split_ratio = request.form.get('split_ratio', '80:20')
    split_map = {
        '90:10': (0.9, 0.1),
        '85:15': (0.85, 0.15),
        '80:20': (0.8, 0.2),
        '75:25': (0.75, 0.25),
        '70:30': (0.7, 0.3),
        '65:35': (0.65, 0.35),
        '60:40': (0.6, 0.4)
    }

    if split_ratio not in split_map:
        flash('Pilihan split data tidak valid.', 'danger')
        return redirect(url_for('admin.training_model'))

    train_size, test_size = split_map[split_ratio]

    hasil = train_naive_bayes(test_size=test_size, train_size=train_size, split_ratio=split_ratio)

    if hasil['status'] == 'error':
        flash(hasil.get('message', 'Terjadi kesalahan saat training.'), 'danger')
    else:
        flash(f"Model berhasil dilatih dengan akurasi {hasil['akurasi']}%", 'success')
        return redirect(url_for('admin.training_model'))

    return redirect(url_for('admin.training_model'))


@admin_bp.route('/simulasi', methods=['GET', 'POST'])
@login_required
def simulasi():
    hasil_prediksi = None
    teks_input = ''
    teks_clean = ''

    if request.method == 'POST':
        teks_input = request.form.get('teks_input', '')

        if teks_input:
            tokens = preprocess_text(teks_input)
            teks_clean = " ".join(tokens)

        if teks_clean:
            hasil_prediksi = predict_single_clean(teks_clean)

    return render_template('admin/simulasi.html',
                           hasil=hasil_prediksi,
                           teks_input=teks_input)
