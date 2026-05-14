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
    tipe_data = db.Column(db.String(20), nullable=True)
    tanggal_input = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Ulasan {self.id}>'

class RiwayatTraining(db.Model):
    __tablename__ = 'riwayat_training'

    id = db.Column(db.Integer, primary_key=True)
    tanggal_training = db.Column(db.DateTime, default=datetime.utcnow)
    jumlah_data = db.Column(db.Integer, nullable=False)
    rasio_split = db.Column(db.String(10), nullable=False)
    akurasi = db.Column(db.Float, nullable=False)
    presisi = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    f1_score = db.Column(db.Float, nullable=False)

    # Sel Confusion Matrix 3x3
    # Baris Aktual Negatif
    neg_neg = db.Column(db.Integer, default=0)
    neg_neu = db.Column(db.Integer, default=0)
    neg_pos = db.Column(db.Integer, default=0)

    # Baris Aktual Netral
    neu_neg = db.Column(db.Integer, default=0)
    neu_neu = db.Column(db.Integer, default=0)
    neu_pos = db.Column(db.Integer, default=0)

    # Baris Aktual Positif
    pos_neg = db.Column(db.Integer, default=0)
    pos_neu = db.Column(db.Integer, default=0)
    pos_pos = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<RiwayatTraining {self.id} - Acc: {self.akurasi}%>'

    def to_dict(self):
        """Mudah untuk dikonversi ke JSON jika ingin ditampilkan di Dashboard"""
        return {
            'id': self.id,
            'tanggal': self.tanggal_training.strftime('%Y-%m-%d %H:%M:%S'),
            'rasio': self.rasio_split,
            'akurasi': self.akurasi,
            'presisi': self.presisi,
            'recall': self.recall,
            'f1': self.f1_score,
            'matrix': {
                'negatif': [self.neg_neg, self.neg_neu, self.neg_pos],
                'netral': [self.neu_neg, self.neu_neu, self.neu_pos],
                'positif': [self.pos_neg, self.pos_neu, self.pos_pos]   
            }
        }