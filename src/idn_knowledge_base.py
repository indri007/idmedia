"""
IDMedia Knowledge Base & Rule Engine
Disarikan (reverse-engineered) dari 20 panduan editorial resmi IDN Times Community.
"""

KATA_PENYEDAP_JUDUL = [
    "Kerap", "Bikin", "Bakal", "Wajib Tahu", "Diam-diam", "Konon",
    "Jitu", "Antimainstream", "Gak Disangka", "Rentan", "Malah Bikin",
    "Auto", "Diam-diam", "Ternyata", "Ampuh", "Bikin Melongo"
]

TEKNIK_PENUTUP = {
    "Kesimpulan Solutif": "Merangkum benang merah solusi dari poin-poin yang telah dibahas tanpa bertele-tele.",
    "Punchline Menggugah": "Kalimat penutup yang memantik emosi, inspirasi, atau sudut pandang baru yang berkesan.",
    "Pertanyaan Interaktif": "Mengajak audiens berdiskusi langsung di kolom komentar (contoh: 'Dari kelima tips di atas, mana yang paling relate sama kamu?').",
    "Rekomendasi Tindakan (Call-to-Action)": "Mendorong pembaca mencoba langkah konkret mulai hari ini.",
    "Refleksi Diri": "Mengajak pembaca merenungkan kembali kebiasaan sehari-hari secara bijak."
}

HIERARKI_PENULIS = {
    "Community Member": {
        "deskripsi": "Akun baru terdaftar. Dapat menulis draf dan mengirimkan artikel ke meja redaksi.",
        "syarat": "Registrasi akun dengan email aktif.",
        "benefit": "Akses editor teks dan pengumpulan poin organik."
    },
    "Community Writer": {
        "deskripsi": "Penulis aktif yang telah memiliki minimal 1 artikel terbit resmi.",
        "syarat": "Minimal 1 artikel lolos kurasi editor.",
        "benefit": "Profil publik penulis, statistik views artikel, dan pencairan poin."
    },
    "Verified Writer": {
        "deskripsi": "Penulis berprestasi dengan reputasi penerbitan konsisten dan minim revisi (Zero Reject).",
        "syarat": "Konsistensi rilis artikel bulanan, rasio lolos kurasi tinggi, dan terverifikasi identitas KTP.",
        "benefit": "Badge biru Verified Writer, prioritas review editor, bonus event eksklusif, dan penugasan khusus."
    }
}

SKEMA_POIN_MONETISASI = {
    "rasio_views": "1 Poin per 100 Views Organik",
    "konversi_rupiah": "1 Poin = Rp100 (Atau sesuai ketentuan promo bulanan)",
    "ambang_pencairan": "Minimal 2.500 Poin (Setara Rp250.000)",
    "metode_redeem": ["Transfer Rekening Bank", "GoPay", "OVO", "DANA"]
}

