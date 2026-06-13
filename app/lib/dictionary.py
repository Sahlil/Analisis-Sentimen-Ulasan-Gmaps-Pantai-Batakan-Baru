import csv
import os
import re

import pandas as pd
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

NORMALISASI = {
    # Kata ganti dan umum
    "sy": "saya", "aq": "saya", "aku": "saya", "gw": "saya", "gue": "saya",
    "ulun": "saya", "uln": "saya",
    "skrg": "sekarang", "skrng": "sekarang", "skarang": "sekarang",
    "bgt": "banget", "bngt": "banget", "bangeet": "banget", "bangettt": "banget",
    "bgd": "banget", "banged": "banget",
    "gk": "tidak", "ga": "tidak", "gak": "tidak", "tdk": "tidak",
    "nggak": "tidak", "ngga": "tidak", "kagak": "tidak", "enggak": "tidak",
    "jg": "juga", "jga": "juga", "jua": "juga",
    "yg": "yang", "yng": "yang",
    "org": "orang", "orng": "orang",
    "dgn": "dengan", "dngn": "dengan", "dg": "dengan",
    "dpt": "dapat", "dpet": "dapat",
    "tp": "tapi", "tpi": "tapi",
    "trs": "terus", "trus": "terus",
    "udh": "sudah", "udah": "sudah", "sdh": "sudah", "dah": "sudah",
    "blm": "belum", "blum": "belum",
    "sm": "sama", "sma": "sama",
    "kmu": "kamu", "lu": "kamu",
    "klo": "kalau", "kl": "kalau", "kalo": "kalau",
    "pian": "anda",
    "deh": "saja", "aja": "saja",
    "nih": "ini",
    "nye": "nya",

    # Singkatan umum
    "ad": "ada",
    "rekom": "rekomendasi", "rekomend": "rekomendasi",
    "bgs": "bagus", "baguzz": "bagus", "bagusss": "bagus",
    "krn": "karena", "karna": "karena", "krna": "karena",
    "utk": "untuk", "untk": "untuk",
    "mantul": "mantap", "mantapp": "mantap", "mantappp": "mantap",  # FIX: mantul bukan "mantap betul"
    "sgt": "sangat", "sngt": "sangat",
    "bner": "benar", "bener": "benar", "banar": "benar",
    "bgtu": "begitu", "gitu": "begitu",
    "brp": "berapa", "brpa": "berapa",
    "cm": "hanya", "cmn": "hanya", "cuman": "hanya", "cuma": "hanya",
    "dll": "dan lain",   # FIX: "dan lain-lain" → 3 token, pakai "dan lain" saja
    "dlm": "dalam",
    "dr": "dari",
    "dl": "dulu",
    "dsni": "di sini",
    "gmn": "bagaimana", "gimana": "bagaimana",
    "hrs": "harus", "hrus": "harus",
    "jd": "jadi",
    "kcil": "kecil", "kecill": "kecil",
    "kyk": "seperti", "kayak": "seperti",
    "lbh": "lebih",
    "lg": "lagi",
    "mksd": "maksud", "mksud": "maksud",
    "msh": "masih", "msih": "masih",
    "murahh": "murah",
    "pdhl": "padahal",
    "plg": "paling",
    "prlu": "perlu",
    "rmh": "rumah", "rumahh": "rumah",
    "sblm": "sebelum",
    "sdikit": "sedikit", "sdkit": "sedikit",
    "sgala": "segala",
    "smpai": "sampai",
    "smua": "semua",
    "sneng": "senang", "seneng": "senang", "himung": "senang",
    "t4": "tempat",
    "td": "tadi",
    "trima": "terima",
    "yaa": "ya", "yaaa": "ya",
    "bwanyak": "banyak", "bnyak": "banyak", "bnyk": "banyak",
    "bkn": "bukan",

    # Kata khusus
    "pengen": "ingin", "pengin": "ingin",     # FIX: pingin → ingin (lebih baku)
    "mo": "mau",
    "tu": "itu",
    "deket": "dekat",
    "kereen": "keren", "kerenn": "keren", "kerennn": "keren",
    "kece": "keren", "kecee": "keren",
    "pengunjungg": "pengunjung",
    "pantainya": "pantai", "pantaii": "pantai",
    "sunsetnya": "sunset",
    "wahanaa": "wahana", "wahananya": "wahana",
    "penginapannya": "penginapan", "penginapann": "penginapan",
    "ok": "oke",
    "thanks": "terima kasih", "thx": "terima kasih",
    "plis": "tolong", "please": "tolong",
    "sorry": "maaf", "sori": "maaf",
    "gas": "ayo",
    "srek": "cocok",
    "rami": "ramai",
    "best": "baik",
    "seru": "asik", "asikk": "asik",
    "puass": "puas",
    "ramahh": "ramah",
    "jelekk": "jelek",
    "mahall": "mahal",
    "kotorr": "kotor",
    "bersihh": "bersih",
    "dijaminn": "dijamin",
    "pemandangann": "pemandangan",
    "fasilitass": "fasilitas",
    "kebersihann": "kebersihan",
    "kenyamanann": "kenyamanan",
    "jauuuhhhhh": "jauh",
    "joss": "bagus", "jos": "bagus",
    "gemes": "gemas", "gemess": "gemas",
    "geratis": "gratis", "gratiss": "gratis",
    "parahh": "parah", "parahhh": "parah",
    "pphon": "pohon",
    "karcisnyaa": "karcis", "karcisnya": "karcis", "karcisss": "karcis",
    "duaa": "dua",
    "rb": "ribu",
    "nyediakan": "sedia",
    "gejebo": "gazebo",
    "najiss": "najis",

    # TAMBAHAN BARU — dari analisis dataset
    "no": "tidak",          # "no problem" → tidak problem (hati-hati, bisa ambigu)
    "emng": "memang", "emang": "memang",
    "agak": "agak",
    "loh": "lho",
    "iyaa": "iya",
    "gimanaa": "bagaimana",
    "kesini": "ke sini",
    "disini": "di sini",
    "disana": "di sana",
    "kyknya": "sepertinya", "kykny": "sepertinya",
    "sjk": "sejak",
    "byk": "banyak",
    "jgn": "jangan",
    "sdkt": "sedikit",
    "krg": "kurang",
    "tgk": "tengok",
    "blg": "bilang",
    "wkwk": "tertawa", "wkwkwk": "tertawa", "haha": "tertawa", "hehe": "tertawa",
    "worth": "sepadan",
    "crowded": "ramai",
    "jorok": "kotor",
    "rigat": "kotor",
    "bising": "berisik",
    "coklat": "keruh",      
    "nyari": "cari",
    "nyewa": "sewa",
    "nyaman": "nyaman",
    "pemda": "pemerintah",
    "bjm": "banjarmasin",  
    "kada": "tidak",
    "kd": "tidak",
    "kedada": "tidak ada",
    "kdd": "tidak ada",
    "larang": "mahal",
    "bungas": "bagus", 
    "langkar": "cantik",
    "banyu": "air",
    "hanyar": "baru",
    "lawas": "lama",
    "kelotok": "perahu",
    "klotok": "perahu",
    "kuda": "kuda",
    "pacah": "pecah",
    "handak": "mau",
    "parak": "dekat",
}

