# seeder.py
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Cek apakah sudah ada user admin
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123') # Passwordnya: admin123
        db.session.add(admin)
        db.session.commit()
        print("User 'admin' berhasil dibuat! Password: admin123")
    else:
        print("User 'admin' sudah ada.")