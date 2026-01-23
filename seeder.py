# seeder.py
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # 1. Cek Admin Biasa
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print("✅ User 'admin' dibuat.")

    # 2. BUAT SUPER ADMIN
    if not User.query.filter_by(username='super').first():
        super_adm = User(username='super', role='super_admin') # Role harus persis
        super_adm.set_password('super123') # Passwordnya: super123
        db.session.add(super_adm)
        db.session.commit()
        print("✅ User 'super' (Super Admin) berhasil dibuat!")
    else:
        print("ℹ️ User 'super' sudah ada.")