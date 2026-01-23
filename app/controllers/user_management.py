from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.lib.decorators import super_admin_required # Import satpam tadi

user_bp = Blueprint('user_mgmt', __name__, url_prefix='/users')

# 1. READ - Tampilkan Semua User
@user_bp.route('/')
@login_required
@super_admin_required # <--- Pasang Satpam Disini
def index():
    users = User.query.all()
    return render_template('admin/users/index.html', users=users)

# 2. CREATE - Tambah User Baru
@user_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@super_admin_required
def tambah():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # Cek username kembar
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan!', 'danger')
        else:
            new_user = User(username=username, role=role)
            new_user.set_password(password) # Enkripsi password
            db.session.add(new_user)
            db.session.commit()
            flash('User berhasil ditambahkan!', 'success')
            return redirect(url_for('user_mgmt.index'))

    return render_template('admin/users/tambah.html')

# 3. UPDATE - Edit User
@user_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@super_admin_required
def edit(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form.get('username')
        user.role = request.form.get('role')
        
        # Cek jika password diisi (jika kosong, jangan ubah password)
        password_baru = request.form.get('password')
        if password_baru:
            user.set_password(password_baru)
            
        db.session.commit()
        flash('Data user berhasil diperbarui!', 'success')
        return redirect(url_for('user_mgmt.index'))

    return render_template('admin/users/edit.html', user=user)

# 4. DELETE - Hapus User
@user_bp.route('/hapus/<int:id>')
@login_required
@super_admin_required
def hapus(id):
    # Cegah menghapus diri sendiri
    if id == current_user.id:
        flash('Anda tidak bisa menghapus akun sendiri saat sedang login!', 'warning')
        return redirect(url_for('user_mgmt.index'))

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User berhasil dihapus.', 'success')
    return redirect(url_for('user_mgmt.index'))