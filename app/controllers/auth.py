from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.lib.machine_learning import predict_single

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return render_template('landing.html')

@auth_bp.route('/demo', methods=['GET', 'POST'])
def demo():
    if current_user.is_authenticated:
        return redirect(url_for('admin.simulasi'))

    hasil = None
    pesan = None
    teks_input = ''

    if request.method == 'POST':
        teks_input = request.form.get('teks_input', '').strip()
        if teks_input:
            prediksi = predict_single(teks_input)
            prediksi_lower = prediksi.lower() if isinstance(prediksi, str) else ''
            if prediksi_lower in ['positif', 'negatif', 'netral']:
                hasil = prediksi_lower
            else:
                pesan = prediksi
        else:
            pesan = 'Silakan isi kalimat ulasan terlebih dahulu.'

    return render_template('landing_demo.html', hasil=hasil, pesan=pesan, teks_input=teks_input)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Username atau password salah.')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))