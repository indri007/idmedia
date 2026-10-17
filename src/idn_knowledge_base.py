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

MASTERBOOK_12_MODUL = [
    {
        "halaman": 1,
        "modul": "Pengantar & Visi Kurasi 100%",
        "ringkasan": "Buku panduan komprehensif 12 halaman: Monetisasi, Kurasi 100%, Strategi AI, & Teknik Jurnalisme Modern.",
        "detail": "Dirancang khusus membimbing penulis pemula hingga profesional agar menguasai standar redaksi media siber nasional IDN Times Community.",
        "poin_kunci": [
            "Penyelarasan standar redaksi IDN Times pusat",
            "Membangun portofolio kepenulisan kredibel",
            "Skema monetisasi transparan dan legalitas hak cipta"
        ]
    },
    {
        "halaman": 2,
        "modul": "Modul 1: Skema Finansial & Konversi Poin",
        "ringkasan": "Memahami bagaimana angka pembaca (views) dikonversi menjadi rupiah melalui sistem poin platform.",
        "detail": "1 Poin setiap 100 Views Organik. Poin tambahan diperoleh dari bonus event bulanan. Pencairan (Redeem) dapat ditarik ke rekening bank atau e-wallet (GoPay, OVO, DANA) setelah mencapai batas minimum 2.500 Poin (Rp250.000).",
        "poin_kunci": [
            "Rasio: 1 Poin per 100 Views Organik",
            "Nilai: 1 Poin = Rp100",
            "Target: Rp500.000+ dari views rutin & partisipasi event bulanan",
            "Redeem fleksibel via Bank & E-Wallet"
        ]
    },
    {
        "halaman": 3,
        "modul": "Modul 2: Tahapan Onboarding & Pengaturan Akun",
        "ringkasan": "Langkah awal krusial untuk memastikan identitas dan profil Anda terverifikasi dengan benar oleh sistem.",
        "detail": "Registrasi via community.idntimes.com dengan akun valid. Pengisian nama lengkap profil wajib sesuai nama KTP agar pencairan dana tidak terkendala anti-fraud. Sinkronisasi nomor rekening bank atau e-wallet terverifikasi atas nama pribadi.",
        "poin_kunci": [
            "Registrasi via Google/Facebook aktif",
            "Nama profil wajib identik dengan KTP",
            "Rekening bank & e-wallet wajib atas nama sendiri",
            "Keamanan akun: Jangan pernah membagikan sandi atau OTP"
        ]
    },
    {
        "halaman": 4,
        "modul": "Modul 3: Standar Teknis & Kuantitatif Artikel",
        "ringkasan": "Redaksi media nasional menetapkan ambang batas ukuran artikel yang ketat guna menjaga kualitas pembacaan.",
        "detail": "Minimal 500 kata untuk semua jenis tulisan. Minimal 3 subjudul (H2) untuk artikel deskriptif dan 7 subjudul untuk listicle kompilasi foto. Setiap subjudul wajib memiliki minimal 2 paragraf dengan masing-masing paragraf berisi minimal 3 kalimat.",
        "poin_kunci": [
            "Panjang Naskah: Minimal 500 kata",
            "Subjudul (H2): Min. 3 (deskriptif) atau Min. 7 (listicle galeri)",
            "Kepadatan Paragraf: Min. 2 paragraf per subjudul",
            "Panjang Kalimat: Min. 3 kalimat per paragraf"
        ]
    },
    {
        "halaman": 5,
        "modul": "Modul 4: Kaidah EYD V & Penulisan Judul Berita",
        "ringkasan": "Judul adalah pintu gerbang pertama pembaca. Kesalahan penulisan kapitalisasi huruf sering menjadi alasan utama revisi.",
        "detail": "Setiap awal kata pada judul wajib menggunakan huruf kapital, kecuali kata tugas (dan, atau, di, ke, dari, untuk, dengan, pada, dalam) di tengah. Gunakan angka di awal (5 Fakta Unik...) untuk mendongkrak CTR. Hindari bahasa kaku skripsi.",
        "poin_kunci": [
            "Kapitalisasi EYD V: Huruf besar tiap kata kecuali partikel di tengah",
            "Angka numerik di awal judul listicle untuk menaikkan CTR",
            "Gaya santai, padat, dan elegan khas anak muda",
            "Contoh benar: '5 Tips Mengatur Keuangan untuk Gen Z agar Cepat Mandiri'"
        ]
    },
    {
        "halaman": 6,
        "modul": "Modul 5: Prompt AI Parafrase Lolos Plagiasi",
        "ringkasan": "Pemanfaatan kecerdasan buatan (AI) harus dilakukan secara etis untuk merombak sumber berita luar negeri.",
        "detail": "Gunakan formula prompt redaksi resmi: 'Bertindaklah sebagai Senior Editor IDN Times. Parafrase ulang teks acuan di bawah ini dengan gaya bahasa jurnalistik dinamis dan santai khas media anak muda. 1. Rombak struktur kalimat aktif. 2. Terapkan KBBI dan EYD V. 3. Pertahankan fakta asli dengan angle segar. 4. Jangan gunakan frasa repetitif robot.'",
        "poin_kunci": [
            "Formula prompt resmi Senior Editor IDN Times",
            "Tingkat keaslian (originality) terjaga di atas 90%",
            "Bebas deteksi AI & mesin anti-plagiasi",
            "Fakta terjaga dengan sudut pandang unik"
        ]
    },
    {
        "halaman": 7,
        "modul": "Modul 6: Etika Penggunaan Gambar & Hak Cipta",
        "ringkasan": "Kesalahan visual dapat berakibat fatal bagi legalitas publikasi media siber.",
        "detail": "Rasio gambar sampul wajib 3:2 landscape, resolusi jernih dengan ukuran file ringan (< 1 MB). Letakkan gambar tepat di bawah subjudul (H2) sebelum narasi. Wajib mencantumkan atribusi sumber cetak miring (Pixabay/John Doe atau Dokumentasi Pribadi). Dilarang keras screenshot tanpa izin.",
        "poin_kunci": [
            "Rasio landscape 3:2 (min. 800x350 px)",
            "Ukuran file kompresi ringan maksimal 1 MB",
            "Penempatan tepat di bawah subjudul H2",
            "Atribusi sumber jelas, tanpa watermark, bebas pelanggaran hak cipta"
        ]
    },
    {
        "halaman": 8,
        "modul": "Modul 7: Pemilihan Topik Trending & Riset Keyword",
        "ringkasan": "Artikel dengan views tinggi berasal dari topik yang sedang dicari banyak pembaca saat ini.",
        "detail": "Pantau Google Trends Indonesia harian. Fokus pada niche populer (Relationship, Career, Tech, Travel, Kuliner, Entertainment). Temukan sudut pandang unik (angle) dan letakkan kata kunci utama di paruh awal judul artikel untuk optimasi SEO.",
        "poin_kunci": [
            "Riset Google Trends Indonesia secara berkala",
            "Kategori favorit: Relationship, Career, Tech, Lifestyle, Pop Culture",
            "Diferensiasi sudut pandang (unique angle)",
            "Peletakan keyword utama di paruh depan judul (SEO-friendly)"
        ]
    },
    {
        "halaman": 9,
        "modul": "Modul 9: Psikologi Pembaca & Teknik Hook Paragraf",
        "ringkasan": "Membujuk pembaca agar tidak menutup halaman dalam 5 detik pertama kunjungan.",
        "detail": "Gunakan paragraf pembuka (lead) berupa pertanyaan retoris, fakta mengejutkan, atau skenario relatable. Batasi maksimal 3-4 kalimat per paragraf agar nyaman dibaca di layar smartphone. Pecah data kompleks dengan bullet points agar mudah dipindai.",
        "poin_kunci": [
            "Lead memikat dalam 5 detik pertama",
            "Paragraf pendek (maks. 3-4 kalimat per paragraf mobile-friendly)",
            "Hindari wall of text (blok teks menjemukan)",
            "Format scannable dengan penomoran jelas"
        ]
    },
    {
        "halaman": 10,
        "modul": "Modul 10: Troubleshooting Penolakan & Revisi Editor",
        "ringkasan": "Jika artikel Anda dikembalikan atau ditolak oleh editor, jangan berkecil hati. Lakukan solusi cepat.",
        "detail": "Kurang dari 500 kata: Tambahkan analisis mendalam pada poin terakhir. Terindikasi plagiasi: Rombak struktur kalimat pasif menjadi aktif secara mandiri. Kesalahan EYD: Periksa tanda koma sebelum konjungsi dan kapitalisasi kata tugas.",
        "poin_kunci": [
            "Solusi kata kurang: Tambah elaborasi studi kasus di poin penutup",
            "Solusi plagiasi: Parafrase aktif kalimat per kalimat",
            "Solusi EYD: Cek partikel depan dan tanda baca baku",
            "Respons revisi dalam kurun waktu cepat di dashboard penulis"
        ]
    },
    {
        "halaman": 11,
        "modul": "Modul 11: Etika Jurnalistik Media Siber Nasional",
        "ringkasan": "Sebagai penulis di platform media terkemuka, menjunjung tinggi kode etik adalah harga mati.",
        "detail": "Wajib anti-hoaks dengan verifikasi minimal 2 sumber kredibel. Dilarang keras memuat konten SARA, ujaran kebencian, atau pencemaran nama baik. Sampaikan opini pribadi secara santun, objektif, dan tidak menggurui audiens.",
        "poin_kunci": [
            "Verifikasi ketat minimal 2 sumber referensi kredibel",
            "Netralitas mutlak: Nol toleransi terhadap SARA & ujaran kebencian",
            "Opini objektif tanpa nada menggurui",
            "Menjunjung tinggi Pedoman Pemberitaan Media Siber (PPMS)"
        ]
    },
    {
        "halaman": 12,
        "modul": "Modul 12: Menuju Verified Writer & Penutup",
        "ringkasan": "Pencapaian tertinggi seorang kontributor di IDN Times Community adalah mendapatkan lencana Verified Writer.",
        "detail": "Bangun konsistensi penerbitan rutin mingguan. Pertahankan rekam jejak Zero Reject Rate dengan mematuhi seluruh 12 modul panduan. Aktif di komunitas resmi penulis untuk mendapatkan penugasan khusus dan event berhadiah menarik.",
        "poin_kunci": [
            "Konsistensi rilis berkala membangun trust editor",
            "Zero Reject Rate dengan checklist audit mandiri",
            "Lencana biru Verified Writer & hak prioritas kurasi",
            "Menulis adalah investasi konsistensi dan reputasi jangka panjang"
        ]
    }
]

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
        "inti": "Kumpulkan minimal 2.500 Poin (Rp250.000) dari views (1 poin/100 views) dan event bulanan. Tarik via Transfer Bank atau E-Wallet (GoPay, OVO, DANA). Pastikan nama akun sesuai rekening KTP. Pencairan diproses 7-14 hari kerja."
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

