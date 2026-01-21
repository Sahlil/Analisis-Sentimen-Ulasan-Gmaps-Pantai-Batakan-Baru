import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Ulasan
from app.lib.preprocessing import preprocess_text, label_sentiment

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


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
    


@admin_bp.route('/proses_preprocessing')
@login_required
def proses_preprocessing():
    data_mentah = Ulasan.query.filter(Ulasan.teks_clean == None).all()

    if not data_mentah:
        flash('Tidak ada data ulasan mentah yang perlu diproses.', 'info')
        return redirect(url_for('admin.data_ulasan'))

    jumlah = 0
    for item in data_mentah:
        tokens = preprocess_text(item.teks_asli)

        clean_text = ' '.join(tokens)

        label = label_sentiment(tokens)

        item.teks_clean = clean_text
        item.label = label
        jumlah += 1

    db.session.commit()
    flash(f'Berhasil memproses {jumlah} ulasan.', 'success')
    return redirect(url_for('admin.data_ulasan'))

