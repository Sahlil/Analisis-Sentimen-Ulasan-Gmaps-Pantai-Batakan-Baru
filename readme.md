# Projek Sistem TA - Analisis Sentimen Ulasan

Aplikasi web berbasis Flask untuk mengelola ulasan, melakukan preprocessing bahasa Indonesia, melatih model klasifikasi sentimen (Naive Bayes + TF-IDF), dan menampilkan hasil evaluasi. Aplikasi ini juga menyediakan demo prediksi sentimen untuk pengunjung dan panel admin untuk pengelolaan data serta pengguna.

## Tujuan

- Membantu proses klasifikasi sentimen ulasan (positif, netral, negatif).
- Menyediakan alur end-to-end: impor data, preprocessing, pelatihan model, hingga evaluasi.
- Menyajikan dashboard dan riwayat training untuk pemantauan performa model.

## Fitur Utama

- Autentikasi login dan manajemen pengguna (admin dan super admin).
- Impor data ulasan dari CSV atau Excel.
- Preprocessing bahasa Indonesia (normalisasi, negasi, stemming, stopword, lexicon).
- Training model Naive Bayes dengan TF-IDF dan SMOTE.
- Riwayat training dan confusion matrix.
- Demo prediksi sentimen untuk pengguna umum.

## Persiapan Sebelum Menjalankan

1. **Python 3.9+**
2. **MySQL Server**
   - Pastikan database tersedia sesuai konfigurasi di [config.py](config.py).
   - Default: `mysql+pymysql://root:@localhost/ta_db`
3. **File .env**
   - Salin dari [\.env.example](.env.example) menjadi `.env` lalu sesuaikan nilainya.
4. **Virtual environment** (disarankan)
5. **Dependensi Python**
   - flask
   - flask_sqlalchemy
   - flask_login
   - pymysql
   - pandas
   - numpy
   - scikit-learn
   - imbalanced-learn
   - sastrawi
   - nltk
   - openpyxl (untuk baca file Excel)
   - python-dotenv

## Cara Menjalankan

1. Buat dan aktifkan virtual environment.
2. Salin file env contoh:
   ```bash
   copy .env.example .env
   ```
3. Install dependensi:
   ```bash
   pip install flask flask_sqlalchemy flask_login pymysql pandas numpy scikit-learn imbalanced-learn sastrawi nltk openpyxl python-dotenv
   ```
4. Buat database MySQL sesuai konfigurasi (contoh: `ta_db`).
5. Jalankan seeder untuk membuat akun awal:
   ```bash
   python seeder.py
   ```
6. Jalankan aplikasi:
   ```bash
   python run.py
   ```
7. Buka aplikasi di browser: `http://127.0.0.1:5000`

## Akun Default

- Admin:
  - username: `admin`
  - password: `admin123`
- Super Admin:
  - username: `super`
  - password: `super123`

## Catatan

- File model akan disimpan di folder [model_storage](model_storage).
- NLTK stopwords akan diunduh otomatis saat pertama kali preprocessing dijalankan.
- Sesuaikan konfigurasi database dan secret key di `.env` untuk lingkungan produksi.