# ══════════════════════════════════════════════════════════════════════════════
# LEXICON — kata bersentimen beserta bobotnya
# Aturan pemberian bobot:
#   +2 / -2 : sentimen kuat, kata spesifik
#   +1 / -1 : sentimen lemah, kata umum/kontekstual
#   Dihapus : kata ambigu, nama tempat, kata netral domain wisata
# ══════════════════════════════════════════════════════════════════════════════
CUSTOM_DOMAIN_LEXICON = {
    # ── Positif kuat ──────────────────────────────────────────────────────────
    "bagus": 2, "indah": 2, "bersih": 2, "rekomendasi": 2, "mantap": 2,
    "fotoable": 2, "keren": 2, "puas": 2, "asik": 2,
    "jernih": 2, "cantik": 2, "memukau": 2, "sepadan": 2,

    # ── Positif standar ───────────────────────────────────────────────────────
    "nyaman": 1, "ramah": 1, "menarik": 1, "luas": 1, "murah": 1,
    "tenang": 1, "aman": 1, "enak": 1, "baik": 1, "senang": 1,
    "terjangkau": 1, "cocok": 1, "nikmat": 1, "sunset": 1, 
    "gratis": 1, "rindang": 1, "segar": 1, "asri": 1, "tertawa": 1,

    # ── Negasi positif ────────────────────────────────────────────────────────
    "tidak_mahal": 2, "tidak_kotor": 2, "tidak_buruk": 2,
    "tidak_jelek": 2, "tidak_parah": 2,
    "tidak_bising": 1, "tidak_ramai": 1, "tidak_berserakan": 2,

    # ── Negatif fatal ─────────────────────────────────────────────────────────
    "sampah": -4, "pungli": -5, "kumuh": -3, "bau": -3, "jorok": -3, 
    "berlumpur": -2, "gatal": -2,

    # ── Negatif kuat ──────────────────────────────────────────────────────────
    "kotor": -2, "ribut": -2, "berisik": -2, "parah": -2,
    "jelek": -2, "kecewa": -3, "buruk": -2, "keruh": -2, 
    "najis": -3, "rusak": -2, "hambur": -2, "bising": -2, 
    "kacau": -2, "macet": -2, "sera": -2,

    # ── Negatif standar ───────────────────────────────────────────────────────
    "kurang": -1, "sulit": -1, "panas": -1, "terganggu": -1,
    "mahal": -2, "sayang": -1, "kok": -1, "tagih": -1, "bayar": -1, "bingung": -1,

    # ── Negasi negatif ────────────────────────────────────────────────────────
    "tidak_bagus": -2, "tidak_rekomendasi": -2, "tidak_bersih": -2,
    "tidak_mantap": -2, "tidak_ada": -1, "tidak_bisa": -1,
    "kurang_nyaman": -1, "kurang_bagus": -1, "kurang_bersih": -2, 
    "kurang_puas": -2, "kurang_tata": -1,
}

