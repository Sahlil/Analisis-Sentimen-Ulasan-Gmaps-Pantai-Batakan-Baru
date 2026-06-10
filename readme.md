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

# Penjelasan Singkat Library Python (Requirements)

Dokumen ini berisi rangkuman dan penjelasan singkat mengenai fungsi dari setiap library yang terdapat dalam daftar dependencies Anda. Proyek ini terindikasi sebagai aplikasi web berbasis **Flask** yang mengintegrasikan fitur **Machine Learning (ML)** dan **Natural Language Processing (NLP)** berbahasa Indonesia.

---

## 🌐 Web Framework & Server (Flask Ecosystem)

| Library | Versi | Deskripsi Singkat |
| :--- | :--- | :--- |
| **Flask** | `3.1.2` | *Micro-framework* utama untuk membangun arsitektur aplikasi web atau RESTful API. |
| **Flask-Login** | `0.6.3` | Ekstensi Flask untuk mengelola sesi pengguna, autentikasi (login/logout), dan proteksi rute halaman. |
| **Werkzeug** | `3.1.5` | Pustaka utilitas WSGI standar di balik Flask yang menangani rute (*routing*), request, dan response HTTP. |
| **Jinja2** | `3.1.6` | *Template engine* cepat dan aman untuk merender halaman HTML dinamis dari sisi server. |
| **MarkupSafe** | `3.0.3` | Berpasangan dengan Jinja2 untuk melakukan *escaping* karakter HTML berbahaya guna mencegah serangan XSS. |
| **itsdangerous** | `2.2.0` | Menyediakan fungsi kriptografi ringan untuk menandai data secara aman (misal: token aktivasi atau session cookie). |
| **blinker** | `1.9.0` | Sistem *event signaling* berbasis objek untuk mengirim pesan/sinyal antar komponen di Flask. |

---

## 🗄️ Database & ORM

| Library | Versi | Deskripsi Singkat |
| :--- | :--- | :--- |
| **SQLAlchemy** | `2.0.45` | Toolkit SQL dan *Object-Relational Mapping* (ORM) industri untuk memetakan objek Python ke tabel database. |
| **Flask-SQLAlchemy**| `3.1.1` | Ekstensi pembungkus (*wrapper*) agar integrasi SQLAlchemy ke dalam ekosistem Flask menjadi lebih mudah. |
| **PyMySQL** | `1.1.2` | Driver murni Python (*pure-Python MySQL client*) untuk menghubungkan aplikasi ke server database MySQL/MariaDB. |

---

## 🧠 Machine Learning & Data Science

| Library | Versi | Deskripsi Singkat |
| :--- | :--- | :--- |
| **pandas** | `2.3.3` | Library fundamental untuk manipulasi, analisis, pembersihan, dan strukturisasi data berbentuk tabel (*DataFrame*). |
| **numpy** | `2.4.1` | Komputasi saintifik berbasis array multidimensi dan operasi matriks dengan performa tinggi. |
| **scikit-learn** | `1.8.0` | Library utama untuk *Machine Learning* klasik (algoritma klasifikasi, regresi, clustering, dan preprocessing data). |
| **imbalanced-learn**| `0.14.1`| Alat bantu untuk menangani masalah ketidakseimbangan kelas (*imbalanced datasets*) dengan teknik ressampling (SMOTE, dll). |
| **scipy** | `1.17.0` | Library matematika, sains, dan rekayasa tingkat lanjut yang menjadi basis algoritma komputasi scikit-learn. |
| **joblib** | `1.5.3` | Digunakan untuk eksekusi tugas secara paralel serta menyimpan (*serialize*) dan memuat (*deserialize*) model ML ke dalam file. |
| **sklearn-compat** | `0.1.5` | Utilitas pembantu untuk menjaga kompatibilitas API antar versi modul scikit-learn yang berbeda. |
| **threadpoolctl** | `3.6.0` | Mengontrol jumlah antrean thread (konkurensi) pada pustaka matematika tingkat tinggi seperti BLAS atau LAPACK. |

---

## 💬 Natural Language Processing (NLP) & Pemrosesan Teks

| Library | Versi | Deskripsi Singkat |
| :--- | :--- | :--- |
| **nltk** | `3.9.4` | *Natural Language Toolkit*, perpustakaan legendaris untuk tokenisasi, parsing, stemming, dan analisis teks bahasa alami. |
| **Sastrawi** | `1.0.1` | Library khusus NLP untuk melakukan *stemming* (pencarian kata dasar) pada teks yang berbahasa Indonesia. |
| **regex** | `2026.4.4`| Modul Regular Expression alternatif yang lebih bertenaga dan memiliki fitur lebih kaya dibanding modul bawaan Python `re`. |

---

## 🛠️ Utilitas, Format File & Manajemen Sistem

| Library | Versi | Deskripsi Singkat |
| :--- | :--- | :--- |
| **click** | `8.3.1` | Toolkit untuk membuat antarmuka baris perintah (*Command Line Interface* / CLI) secara deklaratif. |
| **colorama** | `0.4.6` | Memberikan pewarnaan teks ANSI pada terminal agar tampilan log atau output CLI lebih interaktif. |
| **openpyxl** | `3.1.5` | Membaca dan menulis file spreadsheet berformat Microsoft Excel (`.xlsx`). |
| **et_xmlfile** | `2.0.0` | Dependensi tingkat rendah untuk pemrosesan XML (diperlukan secara internal oleh `openpyxl`). |
| **python-dateutil**| `2.9.0.post0`| Ekstensi kuat untuk memanipulasi objek datetime (parsing string tanggal, kalkulasi selisih waktu, dll). |
| **python-dotenv** | `1.2.2` | Membaca konfigurasi atau kredensial rahasia (seperti DB_PASSWORD) dari file `.env` ke variabel lingkungan aplikasi. |
| **pytz** | `2025.2` | Pengelolaan zona waktu dunia (*Tz database*) agar perhitungan waktu bersifat *timezone-aware*. |
| **tzdata** | `2025.3` | Penyedia data mentah zona waktu terbaru untuk digunakan oleh ekosistem Python. |
| **tqdm** | `4.67.3` | Membuat indikator proses (*progress bar*) yang interaktif dan dinamis di terminal/konsol. |
| **greenlet** | `3.3.0` | Menyediakan komponen konkurensi berbasis *micro-threads* ringan untuk eksekusi tugas secara asinkron. |
| **typing_extensions**| `4.15.0`| Menyediakan fitur pembatasan tipe (*type hinting*) terbaru untuk versi Python lama yang belum mendukungnya secara native. |
| **six** | `1.17.0` | Library utilitas kompatibilitas untuk menjembatani perbedaan sintaksis antara Python 2 dan Python 3 (legacy library). |