PANDUAN_20_MODUL = [
    {
        "id": 1,
        "judul": "10 Step-by-step Nulis Artikel di IDN Times Community",
        "kategori": "Alur Kerja",
        "inti": "Alur 10 langkah: Tentukan angle ➔ Riset 2 sumber kredibel ➔ Susun judul EYD V ➔ Tulis excerpt hook ➔ Format listicle (H2 ➔ Foto ➜ Narasi) ➔ Cek typo ➔ Submit ke antrean editor."
    },
    {
        "id": 2,
        "judul": "Ketentuan Gambar Artikel di IDN Times Community",
        "kategori": "Visual & SOP",
        "inti": "Rasio 3:2 landscape, resolusi min 800x350, max 1 MB, objek manusia hidup, tanpa watermark, dan caption sesuai format (frasa kecil tanpa titik / kalimat kapital bertitik)."
    },
    {
        "id": 3,
        "judul": "5 Tips Jitu Membuat Judul Artikel yang Mengundang Banyak Pembaca",
        "kategori": "Judul & CTR",
        "inti": "Gunakan angka listicle di awal, masukkan kata kunci utama, hindari clickbait palsu, jaga panjang judul 4-12 kata, dan patuhi huruf kapital EYD V."
    },
    {
        "id": 4,
        "judul": "5 Tips Membuat 'Kata Penyedap' Buat Judul Artikel Biar Antimainstream",
        "kategori": "Judul & CTR",
        "inti": "Sisipkan kata-kata pemantik emosi seperti 'Kerap', 'Bikin', 'Diam-diam', 'Auto', dan 'Malah' agar judul lebih segar dan tidak kaku ala skripsi."
    },
    {
        "id": 5,
        "judul": "5 Teknik Menutup Cerita biar Paragraf Penutup Gak Itu-Itu Aja",
        "kategori": "Struktur Teks",
        "inti": "Variasikan penutup dengan 5 gaya: Kesimpulan padat, punchline filosofis, pertanyaan interaktif, ajakan aksi, atau refleksi pribadi."
    },
    {
        "id": 6,
        "judul": "Artikel Listicle Vs Narasi, Ini Lho Perbedaannya!",
        "kategori": "Format Tulisan",
        "inti": "Listicle menggunakan poin bernomor (H2) dengan kuota subjudul min. 3 (deskriptif) atau min. 7 (koleksi foto). Narasi mengalir runut untuk opini, esai, atau fiksi."
    },
    {
        "id": 7,
        "judul": "Artikelmu Sering Ditolak oleh Editor IDN Times? Lakukan 5 Hal Ini",
        "kategori": "Troubleshooting",
        "inti": "Cek 5 faktor penolakan: kata kurang dari 500, salah penulisan sumber gambar, sumber rujukan dari media kompetitor/wiki, duplikasi topik, atau salah kapitalisasi judul."
    },
    {
        "id": 8,
        "judul": "5 Mindset yang Harus Ditanamkan Saat Artikelmu Masuk Revisi Editor",
        "kategori": "Mindset Penulis",
        "inti": "Revisi bukan penolakan, melainkan tanda artikelmu potensial. Baca catatan editor dengan teliti, perbaiki segera, dan submit ulang tanpa berkecil hati."
    },
    {
        "id": 9,
        "judul": "Apa Bedanya Member, Writer, dan Verified Writer?",
        "kategori": "Karir Penulis",
        "inti": "Tingkatan penulis menentukan kredibilitas, kecepatan proses review oleh editor, dan akses ke program bonus kuota penulisan bulanan."
    },
    {
        "id": 10,
        "judul": "Cara Redeem IDN Points yang Praktis untuk Community Writers",
        "kategori": "Monetisasi",
        "inti": "Kumpulkan poin dari akumulasi views organik dan event menulis. Tarik saldo langsung ke rekening atau e-wallet setelah mencapai batas minimum."
    },
    {
        "id": 11,
        "judul": "Jangan Bingung! Ini Cara Tulis Puisi di IDN Times Community",
        "kategori": "Kategori Khusus",
        "inti": "Puisi minimal 3 bait dengan diksi puitis mendalam, tipografi rapi, foto ilustrasi yang selaras dengan tema, dan bebas unsur provokatif."
    },
    {
        "id": 12,
        "judul": "Tips Nulis IDN Times Community: Dos and Don'ts Nulis Artikel Throwback",
        "kategori": "Kategori Khusus",
        "inti": "Artikel nostalgia wajib mengulas fakta unik di balik peristiwa/karya lama, bukan sekadar rangkuman sinopsis yang sudah diketahui umum."
    },
    {
        "id": 13,
        "judul": "Wajib Tahu, Nih 5 Tips Nulis Artikel Bollywood Viral",
        "kategori": "Hype & Entertainment",
        "inti": "Eksplorasi kehidupan artis, fakta di balik layar film box office, sudut pandang inspiratif, dan wajib gunakan foto resmi berkualitas tinggi."
    },
    {
        "id": 14,
        "judul": "5 Sikap yang Harus Dihindari Saat Baru Mulai Menulis Artikel",
        "kategori": "Etika & Kebiasaan",
        "inti": "Hindari: Langsung menyerah saat revisi, malas riset rujukan asli, copy-paste tanpa izin, mengabaikan EYD, dan spam submit naskah yang sama."
    },
    {
        "id": 15,
        "judul": "Kumpulan Jawaban Editor IDN Times Community di #TanyaEditor",
        "kategori": "Q&A Redaksi",
        "inti": "Editor mengutamakan orisinalitas, sudut pandang personal (angle unik), kelengkapan gambar, dan kebersihan naskah dari salah ketik (typo)."
    },
    {
        "id": 16,
        "judul": "Mengenal Badge and Reward IDN Times Community",
        "kategori": "Gamifikasi",
        "inti": "Raih lencana pencapaian berdasarkan produktivitas artikel, akumulasi views tertinggi, dan konsistensi kategori tulisan."
    },
    {
        "id": 17,
        "judul": "11 Hal yang Perlu Kamu Tahu Soal Mimin Media Sosial IDN Times",
        "kategori": "Distribusi Konten",
        "inti": "Artikel yang dibagikan ke Instagram/Facebook IDN Times dipilih berdasarkan kekuatan judul, excerpt yang memikat, dan topik yang sedang trending."
    },
    {
        "id": 18,
        "judul": "10 Jawaban Editor Atas Segala Pertanyaanmu tentang IDN Community",
        "kategori": "Q&A Redaksi",
        "inti": "Panduan verifikasi akun, jadwal review artikel (1-14 hari kerja), tips tembus artikel pilihan editor, dan proteksi hak cipta karya."
    },
    {
        "id": 19,
        "judul": "Mengenal Fitur Menulis di IDN Times Community",
        "kategori": "Tooling",
        "inti": "Manfaatkan fitur tambah section, pratinjau mobile, penyematan gambar, dan penyimpanan draf otomatis agar proses penulisan nyaman."
    },
    {
        "id": 20,
        "judul": "Tips & Trik Nulis Artikel Seputar Piala Dunia / Olahraga Ala IDN Times",
        "kategori": "Sports",
        "inti": "Kombinasikan statistik pertandingan, profil inspiratif atlet, drama di luar lapangan, dan cantumkan sumber rujukan dari federasi resmi."
    }
]

def hitung_estimasi_poin(views: int):
    poin = views // 100
    rupiah = poin * 100
    return poin, rupiah
