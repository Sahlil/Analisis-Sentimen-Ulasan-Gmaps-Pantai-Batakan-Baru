from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Ulasan(db.Model):
    __tablename__ = 'ulasan'
    
    id = db.Column(db.Integer, primary_key=True)
    teks_asli = db.Column(db.Text, nullable=False)
    teks_clean = db.Column(db.Text, nullable=True)
    label = db.Column(db.String(20), nullable=True)
    prediksi = db.Column(db.String(20), nullable=True)
    tanggal_input = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Ulasan {self.id}>'