def format_idn_times_payload(art: dict) -> str:
    """Format draf artikel agar siap di-copy paste langsung ke dashboard IDN Times Community."""
    rujukan_txt = ""
    if art.get("rujukan_urls"):
        rujukan_txt = "Sumber rujukan:\n" + "\n".join(art["rujukan_urls"]) + "\n\n"

    caption = art.get("caption_gambar") or art.get("sumber_gambar") or "ilustrasi artikel (pexels.com)"
    cover_info = (
        f"URL Gambar: {art.get('gambar', '-')}\n"
        f"Caption & Sumber: {caption}\n"
        f"Tautan Asli: {art.get('url_sumber', '-')}\n"
        f"Deskripsi Foto: {art.get('deskripsi_gambar', '-')}\n"
    )

    full_payload = (
        f"==========================================================\n"
        f"DRAF SIAP TERBIT — IDN TIMES COMMUNITY FORMAT\n"
        f"==========================================================\n\n"
        f"JUDUL ARTIKEL (EYD V):\n{art.get('judul', '')}\n\n"
        f"CUPLIKAN / EXCERPT:\n{art.get('cuplikan', '')}\n\n"
        f"KATEGORI:\n{art.get('kategori', 'Life')}\n\n"
        f"GAMBAR SAMPUL (COVER):\n{cover_info}\n"
        f"----------------------------------------------------------\n"
        f"NASKAH LENGKAP LISTICLE:\n\n"
        f"{rujukan_txt}"
        f"{art.get('isi', '')}\n\n"
        f"----------------------------------------------------------\n"
        f"Status Kurasi Internal: {art.get('status', 'Diterbitkan')}\n"
        f"IDMedia UID: {art.get('id', '')}\n"
    )
    return full_payload

