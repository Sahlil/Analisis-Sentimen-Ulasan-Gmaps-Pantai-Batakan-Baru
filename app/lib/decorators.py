from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'super_admin':
            flash('⛔ Akses Ditolak! Halaman ini khusus Super Admin.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function