def _normalize_lexicon_word(word):
    if word is None:
        return ""
    text = str(word).lower().strip()
    if not text:
        return ""
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    normalized_tokens = []
    for token in text.split():
        # NORMALISASI harus sudah didefinisikan di atas kode ini
        token = NORMALISASI.get(token, token)
        if token:
            normalized_tokens.append(token)
    return "_".join(normalized_tokens)

def _load_lexicon_from_tsv(file_name, target_lexicon):
    file_path = os.path.join(BASE_DIR, file_name)
    if not os.path.exists(file_path):
        print(f"File {file_name} tidak ditemukan di {file_path}")
        return target_lexicon

    with open(file_path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            word = _normalize_lexicon_word(row.get("word"))
            if not word:
                continue
            raw_weight = row.get("weight", "")
            try:
                weight = int(float(raw_weight))
            except (TypeError, ValueError):
                continue
            
            # Khusus untuk InSet, bobot dijumlahkan jika ada duplikat dalam file TSV
            target_lexicon[word] = target_lexicon.get(word, 0) + weight

    return target_lexicon

# =====================================================================
# 2. IMPLEMENTASI HYBRID LEXICON
# =====================================================================

# A. Inisialisasi dictionary utama
LEXICON = {}

# B. Muat Baseline (InSet Lexicon)
_load_lexicon_from_tsv("positive.tsv", LEXICON)
_load_lexicon_from_tsv("negative.tsv", LEXICON)
print(f"Memuat {len(LEXICON)} kata dasar dari InSet Lexicon.")

# C. Terapkan Domain-Specific Adaptation (Menimpa dengan kamus pantai)
kata_ditimpa = 0
kata_baru = 0

for custom_word, custom_weight in CUSTOM_DOMAIN_LEXICON.items():
    # Normalisasi agar formatnya pasti cocok
    normalized_word = _normalize_lexicon_word(custom_word)
    if not normalized_word:
        continue
    
    if normalized_word in LEXICON:
        kata_ditimpa += 1
    else:
        kata_baru += 1
        
    # OVERRIDE: Gunakan '=' bukan '+=' agar skor InSet diganti total
    # Contoh: 'bagus' di InSet -4, akan diganti menjadi 2 sesuai kamusmu
    LEXICON[normalized_word] = custom_weight

print(f"Hyrbid Lexicon Sukses: {kata_ditimpa} skor kata InSet dikoreksi, {kata_baru} kata spesifik ditambahkan.")
print(f"Total kata di Lexicon siap pakai: {len(LEXICON)}")

# =====================================================================

# Ekstraksi untuk sistem pencocokan frasa di preprocessing
LEXICON_COMPONENT_TOKENS = {
    part
    for key in LEXICON
    for part in key.split("_")
    if part
}

LEXICON_PATTERN_LENGTHS = sorted(
    {len(key.split("_")) for key in LEXICON},
    reverse=True
)

# ══════════════════════════════════════════════════════════════════════════════
# STOPWORD TAMBAHAN — domain-specific
# ══════════════════════════════════════════════════════════════════════════════
STOPWORD_TAMBAHAN = {
    # Partikel/filler
    "nya", "y", "sih", "dong", "tuh", "deh", "lho", "loh", "iya",

    # Stem salah dari nama tempat (JANGAN masukkan ke lexicon)
    "bata",     # ← batakan (nama tempat, bukan kata bata/batu bata)
    "unjung",   # ← pengunjung (stem salah, tidak bersentimen)
    "sera",     # ← berserakan (HAPUS dari sini karena sudah masuk LEXICON di atas)

    # Kata domain wisata yang netral (muncul di semua kelas)
    "pantai",   # ← muncul 649x di semua kelas, tidak membedakan sentimen
    "wisata",   # ← netral
    "libur",    # ← netral
    "keluarga", # ← netral
    "inap",     # ← netral (penginapan)
    "sewa",     # ← netral
    "tenda",    # ← netral
    "wahana",   # ← netral (atv, banana boat, kuda)
    "parkir",   # ← netral
    "area",     # ← netral
    "fasilitas",# ← netral (kecuali ada konteks)
    "mandi",    # ← netral
    "masuk",    # ← netral (biaya masuk = konteks, bukan kata "masuk" sendiri)
    "boat",     # ← netral (banana boat = wahana)
    "kuda",     # ← netral (wahana kuda)
    "camping",  # ← netral
    "sunset",   # ← CATATAN: dihapus dari stopword karena sudah masuk LEXICON (+1)
    "orang",    # ← netral
    "jalan",    # ← netral
    "waktu",    # ← netral
    "tempat",   # ← netral
    "air",      # ← HATI-HATI: "air kotor/keruh" sudah ditangani lewat kata kotor/keruh
    "tertawa",  # ← wkwk/haha = ekspresi, sudah masuk lexicon +1, jangan distopword
}

# ── HAPUS "sera" dari STOPWORD karena sudah di LEXICON ──────────────────────
STOPWORD_TAMBAHAN.discard("sera")
STOPWORD_TAMBAHAN.discard("tertawa")

# ══════════════════════════════════════════════════════════════════════════════
# KATA NEGASI — kata yang memicu penggabungan token
# ══════════════════════════════════════════════════════════════════════════════
KATA_NEGASI = {"tidak", "bukan", "jangan", "kurang", "belum"}

# ══════════════════════════════════════════════════════════════════════════════
# PROTECTED WORDS — kata yang TIDAK boleh di-stem oleh Sastrawi
# Gunakan ini di preprocessing untuk skip stemming pada kata-kata ini
# ══════════════════════════════════════════════════════════════════════════════
PROTECTED_WORDS = {
    # Nama tempat
    "batakan", "banjarmasin", "kalimantan", "tanah", "laut",
    # Kata asing yang tidak perlu di-stem
    "atv", "banana", "boat", "camping", "glamping", "villa",
    "gazebo", "sunset", "sunrise", "selfie",
    # Kata yang hasilnya benar tanpa di-stem
    "pantai", "pasir", "ombak", "angin",
}