TRENDING_GAP_ARTICLES = [
    {
        "id": "trend-1",
        "tema": "Health & Lifestyle",
        "judul": "5 Bahaya Revenge Bedtime Procrastination yang Bikin Tubuh Selalu Lelah Setiap Pagi",
        "cuplikan": "Sering begadang sengaja cuma demi scrolling medsos? Waspadai 5 dampak fatal balas dendam waktu tidur ini bagi kesehatan fisik dan mentalmu!",
        "kategori": "Life",
        "gambar": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?q=80&w=1200&auto=format&fit=crop",
        "caption_gambar": "ilustrasi orang begadang menatap layar ponsel di tempat tidur (unsplash.com/kate_sullivan)",
        "sumber_gambar": "ilustrasi orang begadang menatap layar ponsel di tempat tidur (unsplash.com/kate_sullivan)",
        "url_sumber": "https://unsplash.com/photos/woman-holding-smartphone-in-dark-room",
        "deskripsi_gambar": "bahaya begadang revenge bedtime procrastination kesehatan",
        "rujukan_urls": [
            "https://www.sleepfoundation.org/sleep-hygiene/revenge-bedtime-procrastination",
            "https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/sleep/art-20048379"
        ],
        "isi": """Pernahkah kamu merasa waktu siang hari terlalu padat oleh tuntutan pekerjaan atau perkuliahan, sehingga kamu sengaja mengorbankan waktu tidur malam hanya demi menonton video atau berselancar di media sosial? Fenomena psikologis ini dikenal secara luas di dunia medis sebagai *revenge bedtime procrastination*. 

Meskipun aktivitas santai larut malam terasa memuaskan pada awalnya, kebiasaan menunda tidur secara sengaja ini menyimpan segudang dampak buruk yang mengintai kesehatanmu. Berikut lima bahaya fatal yang mengancam jika kamu terus membiarkan kebiasaan balas dendam waktu tidur ini berlarut-larut.

## 1. Penurunan Fungsi Kognitif dan Ketajaman Memori Otak
Ketika kamu memangkas durasi tidur malam, otak tidak memiliki kesempatan yang cukup untuk membersihkan racun metabolik dan mengonsolidasikan ingatan jangka panjang. Akibatnya, kamu akan merasa linglung, sulit berkonsentrasi saat diajak berbicara, dan kerap melupakan detail-detail pekerjaan penting keesokan harinya.

Penelitian menunjukkan bahwa defisit tidur kronis membuat reaksi otak melambat hingga setara dengan kondisi orang yang berada di bawah pengaruh alkohol. Mengabaikan waktu istirahat malam demi hiburan sekejap jelas merupakan pertukaran yang sangat merugikan produktivitasmu.

## 2. Gangguan Keseimbangan Hormon dan Pemicu Nafsu Makan Berlebih
Kurang tidur secara langsung mengacaukan regulasi dua hormon utama pengendali nafsu makan di dalam tubuh, yakni ghrelin dan leptin. Hormon ghrelin yang merangsang rasa lapar akan melonjak drastis, sedangkan hormon leptin yang memberi sinyal kenyang justru mengalami penurunan tajam.

Kondisi ketidakseimbangan hormonal ini menjelaskan mengapa orang yang hobi begadang cenderung tergiur untuk mengonsumsi makanan cepat saji atau camilan manis berkalori tinggi pada dini hari. Dalam jangka panjang, kebiasaan ini meningkatkan risiko obesitas dan diabetes tipe 2 secara signifikan.

## 3. Penurunan Drastis Kinerja Sistem Kekebalan Tubuh
Selama fase tidur lelap, sistem imun tubuh memproduksi dan melepaskan sitokin, yaitu sejenis protein pelindung yang bertugas melawan peradangan dan infeksi virus. Ketika waktu tidur malammu dipangkas, produksi antibodi pelindung ini akan menurun secara drastis.

Akibat melemahnya benteng pertahanan alami ini, tubuhmu menjadi jauh lebih rentan tertular penyakit flu, batuk, dan membutuhkan waktu pemulihan yang jauh lebih lama ketika jatuh sakit. Menjaga tidur cukup adalah vaksin alami paling murah yang dimiliki manusia.

## 4. Lonjakan Hormon Stres Kortisol yang Memicu Kecemasan Kronis
Tidur malam yang tidak memadai memicu kelenjar adrenal untuk memproduksi hormon stres kortisol secara berlebihan sebagai kompensasi rasa lelah. Lonjakan kortisol yang berkepanjangan ini membuat detak jantung berdebar lebih cepat dan menciptakan ketegangan emosional yang konstan.

Secara psikologis, individu yang mengalami defisit tidur kronis menjadi jauh lebih sensitif, mudah tersinggung oleh masalah sepele, dan rentan mengalami serangan kecemasan (*anxiety*). Memperbaiki siklus tidur adalah fondasi awal paling efektif untuk menenangkan pikiran yang kalut.

## 5. Peningkatan Risiko Penyakit Jantung dan Tekanan Darah Tinggi
Pada saat tidur normal, tekanan darah manusia secara alami akan mengalami fase penurunan (*nocturnal dipping*) untuk memberikan jeda istirahat bagi pembuluh darah dan otot jantung. Kebiasaan begadang menghalangi terjadinya proses istirahat alami ini.

Tekanan darah yang terus-menerus tinggi sepanjang malam memicu pengerasan dinding arteri dan memperberat beban kerja pompa jantung secara terus-menerus. Jika kebiasaan ini dibiarkan selama bertahun-tahun, risiko serangan jantung koroner dan strok akan meningkat berlipat ganda.

Menghargai waktu istirahat malam bukanlah bentuk kemalasan, melainkan investasi paling berharga untuk menjaga keberlangsungan hidup dan kesehatan masa depanmu. Dari kelima dampak buruk di atas, mana sinyal bahaya yang paling sering kamu rasakan saat bangun pagi?""",
        "penulis": "Indri Kartika",
        "tanggal": "17 Okt 2026",
        "status": "Diterbitkan",
        "views": 420
    },
    {
        "id": "trend-2",
        "tema": "Career & Finansial",
        "judul": "5 Strategi Menerapkan Loud Budgeting untuk Gen Z agar Gak Terjebak FOMO Finansial",
        "cuplikan": "Gak perlu gengsi menolak ajakan nongkrong mahal. Terapkan 5 langkah cerdas loud budgeting agar kondisi keuanganmu tetap stabil!",
        "kategori": "Career",
        "gambar": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=1200&auto=format&fit=crop",
        "caption_gambar": "ilustrasi seseorang menghitung anggaran keuangan bulanan (pexels.com/Karolina Grabowska)",
        "sumber_gambar": "ilustrasi seseorang menghitung anggaran keuangan bulanan (pexels.com/Karolina Grabowska)",
        "url_sumber": "https://www.pexels.com/photo/person-calculating-finances-4386431/",
        "deskripsi_gambar": "tips mengelola uang strategi loud budgeting gen z",
        "rujukan_urls": [
            "https://www.forbes.com/advisor/banking/what-is-loud-budgeting/",
            "https://hbr.org/2023/11/how-to-manage-financial-anxiety"
        ],
        "isi": """Tekanan sosial di era digital sering kali memaksa generasi muda untuk memaksakan gaya hidup di luar batas kemampuan finansial demi menghindari rasa takut tertinggal (*fear of missing out* atau FOMO). Namun, belakangan ini muncul gerakan finansial baru yang sangat positif bernama *loud budgeting*.

Berbeda dengan pola hidup hemat yang dijalani diam-diam dengan rasa malu, *loud budgeting* justru mendorong kamu untuk bersikap transparan dan vokal mengenai prioritas keuangan pribadimu kepada teman sebaya. Berikut lima strategi efektif menerapkan *loud budgeting* agar tabunganmu aman tanpa merusak pertemanan.

## 1. Mengubah Pola Kalimat Penolakan Tanpa Emosi Defensif
Kunci utama dari keberhasilan *loud budgeting* terletak pada seni komunikasi yang percaya diri tanpa terkesan mengeluh atau merasa rendah diri. Daripada mengatakan kalimat sedih seperti 'aku gak punya uang', gantilah dengan pernyataan tegas seperti 'itu di luar alokasi bujetku bulan ini'.

Pergeseran diksi ini menegaskan bahwa keputusanmu didasarkan pada kendali diri yang matang, bukan karena ketidakberdayaan ekonomi. Teman-teman yang dewasa pasti akan menghargai ketegasan prinsipmu dalam mengelola penghasilan.

## 2. Mengajukan Alternatif Agenda Nongkrong yang Lebih Ramah Kantong
Menolak ajakan makan di restoran mewah bukan berarti kamu harus memutus tali silaturahmi atau mengurung diri dari pergaulan sosial. Jadilah inisiator yang menawarkan alternatif kegiatan lain yang menyenangkan namun tetap hemat biaya.

Kamu bisa mengusulkan sesi piknik santai di taman kota, memasak bersama di rumah (*potluck*), atau sekadar ngopi di kedai lokal yang terjangkau. Kebersamaan yang berkualitas ditentukan oleh kedalaman obrolan, bukan oleh mahalnya tagihan struk makanan.

## 3. Menetapkan Rencana Finansial Jangka Pendek yang Transparan
Jelaskan kepada lingkaran terdekatmu mengenai tujuan keuangan besar yang sedang kamu perjuangkan dengan penuh antusiasme. Ketika teman-temanmu mengetahui bahwa kamu sedang menabung untuk dana darurat, modal bisnis, atau persiapan studi lanjut, mereka akan lebih berempati.

Keterbukaan ini secara tidak sadar mengubah posisi mereka dari pemicu godaan konsumtif menjadi suporter yang ikut mengawal pencapaian impianmu. Lingkungan sosial yang suportif akan terbentuk dari keberanianmu membuka percakapan yang jujur.

## 4. Menghapus Godaan Aplikasi Belanja dari Notifikasi Ponsel
Gaya hidup impulsif sering kali dipicu oleh rentetan pemberitahuan diskon kilat (*flash sale*) dan promosi yang membanjiri layar ponselmu setiap hari. Ambil langkah tegas dengan menonaktifkan seluruh notifikasi aplikasi e-commerce dan pesan promosi perbankan.

Terapkan aturan jeda 48 jam sebelum memutuskan untuk membeli barang-barang non-kebutuhan pokok yang kamu inginkan. Waktu jeda ini memberi ruang bagi logika berpikir rasional untuk menilai apakah barang tersebut benar-benar bernilai guna atau sekadar nafsu sesaat.

## 5. Mengapresiasi Diri Sendiri Berdasarkan Pencapaian Tabungan
Secara tradisi, masyarakat sering mengukur kesuksesan dari barang-barang bermerek yang dipamerkan di linimasa media sosial. Mulai sekarang, ubahlah tolok ukur kebanggaan pribadimu dari apa yang kamu belanjakan menjadi seberapa kokoh dana darurat yang berhasil kamu amankan.

Ketenangan batin karena memiliki kebebasan finansial dan bebas dari jeratan utang konsumtif jauh lebih berharga daripada validasi semu di dunia maya. Rayakan setiap tonggak kecil pencapaian saldo tabunganmu dengan rasa syukur yang mendalam.

Kemandirian finansial tidak dibangun dari besarnya nominal gengsi, melainkan dari konsistensi keputusan bijak yang kamu ambil hari demi hari. Sudahkah kamu berani menerapkan prinsip loud budgeting ini di tongkronganmu?""",
        "penulis": "Indri Kartika",
        "tanggal": "17 Okt 2026",
        "status": "Diterbitkan",
        "views": 380
    },
    {
        "id": "trend-3",
        "tema": "Relationship & Cinta",
        "judul": "5 Bentuk Micro-cheating di Media Sosial yang Diam-diam Merusak Kepercayaan Pasangan",
        "cuplikan": "Interaksi digital yang tampak sepele ternyata bisa melukai komitmen. Kenali 5 tanda perselingkuhan mikro di dunia maya sebelum terlambat!",
        "kategori": "Relationship",
        "gambar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1200&auto=format&fit=crop",
        "caption_gambar": "ilustrasi pasangan memeriksa pesan rahasia di layar gawai (unsplash.com/priscilla_du_preez)",
        "sumber_gambar": "ilustrasi pasangan memeriksa pesan rahasia di layar gawai (unsplash.com/priscilla_du_preez)",
        "url_sumber": "https://unsplash.com/photos/man-and-woman-sitting-near-each-other",
        "deskripsi_gambar": "hubungan asmara micro cheating media sosial tanda pasangan",
        "rujukan_urls": [
            "https://www.psychologytoday.com/us/basics/infidelity",
            "https://www.verywellmind.com/what-is-micro-cheating-5192802"
        ],
        "isi": """Di era interaksi digital yang serbacepat, batas kesetiaan dalam sebuah hubungan asmara kerap menjadi kabur akibat interaksi daring yang terkesan sepele. Banyak orang tidak menyadari bahwa ketidaksetiaan tidak selalu berwujud perselingkuhan fisik secara terang-terangan.

Para pakar hubungan mendefinisikan fenomena perselingkuhan terselubung ini sebagai *micro-cheating*, yakni serangkaian tindakan kecil yang secara emosional mengarah pada ketertarikan rahasia di luar ikatan pasangan resmi. Berikut lima bentuk *micro-cheating* di media sosial yang sering diabaikan padahal berpotensi merusak keutuhan hubungan.

## 1. Menjaga Percakapan Rahasia di Fitur Pesan Langsung (Direct Message)
Mengirimkan pesan singkat kepada seseorang dengan sengaja menghapus riwayat obrolan (*chat history*) agar tidak terbaca oleh pasangan adalah tanda bahaya paling nyata. Jika kamu merasa perlu menyembunyikan isi percakapan tersebut, itu adalah indikator jelas bahwa ada batasan emosional yang telah kamu langgar.

Keintiman digital yang dibangun atas dasar kerahasiaan mencerminkan hilangnya rasa hormat terhadap pasangan sahmu. Hubungan yang sehat selalu dibangun di atas keterbukaan dan kejujuran tanpa ada ruang gelap yang disembunyikan.

## 2. Membiasakan Interaksi Rayuan Terselubung Berkedok Candaan
Memberikan reaksi emoji hati secara konsisten pada unggahan swafoto (*selfie*) orang lain atau membubuhkan komentar menggoda yang bernuansa romantis sering kali dibela dengan dalih 'cuma bercanda'. Padahal, intensitas perhatian visual yang berlebihan tersebut mengirimkan sinyal ketersediaan emosional secara sadar.

Perilaku ini memicu pembandingan fisik antara pasangan asli dengan sosok ideal di layar kaca. Pasanganmu berhak mendapatkan curahan perhatian terbaik, bukan sisa energi setelah kamu habiskan memvalidasi orang asing di media sosial.

## 3. Berbagi Curahan Hati Mendalam yang Seharusnya Hanya untuk Pasangan
Ketika kamu mengalami hari yang berat di tempat kerja atau menghadapi konflik keluarga, kepada siapa kamu pertama kali menceritakannya? Jika kamu lebih memilih mencurahkan kerentanan emosionalmu kepada teman lawan jenis di media sosial daripada pasanganmu sendiri, kamu telah membuka celah keterikatan batin yang berbahaya.

Proses perpindahan keintiman emosional (*emotional transfer*) inilah yang menjadi gerbang utama terjadinya perselingkuhan rasa yang lebih dalam. Pasangan hidupmu seharusnya menjadi tempat pulang pertama dan teraman untuk berkeluh kesah.

## 4. Sengaja Menyembunyikan Status Hubungan Demi Mendapatkan Validasi
Memilih untuk tidak menampilkan keberadaan pasangan sama sekali di profil publik demi mempertahankan citra seolah-olah kamu masih lajang (*single*) adalah bentuk pengkhianatan kecil yang disengaja. Motif di balik tindakan ini biasanya didorong oleh rasa haus akan atensi dan pujian dari lawan jenis.

Memvalidasi harga diri dari seberapa banyak orang yang mendekatimu di dunia maya adalah tanda ketidakmatangan emosional. Menghormati pasangan berarti bangga mengakui keberadaannya dalam setiap ruang kehidupanmu, termasuk di ruang digital.

## 5. Tetap Menjalin Kontak Hangat dengan Mantan Kekasih Tanpa Batas Jelas
Masih rutin mengirimkan pesan nostalgia, menanyakan kabar pribadi, atau memantau linimasa mantan kekasih secara obsesif adalah indikator bahwa pintu masa lalumu belum tertutup sepenuhnya. Dalih 'hanya menjaga tali silaturahmi' sering kali menjadi kedok untuk memelihara harapan romantis terpendam.

Tindakan ini tidak adil bagi pasanganmu saat ini yang berusaha membangun masa depan bersamamu. Kedewasaan cinta menuntut keberanian untuk melepaskan lembaran lama demi menjaga ketulusan komitmen yang sedang kamu bina hari ini.

Kepercayaan adalah cermin yang rapuh; sekali retak oleh kebohongan kecil, bayangan kesetiaan tidak akan pernah utuh kembali. Jagalah kehormatan hubunganmu dengan menetapkan batasan digital yang sehat bersama pasangan.""",
        "penulis": "Indri Kartika",
        "tanggal": "17 Okt 2026",
        "status": "Diterbitkan",
        "views": 510
    },
    {
        "id": "trend-4",
        "tema": "Teknologi & Gadget",
        "judul": "5 Bahaya Digital Hoarding yang Diam-diam Bikin Ruang Penyimpanan Ponselmu Sesak",
        "cuplikan": "Hobi menimbun ribuan tangkapan layar dan tab browser terbuka? Simak 5 dampak buruk menumpuk sampah digital bagi kesehatan mentalmu!",
        "kategori": "Tech",
        "gambar": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?q=80&w=1200&auto=format&fit=crop",
        "caption_gambar": "ilustrasi tumpukan aplikasi dan berkas digital pada layar smartphone (unsplash.com/nordwood)",
        "sumber_gambar": "ilustrasi tumpukan aplikasi dan berkas digital pada layar smartphone (unsplash.com/nordwood)",
        "url_sumber": "https://unsplash.com/photos/turned-on-smartphone",
        "deskripsi_gambar": "kebiasaan menimbun file sampah digital hoarding memori ponsel",
        "rujukan_urls": [
            "https://www.psychologytoday.com/us/blog/the-digital-self/202102/the-psychology-digital-hoarding",
            "https://www.wired.com/story/how-to-stop-digital-hoarding/"
        ],
        "isi": """Apakah galeri ponselmu dipenuhi oleh ribuan tangkapan layar (*screenshot*) yang tidak pernah kamu lihat lagi, ratusan tab peramban web yang dibiarkan terbuka berbulan-bulan, dan tumpukan dokumen unduhan yang terbengkalai? Jika iya, kamu kemungkinan besar mengidap sindrom *digital hoarding*.

Menimbun data digital yang sudah tidak relevan sering kali dianggap sepele karena tidak memakan ruang fisik di rumah. Namun, para pakar psikologi menemukan bahwa tumpukan kekacauan digital (*digital clutter*) memiliki dampak psikologis dan teknis yang sangat merugikan. Berikut lima bahaya tersembunyi dari kebiasaan menimbun sampah digital ini.

## 1. Peningkatan Stres dan Beban Kognitif Otak yang Tidak Disadari
Meskipun tidak tampak secara fisik di atas meja kerjamu, ribuan berkas yang berserakan di layar ponsel secara konstan membebani memori kerja otak (*working memory*). Setiap kali kamu membuka galeri atau pengelola berkas, otakmu dipaksa memproses stimulus visual yang berantakan.

Kondisi kekacauan informasi yang tak berujung ini memicu kelelahan mental bawah sadar dan menurunkan konsentrasi saat harus menyelesaikan tugas-tugas penting. Ruang digital yang bersih dan rapi menciptakan pikiran yang jauh lebih tenang dan teratur.

## 2. Penurunan Performa Ponsel dan Pemborosan Kapasitas Memori
Secara teknis, memori internal ponsel yang terisi hingga batas maksimal memperlambat kecepatan baca-tulis sistem operasi (*read-write speed*). Aplikasi akan lebih sering mengalami macet (*freeze*), waktu memuat dokumen menjadi lambat, dan baterai gawai terkuras lebih cepat karena sistem terus-menerus mengindeks data yang menumpuk.

Selain itu, kamu mungkin terpaksa merogoh kocek lebih dalam untuk berlangganan layanan penyimpanan awan (*cloud storage*) tambahan hanya demi menyimpan ribuan foto duplikat yang sebenarnya tidak bernilai guna. Membersihkan berkas sampah adalah cara termudah meremajakan ponsel lamamu.

## 3. Pemborosan Waktu Berharga Hanya untuk Menemukan Berkas Penting
Bayangkan ketika kamu sedang terburu-buru membutuhkan bukti pembayaran perbankan atau dokumen tiket perjalanan, tetapi kamu harus menggulir layar di antara belasan ribu tangkapan layar meme dan foto kabur. Waktu produktifmu akan terbuang sia-sia hanya untuk mencari selembar dokumen penting di tengah lautan sampah digital.

Kebiasaan menunda pengorganisasian berkas ke dalam folder yang rapi menciptakan kepanikan yang tidak perlu dalam situasi darurat. Struktur arsip yang terkelola dengan baik adalah kunci efisiensi kerja di zaman modern.

## 4. Meningkatkan Kerentanan Keamanan Data dan Kebocoran Privasi
Banyak orang memiliki kebiasaan ceroboh menyimpan tangkapan layar kartu identitas (KTP), nomor kartu kredit, hingga kata sandi akun di dalam galeri ponsel selama bertahun-tahun tanpa proteksi tambahan. Jika ponselmu hilang atau terkena serangan malware berbahaya, berkas-berkas sensitif tersebut dapat dengan mudah dieksploitasi oleh pihak tak bertanggung jawab.

Menghapus dokumen rahasia setelah selesai digunakan adalah langkah dasar dalam menjaga kebersihan keamanan siber pribadi (*cyber hygiene*). Jangan biarkan data pribadimu menjadi santapan empuk para pelaku kejahatan siber.

## 5. Menimbulkan Ilusi Produktivitas dan Penundaan Tindakan Nyata
Banyak orang menyimpan ratusan artikel motivasi, infografik tips karier, atau resep makanan dengan keyakinan palsu bahwa mereka akan membacanya suatu saat nanti. Pada kenyataannya, menimbun informasi hanyalah bentuk penundaan tindakan (*procrastination*) yang dibungkus ilusi belajar.

Menyimpan informasi tidak sama dengan menguasai ilmu tersebut sebelum kamu mempraktikkannya dalam kehidupan nyata. Lebih baik membaca satu artikel dan menerapkannya hari ini daripada menyimpan seratus artikel yang hanya menjadi fosil digital di memori ponselmu.

Lakukanlah *digital decluttering* secara berkala setiap akhir pekan: hapus foto yang tidak perlu, bersihkan cache aplikasi, dan rapikan foldermu. Ruang digital yang lapang akan membantumu berpikir lebih jernih dan fokus pada hal-hal yang benar-benar bermakna.""",
        "penulis": "Indri Kartika",
        "tanggal": "17 Okt 2026",
        "status": "Diterbitkan",
        "views": 340
    }
]


