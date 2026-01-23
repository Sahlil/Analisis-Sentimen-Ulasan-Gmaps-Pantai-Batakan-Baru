import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Ulasan
from app.lib.preprocessing import preprocess_text, label_sentiment
from app.lib.machine_learning import train_naive_bayes, predict_single

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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
    return render_template('admin/training_model.html')

@admin_bp.route('/proses_training', methods=['POST'])
@login_required
def proses_training():
    hasil = train_naive_bayes()

    if hasil['status'] == 'error':
        flash(hasil['msg'], 'danger')
    else:
        flash(f"Model berhasil dilatih dengan akurasi {hasil['akurasi']}%", 'success')
        return render_template('admin/training_model.html', hasil=hasil)

    return redirect(url_for('admin.training_model'))


@admin_bp.route('/simulasi', methods=['GET', 'POST'])
@login_required
def simulasi():
    hasil_prediksi = None
    teks_input = ''

    if request.method == 'POST':
        teks_input = request.form.get('teks_input')

        print(teks_input)

        if teks_input:
            hasil_prediksi = predict_single(teks_input)
            print(hasil_prediksi)

    return render_template('admin/simulasi.html',
                           hasil=hasil_prediksi,
                           teks_input=teks_input)
