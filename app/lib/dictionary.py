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
    "tigat": "kotor",
    "bising": "berisik",
    "coklat": "keruh",      # "air coklat" di konteks pantai = air keruh
    "nyari": "cari",
    "nyewa": "sewa",
    "nyaman": "nyaman",
    "pemda": "pemerintah",
    "bjm": "banjarmasin",   # singkatan kota, netral
}

# ══════════════════════════════════════════════════════════════════════════════
# LEXICON — kata bersentimen beserta bobotnya
# Aturan pemberian bobot:
#   +2 / -2 : sentimen kuat, kata spesifik
#   +1 / -1 : sentimen lemah, kata umum/kontekstual
#   Dihapus : kata ambigu, nama tempat, kata netral domain wisata
# ══════════════════════════════════════════════════════════════════════════════
LEXICON = {
    # ── Positif kuat ──────────────────────────────────────────────────────────
    "bagus": 2, "indah": 2, "bersih": 2, "rekomendasi": 2, "mantap": 2,
    "fotoable": 2, "keren": 2, "puas": 2, "asik": 2,
    "jernih": 2,        # air jernih = positif kuat untuk wisata pantai
    "cantik": 2,
    "memukau": 2,
    "sepadan": 2,       # worth it

    # ── Positif standar ───────────────────────────────────────────────────────
    "nyaman": 1, "ramah": 1, "menarik": 1, "luas": 1, "murah": 1,
    "tenang": 1, "aman": 1, "enak": 1, "baik": 1, "senang": 1,
    "terjangkau": 1, "cocok": 1,
    "nikmat": 1,        # TAMBAH: "menikmati" → "nikmat", sering di ulasan positif
    "sunset": 1,        # TAMBAH: sunset sering disebut sebagai daya tarik positif
    "gratis": 1,        # TAMBAH: gratis = nilai plus
    "rindang": 1,       # TAMBAH: pohon rindang = nyaman
    "segar": 1,         # TAMBAH: udara segar = positif
    "asri": 1,          # TAMBAH: suasana asri = positif
    "tertawa": 1,       # wkwk/hehe setelah normalisasi = ekspresi senang

    # ── Negasi positif ────────────────────────────────────────────────────────
    "tidak_mahal": 2, "tidak_kotor": 2, "tidak_buruk": 2,
    "tidak_jelek": 2, "tidak_parah": 2,
    "tidak_bising": 1, "tidak_ramai": 1, "tidak_berserakan": 2,

    # ── Negatif fatal ─────────────────────────────────────────────────────────
    "sampah": -4, "pungli": -5,
    "kumuh": -3,        # naik dari -2
    "bau": -3,          # naik dari -2
    "jorok": -3,        # TAMBAH: jorok = sangat kotor
    "berlumpur": -2, "gatal": -2,

    # ── Negatif kuat ──────────────────────────────────────────────────────────
    "kotor": -2, "ribut": -2, "berisik": -2, "parah": -2,
    "jelek": -2, "kecewa": -3, "buruk": -2,
    "keruh": -2,        # air keruh = negatif untuk wisata pantai
    "najis": -3,
    "rusak": -2,
    "hambur": -2,       # berhamburan (sampah)
    "bising": -2,       # TAMBAH: bising = gangguan
    "kacau": -2,        # TAMBAH: kacau = kondisi buruk
    "macet": -2,        # TAMBAH (naik dari -1 ke -2): macet = gangguan serius
    "sera": -2,         # berserakan → stem "sera", sering muncul di ulasan negatif

    # ── Negatif standar ───────────────────────────────────────────────────────
    "kurang": -1, "sulit": -1, "panas": -1, "terganggu": -1,
    "mahal": -2, "sayang": -1,  # "sayang" dalam arti "disayangkan"
    "kok": -1, "tagih": -1, "bayar": -1, "bingung": -1,

    # ── Negasi negatif ────────────────────────────────────────────────────────
    "tidak_bagus": -2, "tidak_rekomendasi": -2, "tidak_bersih": -2,
    "tidak_mantap": -2, "tidak_ada": -1, "tidak_bisa": -1,
    "kurang_nyaman": -1, "kurang_bagus": -1,
    "kurang_bersih": -2, "kurang_puas": -2, "kurang_tata": -1,

    # ── DIHAPUS dari kamus lama (alasan) ─────────────────────────────────────
    # "seru"       → diganti asik, seru sudah dinormalisasi ke asik
    # "foto"       → netral, semua wisata ada foto
    # "spot"       → netral, kata umum
    # "hammock"    → netral, fasilitas biasa
    # "weekday"    → netral, bukan sentimen
    # "tolong"     → ambigu, bisa muncul di kalimat positif
    # "dua"        → sangat ambigu, "dua kali datang" ≠ negatif
    # "tindak"     → terlalu spesifik, jarang muncul
    # "crowded"    → sudah dinormalisasi ke "ramai" yang netral
    # "double"     → ambigu
    # "duplikat"   → jarang muncul
    # "karokean"   → terlalu spesifik
    # "aneh"       → ambigu
    # "perbaiki"   → ambigu (bisa positif "sudah diperbaiki")
    # "benahi"     → ambigu
    # "banget"     → penguat, bukan sentimen sendiri
}

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
