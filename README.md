# ✍️ IDMedia Community — Platform Penulis Profesional

<p align="center">
  <img src="assets/idmedia_logo_3d.jpg" width="160" alt="IDMedia 3D Logo" style="border-radius: 24px; box-shadow: 0 8px 30px rgba(0,0,0,0.3);" />
</p>

<p align="center">
  <b>Platform Penulisan, Kurasi Redaksi, dan Monetisasi Artikel Digital Berstandar Media Nasional</b><br>
  <i>Diadaptasi dari Masterbook 12 Halaman & 20 Modul Panduan Resmi IDN Times Community</i>
</p>

<p align="center">
  <a href="https://idmedia-indonesia.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App" /></a>
  <img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/Tests-16%20Passed-success?logo=pytest" alt="Test Status" />
  <img src="https://img.shields.io/badge/Design-Material%203%20%2F%20Glassmorphism-purple" alt="Material 3" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

---

<p align="center">
  <img src="assets/idmedia_hero_banner.jpg" width="100%" alt="IDMedia Digital Newsroom 3D Banner" style="border-radius: 14px;" />
</p>

---

## 🌟 Tautan Resmi Aplikasi
- **Aplikasi Live (Streamlit Cloud):** 👉 [https://idmedia-indonesia.streamlit.app/](https://idmedia-indonesia.streamlit.app/)
- **Landing Page (GitHub Pages):** 👉 [https://indri007.github.io/idmedia/](https://indri007.github.io/idmedia/)
- **Repositori Source Code:** [https://github.com/indri007/idmedia](https://github.com/indri007/idmedia)

---

## 🚀 Fitur Utama

### 1. 📰 Beranda Publik (Editorial Feed)
* Menampilkan artikel komunitas yang telah lolos moderasi redaksi (`status: Diterbitkan`).
* Navigasi kategori interaktif: *Life, Tech, Career, Relationship, Science & Tech, Food, Travel, Hiburan*.
* Tampilan kartu artikel lengkap dengan foto sampul rasio 3:2, nama penulis, tanggal, waktu baca, ringkasan *hook*, dan daftar rujukan cek fakta.

### 2. ✍️ Smart Listicle Editor (Standar Zero Reject)
* **Validator Judul EYD V Real-time**: Memeriksa huruf kapital pada awal kata dan memastikan huruf kecil untuk 25 partikel kata sambung (*di, ke, dari, untuk, agar, yang, atau, dan, dll.*), mendukung angka awal listicle (e.g. *5 Tips Sukses*).
* **Inspirasi Kata Penyedap**: Generator diksi klik-ramah (*Kerap, Bikin, Bakal, Wajib Tahu, Diam-diam, Konon, dll.*).
* **Cuplikan (Excerpt)**: 1 kalimat *hook* inti pesan untuk caption media sosial.
* **Cek Fakta Rujukan**: Input minimal 2 URL sumber rujukan kredibel asli di awal draf.
* **SOP Gambar Resmi**: Validasi format caption frasa ilustrasi (huruf kecil tanpa titik) atau kalimat berita peristiwa (huruf kapital dengan titik).
* **Indikator Kuantitatif**: Penghitung kata real-time (target min. 500 kata) dan kuota subjudul (min. 3 untuk deskriptif / min. 7 untuk galeri foto).
* **Templat Baku Otomatis**: Generator struktur listicle instan (*Pembuka ➜ Subjudul ➜ Gambar ➜ Narasi min. 3 kalimat ➜ Penutup*).

### 3. 📊 Dashboard Penulis
* Pelacakan status artikel: *Menunggu Ditinjau, Perlu Perbaikan, Diterbitkan, Ditolak*.
* Akses catatan revisi dari tim editor.
* Formulir *Edit & Submit Ulang* langsung dari dasbor jika artikel berstatus *Perlu Perbaikan*.

### 4. ⚖️ Panel Moderasi Editor
* Meja redaksi untuk meninjau draf yang masuk secara langsung tanpa hambatan.
* Aksi editorial cepat:
  * ✅ **Terbitkan (Tayang)**: Menampilkan artikel ke halaman utama publik.
  * 🔧 **Minta Revisi**: Mengembalikan naskah dengan instruksi perbaikan spesifik.
  * ❌ **Tolak Naskah**: Memberikan alasan penolakan redaksional.

### 5. 📖 10 Pedoman Emas & 📚 Ensiklopedia 20 Panduan IDN Times
* Basis pengetahuan interaktif hasil *reverse engineering* 20 panduan kurasi resmi IDN Times Community.
* **Kalkulator Finansial Penulis**: Simulasi konversi *Views ➜ IDN Points ➜ Rupiah* (1 Poin / 100 views, threshold pencairan 2.500 poin).
* Penjelasan jenjang karir penulis: *Community Member* ➜ *Community Writer* ➜ *Verified Writer*.

---

## 🛠️ Menjalankan di Komputer Lokal

```bash
# 1. Kloning repositori
git clone https://github.com/indri007/idmedia.git
cd idmedia

# 2. Buat lingkungan virtual Python
python3 -m venv .venv
source .venv/bin/activate  # Untuk Windows: .venv\Scripts\activate

# 3. Pasang paket dependensi
pip install -r requirements.txt

# 4. Salin file environment (opsional untuk override secret)
cp .env.example .env

# 5. Jalankan uji unit (16 tests passed)
python -m pytest -q tests/

# 6. Jalankan aplikasi Streamlit
streamlit run app.py
```

---

## 🤖 QA Automation Suite (`idn-media-qa-automation`)

Suite pengujian automasi Robot Framework untuk ekosistem IDN Media:

```bash
cd idn-media-qa-automation

# 1. Pasang dependensi QA
pip install -r requirements.txt

# 2. Siapkan file environment kredensial pengujian
cp .env.example .env
# Isi IDN_TEST_EMAIL dan IDN_TEST_PASSWORD dengan akun test resmi

# 3. Eksekusi pengujian Robot Framework
robot -d results idntimes/artikel/artikel.robot
```

> [!IMPORTANT]
> **Batasan Editorial:** Aksi `Save as draft` pada Robot Framework hanya memverifikasi penyimpanan draf di akun penulis. Di sistem produksi `community.idntimes.com`, publikasi ke indeks publik memerlukan proses kurasi editorial dan tidak dapat diterbitkan secara otomatis tanpa persetujuan redaksi IDN Media.

---

## 📁 Struktur Proyek

```text
idmedia/
├── assets/
│   ├── idmedia_logo_3d.jpg        # Logo 3D Material Design 3
│   └── idmedia_hero_banner.jpg    # Banner 3D Newsroom & Journalism 4.0
├── data/
│   └── articles.json              # Fallback basis data artikel JSON
├── src/
│   ├── idn_knowledge_base.py      # Mesin 20 panduan kurasi & kalkulator poin
│   ├── document_parser.py         # Ekstraktor teks & dokumen
│   ├── quality_rules.py           # Mesin audit naskah
│   ├── visual_quality.py          # Mesin evaluasi kualitas gambar
│   └── reporting.py               # Generator laporan Word & PDF
├── tests/
│   ├── test_articles.py           # Uji unit konten & validasi artikel
│   └── test_database_auth.py      # Uji unit SQLite, auth hashing & role
├── idn-media-qa-automation/       # Robot Framework QA suite
├── .env.example                   # Template konfigurasi environment aman
├── app.py                         # Aplikasi utama IDMedia Community
├── database.py                    # SQLite database persistent storage
├── auth.py                        # Secure PBKDF2 authentication module
├── index.html                     # Landing page GitHub Pages
├── requirements.txt               # Daftar paket dependensi Python
└── README.md                      # Dokumentasi resmi repositori
```

---

## 📜 Lisensi & Etika
Aplikasi ini dikembangkan untuk tujuan edukasi dan peningkatan mutu kepenulisan digital berstandar jurnalistik nasional. Seluruh karya naskah wajib orisinal, menjunjung tinggi kode etik jurnalistik media siber, dan bebas dari praktik plagiarisme.
