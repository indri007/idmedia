import json
import os
import re
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

from src.idn_knowledge_base import (
    KATA_PENYEDAP_JUDUL,
    TEKNIK_PENUTUP,
    HIERARKI_PENULIS,
    SKEMA_POIN_MONETISASI,
    PANDUAN_20_MODUL,
    hitung_estimasi_poin,
    format_idn_times_payload,
)

# ==============================================================================
# KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="IDMedia Community — Platform Penulis Profesional",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).parent / "data" / "articles.json"

PARTIKEL_KECIL = {
    "atau", "dan", "dengan", "ke", "per", "oleh", "ala", "buat", "tetapi",
    "setelah", "tapi", "untuk", "bagi", "dari", "di", "kepada", "pun",
    "sebelum", "tentang", "yang", "daripada", "karena", "pada", "sampai", "tanpa", "agar"
}

def load_articles():
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_articles(articles):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

if "articles" not in st.session_state:
    st.session_state.articles = load_articles()

def update_and_persist(new_articles):
    st.session_state.articles = new_articles
    save_articles(new_articles)

def validate_eyd_title(title):
    words = title.strip().split()
    if not words:
        return True, ""
    issues = []
    for i, w in enumerate(words):
        clean_w = re.sub(r"[^\w]", "", w)
        lower_w = clean_w.lower()
        if i == 0:
            if w and not w[0].isupper():
                issues.append(f"Kata pertama '{w}' wajib diawali huruf kapital.")
        else:
            if lower_w in PARTIKEL_KECIL:
                if w != lower_w:
                    issues.append(f"Partikel '{w}' di tengah judul sebaiknya ditulis huruf kecil ('{lower_w}').")
            else:
                if w and not w[0].isupper():
                    issues.append(f"Kata '{w}' sebaiknya diawali huruf kapital.")
    return len(issues) == 0, issues

# ==============================================================================
# SIDEBAR
# ==============================================================================
LOGO_PATH = Path(__file__).parent / "assets" / "idmedia_logo_3d.jpg"
BANNER_PATH = Path(__file__).parent / "assets" / "idmedia_hero_banner.jpg"

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.title("✍️ IDMedia Hub")
    st.caption("Platform Penulisan & Kurasi Komunitas Berstandar Redaksi Nasional")
    st.markdown("---")
    menu = st.radio(
        "Menu Utama",
        [
            "📰 Beranda Publik",
            "✍️ Tulis & Kirim Artikel",
            "📊 Dashboard Penulis",
            "⚖️ Panel Moderasi Editor",
            "📖 10 Pedoman Emas Redaksi",
            "📚 Ensiklopedia 20 Panduan IDN",
        ],
    )
    st.markdown("---")
    st.markdown(
        """
        **Standar Kurasi Zero Reject:**
        - Format Listicle (Subjudul ➜ Foto ➜ Narasi)
        - Judul EYD V & Excerpt Hook Menarik
        - Minimal 2 URL rujukan kredibel
        - Caption & Atribusi Gambar Lengkap
        """
    )
    st.caption("© 2026 IDMedia Community · Sesuai Masterbook IDN Times")

# ==============================================================================
# 1. BERANDA PUBLIK
# ==============================================================================
if menu == "📰 Beranda Publik":
    if BANNER_PATH.exists():
        st.image(str(BANNER_PATH), use_container_width=True)
    st.title("📰 Portal Berita & Artikel Komunitas")
    st.write(
        "Koleksi tulisan inspiratif, edukatif, dan menghibur dari para penulis komunitas "
        "yang telah lolos kurasi 100% tim redaksi."
    )

    published = [a for a in st.session_state.articles if a.get("status") == "Diterbitkan"]

    categories = ["Semua Kategori", "Life", "Tech", "Career", "Relationship", "Science & Tech", "Food", "Travel", "Hiburan"]
    selected_cat = st.selectbox("Pilih Kategori:", categories)

    if selected_cat != "Semua Kategori":
        filtered = [a for a in published if a.get("kategori") == selected_cat]
    else:
        filtered = published

    st.markdown("---")

    if not filtered:
        st.info("Belum ada artikel yang diterbitkan untuk kategori ini. Jadilah yang pertama mengirimkan karya terbaikmu!")
    else:
        for i, art in enumerate(filtered):
            with st.container():
                col_img, col_txt = st.columns([1, 2])
                with col_img:
                    img_url = art.get("gambar") or "https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=800&auto=format&fit=crop"
                    st.image(img_url, use_container_width=True)
                    caption_text = art.get("caption_gambar") or art.get("sumber_gambar") or "ilustrasi artikel (pexels.com)"
                    st.caption(caption_text)
                    if art.get("url_sumber"):
                        st.caption(f"🔗 [Sumber Gambar Asli]({art['url_sumber']})")

                with col_txt:
                    st.markdown(f"**[{art.get('kategori', 'Umum')}]** · *{art.get('tanggal', '-')}*")
                    st.subheader(art.get("judul", "Tanpa Judul"))
                    if art.get("cuplikan"):
                        st.markdown(f"*{art.get('cuplikan')}*")
                    st.write(f"✍️ **Penulis:** {art.get('penulis', 'Anonim')} · 👁️ {art.get('views', 150)} Pembaca")

                    paragraphs = [p for p in art.get("isi", "").split("\n") if p.strip() and not p.strip().startswith("#")]
                    snippet = paragraphs[0][:260] + "..." if paragraphs else art.get("isi", "")[:260] + "..."
                    st.write(snippet)

                    with st.expander("📖 Baca Artikel Selengkapnya"):
                        if art.get("rujukan_urls"):
                            st.info(f"📚 **Rujukan Sumber Informasi (Cek Fakta):**\n" + "\n".join([f"- {u}" for u in art.get("rujukan_urls", [])]))
                        st.markdown(art.get("isi", ""))
                        st.divider()
                        st.caption(f"Diterbitkan di IDMedia Community · Penulis: {art.get('penulis')}")

                st.divider()

# ==============================================================================
# 2. TULIS & KIRIM ARTIKEL
# ==============================================================================
elif menu == "✍️ Tulis & Kirim Artikel":
    st.title("✍️ Formulir Penulisan Artikel Komunitas")
    st.write(
        "Kirim artikelmu dengan format listicle berstandar IDN Times. "
        "Sistem dilengkapi validator otomatis judul EYD V, kuota subjudul, excerpt, dan rujukan cek fakta."
    )

    penulis = st.text_input("Nama Lengkap Penulis (sesuai profil KTP)", placeholder="Contoh: Indri Kartika")

    col_k, col_t = st.columns([1, 1])
    with col_k:
        kategori = st.selectbox("Kategori Tulisan", ["Life", "Tech", "Career", "Relationship", "Science & Tech", "Food", "Travel", "Hiburan"])
    with col_t:
        tipe_listicle = st.radio("Format Tulisan:", ["Deskriptif / Tips / Opini (Min. 3 Subjudul)", "Kompilasi Foto (Min. 7 Subjudul)"], horizontal=True)

    min_subjudul = 7 if "Kompilasi Foto" in tipe_listicle else 3

    st.subheader("1. Judul & Cuplikan (Excerpt)")
    with st.expander("💡 Inspirasi Kata Penyedap Judul (Biar Antimainstream)"):
        st.write("Gunakan kata penyedap ini untuk memperkuat daya tarik judulmu:")
        st.write(", ".join([f"`{k}`" for k in KATA_PENYEDAP_JUDUL]))

    judul = st.text_input(
        "Judul Artikel (Gunakan angka listicle & EYD V):",
        placeholder="Contoh: 5 Tips Mengatur Keuangan untuk Gen Z agar Cepat Mandiri"
    )

    is_eyd_ok, eyd_issues = validate_eyd_title(judul)
    if judul:
        if is_eyd_ok:
            st.success("✅ Format judul sudah memenuhi kaidah kapitalisasi EYD V.")
        else:
            for issue in eyd_issues[:3]:
                st.warning(f"⚠️ {issue}")

    cuplikan = st.text_input(
        "Cuplikan / Excerpt (1 kalimat inti pesan untuk caption media sosial):",
        placeholder="Contoh: Yuk, simak 5 langkah cerdas mengelola gaji pertama agar tabunganmu aman sampai akhir bulan!"
    )

    st.subheader("2. Sumber Rujukan Cek Fakta (Minimal 2 URL)")
    st.caption("Wajib untuk kategori edukatif/eksplanatif. Cantumkan situs kredibel asli (bukan media lokal kompetitor/Wikipedia).")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        ref_url1 = st.text_input("URL Rujukan 1:", placeholder="https://www.mayoclinic.org/...")
    with col_r2:
        ref_url2 = st.text_input("URL Rujukan 2:", placeholder="https://www.nature.com/articles/...")

    st.subheader("3. Gambar Sampul (Cover)")
    gambar_url = st.text_input(
        "Tautan URL Gambar Sampul (Landscape 3:2, min. 800x350, tanpa watermark):",
        value="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=1200&auto=format&fit=crop"
    )

    col_cp1, col_cp2 = st.columns(2)
    with col_cp1:
        tipe_caption = st.radio(
            "Format Caption Gambar:",
            ["Frasa Ilustrasi (Kecil tanpa titik)", "Kalimat Berita/Peristiwa (Kapital dengan titik)"],
            horizontal=True
        )
        default_caption = "ilustrasi orang bekerja di depan laptop (pexels.com/Burst)" if "Frasa" in tipe_caption else "Suasana diskusi redaksi di Jakarta, Senin (17/10/2026). (IDN Times/Indri)"
        caption_gambar = st.text_input("Teks Caption & Sumber Gambar:", value=default_caption)
    with col_cp2:
        url_sumber_gambar = st.text_input("Alamat URL Sumber Asli Foto:", placeholder="https://www.pexels.com/photo/...")
        deskripsi_gambar = st.text_input("Deskripsi / Kata Kunci Foto:", placeholder="tips menulis produktif")

    st.subheader("4. Isi Naskah Listicle (Pola: Subjudul ➜ Foto ➜ Narasi)")
    st.caption("Pola baku: Paragraf pembuka (2-3 kalimat) ➜ `## 1. Subjudul` ➜ Narasi (min. 3 kalimat per paragraf) ➜ Paragraf penutup (Kesimpulan/Punchline/Pertanyaan).")

    c_temp1, c_temp2 = st.columns(2)
    with c_temp1:
        if st.button("📋 Masukkan Templat Listicle Otomatis"):
            st.session_state["draft_naskah"] = (
                "Paragraf pembuka berisi latar belakang singkat, masalah yang dihadapi pembaca, "
                "dan inti solusi yang ditawarkan (2-3 kalimat lugas dan menarik rasa penasaran).\n\n"
                "## 1. Poin Subjudul Pertama\n"
                "Tuliskan narasi penjelasan mendalam di sini. Hindari paragraf yang hanya berisi satu kalimat "
                "agar pembaca mendapatkan informasi yang utuh dan bernilai tambah. Minimal dua paragraf "
                "dengan masing-masing paragraf berisi tiga kalimat.\n\n"
                "## 2. Poin Subjudul Kedua\n"
                "Uraikan fakta pendukung, data, atau tips praktis yang relevan dengan topik yang sedang dibahas. "
                "Gunakan gaya bahasa santai khas media anak muda namun tetap sesuai kaidah baku KBBI.\n\n"
                "## 3. Poin Subjudul Ketiga\n"
                "Lengkapi penjelasan langkah konkret atau contoh penerapan dalam kehidupan sehari-hari. "
                "Pastikan tidak mengulang-ulang kalimat yang sama di setiap subjudul.\n\n"
                "Paragraf penutup berisi kesimpulan singkat, punchline inspiratif, atau pertanyaan yang mengajak "
                "pembaca berinteraksi di kolom komentar (1 paragraf, 2 kalimat)."
            )
    with c_temp2:
        teknik_pilih = st.selectbox("Contoh Gaya Paragraf Penutup:", list(TEKNIK_PENUTUP.keys()))
        st.caption(TEKNIK_PENUTUP[teknik_pilih])

    isi_default = st.session_state.get("draft_naskah", "")
    isi = st.text_area("Tulis Naskah Lengkap di Sini:", value=isi_default, height=380)

    words_count = len(re.findall(r"\b[\w'-]+\b", isi)) if isi else 0
    h2_matches = re.findall(r"^##\s+.+", isi, re.MULTILINE) if isi else []
    h2_count = len(h2_matches)

    st.subheader("🔍 Pengecekan Kepatuhan Redaksi Real-time")
    v1, v2, v3, v4 = st.columns(4)
    with v1:
        if words_count >= 500:
            st.success(f"✅ **Kata:** {words_count} (>= 500)")
        else:
            st.warning(f"⚠️ **Kata:** {words_count} (Kurang {500 - words_count})")
    with v2:
        if h2_count >= min_subjudul:
            st.success(f"✅ **Subjudul:** {h2_count} (Target >={min_subjudul})")
        else:
            st.warning(f"⚠️ **Subjudul:** {h2_count} (Min. {min_subjudul})")
    with v3:
        if cuplikan and len(cuplikan.split()) >= 6:
            st.success("✅ **Excerpt:** Siap")
        else:
            st.warning("⚠️ **Excerpt:** Belum diisi")
    with v4:
        if ref_url1 or ref_url2:
            st.success("✅ **Rujukan:** Ada")
        else:
            st.info("ℹ️ **Rujukan:** Disarankan min. 2")

    persetujuan = st.checkbox(
        "Saya menjamin naskah ini orisinal karya pribadi, bebas plagiarisme, gambar beresolusi baik tanpa watermark, "
        "tidak mengandung unsur SARA/fitnah, dan belum pernah diterbitkan di media massa lain."
    )

    if st.button("🚀 Kirim Naskah ke Antrean Moderasi", type="primary"):
        if not penulis or not judul or not isi or not cuplikan:
            st.error("Lengkapi nama penulis, judul artikel, cuplikan, dan isi naskah sebelum mengirim.")
        elif not persetujuan:
            st.error("Centang pernyataan etika orisinalitas sebelum melakukan submit.")
        else:
            ref_list = [u.strip() for u in [ref_url1, ref_url2] if u.strip()]
            new_id = f"art-{int(datetime.now().timestamp())}"
            new_article = {
                "id": new_id,
                "penulis": penulis.strip(),
                "kategori": kategori,
                "tipe": tipe_listicle,
                "judul": judul.strip(),
                "cuplikan": cuplikan.strip(),
                "gambar": gambar_url.strip(),
                "caption_gambar": caption_gambar.strip(),
                "sumber_gambar": caption_gambar.strip(),
                "url_sumber": url_sumber_gambar.strip(),
                "deskripsi_gambar": deskripsi_gambar.strip(),
                "rujukan_urls": ref_list,
                "isi": isi.strip(),
                "tanggal": datetime.now().strftime("%d %b %Y"),
                "status": "Menunggu Ditinjau",
                "catatan": "",
                "views": 0,
            }
            updated = [new_article] + st.session_state.articles
            update_and_persist(updated)
            st.success("🎉 Naskah berhasil dikirim ke antrean moderasi! Pantau statusnya di menu 'Dashboard Penulis'.")

# ==============================================================================
# 3. DASHBOARD PENULIS
# ==============================================================================
elif menu == "📊 Dashboard Penulis":
    st.title("📊 Dasbor Status Naskah Penulis")
    st.write("Pantau progres kurasi artikel, catatan perbaikan dari editor, dan kirim ulang naskah hasil revisi.")

    nama_penulis = st.text_input("Ketik Nama Penulis Anda:", placeholder="Contoh: Indri Kartika")

    if nama_penulis:
        tulisan_saya = [a for a in st.session_state.articles if a.get("penulis", "").strip().lower() == nama_penulis.strip().lower()]

        total = len(tulisan_saya)
        terbit = sum(1 for a in tulisan_saya if a.get("status") == "Diterbitkan")
        pending = sum(1 for a in tulisan_saya if a.get("status") == "Menunggu Ditinjau")
        revisi = sum(1 for a in tulisan_saya if a.get("status") == "Perlu Perbaikan")
        tolak = sum(1 for a in tulisan_saya if a.get("status") == "Ditolak")

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total Naskah", total)
        m2.metric("✅ Diterbitkan", terbit)
        m3.metric("⏳ Ditinjau", pending)
        m4.metric("🔧 Minta Revisi", revisi)
        m5.metric("❌ Ditolak", tolak)

        st.markdown("---")

        if not tulisan_saya:
            st.info(f"Belum ditemukan naskah atas nama '{nama_penulis}'. Pastikan ejaan nama sama persis.")
        else:
            for i, art in enumerate(tulisan_saya):
                status = art.get("status", "Menunggu Ditinjau")
                badge_color = {
                    "Diterbitkan": "🟢",
                    "Menunggu Ditinjau": "🟡",
                    "Perlu Perbaikan": "🟠",
                    "Ditolak": "🔴",
                }.get(status, "⚪")

                with st.expander(f"{badge_color} [{status.upper()}] — {art.get('judul')} ({art.get('tanggal')})"):
                    st.write(f"**Kategori:** {art.get('kategori')} | **ID Naskah:** `{art.get('id')}`")
                    if art.get("cuplikan"):
                        st.caption(f"Cuplikan: {art.get('cuplikan')}")
                    if art.get("catatan"):
                        st.warning(f"📝 **Catatan Editor:** {art.get('catatan')}")

                    if status == "Perlu Perbaikan":
                        st.info("💡 Editor meminta perbaikan. Silakan sesuaikan naskah di bawah ini lalu kirim ulang:")
                        with st.form(key=f"edit_form_{art.get('id')}"):
                            edit_judul = st.text_input("Revisi Judul", value=art.get("judul"))
                            edit_cuplikan = st.text_input("Revisi Cuplikan", value=art.get("cuplikan", ""))
                            edit_isi = st.text_area("Revisi Isi Naskah", value=art.get("isi"), height=250)
                            submit_revisi = st.form_submit_button("Kirim Ulang Hasil Revisi")
                            if submit_revisi:
                                for item in st.session_state.articles:
                                    if item.get("id") == art.get("id"):
                                        item["judul"] = edit_judul
                                        item["cuplikan"] = edit_cuplikan
                                        item["isi"] = edit_isi
                                        item["status"] = "Menunggu Ditinjau"
                                        item["catatan"] = "Revisi telah diperbaiki dan dikirimkan ulang oleh penulis."
                                update_and_persist(st.session_state.articles)
                                st.success("Naskah revisi berhasil dikirim ulang ke editor!")
                                st.rerun()

                    st.markdown("**Pratinjau Isi:**")
                    st.markdown(art.get("isi")[:300] + "...")

                    st.markdown("---")
                    st.markdown("##### 🚀 Integrasi & Dispatch ke Portal IDN Times Community")
                    col_l1, col_l2 = st.columns([1, 1])
                    with col_l1:
                        st.link_button("🌐 Buka Editor IDN Times Community ↗", "https://community.idntimes.com/create-post", type="primary")
                    with col_l2:
                        export_text = format_idn_times_payload(art)
                        st.download_button(
                            label="📥 Unduh Naskah Siap Terbit (.txt)",
                            data=export_text,
                            file_name=f"IDN_Times_{art.get('id')}.txt",
                            mime="text/plain",
                            key=f"dl_txt_{art.get('id')}"
                        )
                    with st.expander("📋 Salin Naskah Format Lengkap (Siap Paste ke IDN Times)"):
                        st.code(export_text, language="markdown")

# ==============================================================================
# 4. PANEL MODERASI EDITOR
# ==============================================================================
elif menu in ["Panel Moderasi Editor", "⚖️ Panel Moderasi Editor", "🔐 Panel Moderasi Editor"]:
    st.title("⚖️ Panel Moderasi & Kurasi Redaksi")
    st.caption("Akses tim editor untuk memeriksa kepatuhan 10 pedoman emas naskah dan gambar sebelum diterbitkan.")

    filter_status = st.selectbox(
        "Filter Status Antrean",
        ["Semua", "Menunggu Ditinjau", "Perlu Perbaikan", "Diterbitkan", "Ditolak"],
    )

    all_arts = st.session_state.articles
    if filter_status != "Semua":
        display_arts = [a for a in all_arts if a.get("status") == filter_status]
    else:
        display_arts = all_arts

    st.write(f"Menampilkan **{len(display_arts)}** artikel dalam antrean.")
    st.markdown("---")

    for idx, art in enumerate(display_arts):
        with st.container():
            art_id = art.get("id")
            st.subheader(f"{art.get('judul')} — [{art.get('status')}]")
            st.write(f"✍️ **Penulis:** {art.get('penulis')} | 📂 **Kategori:** {art.get('kategori')} | 📅 **Tanggal:** {art.get('tanggal')}")

            word_count = len(re.findall(r"\b[\w'-]+\b", art.get("isi", "")))
            h2_count = len(re.findall(r"^##\s+.+", art.get("isi", ""), re.MULTILINE))
            st.caption(f"Statistik: {word_count} kata | {h2_count} subjudul H2")

            with st.expander("📖 Tinjau Naskah, Gambar, & Sumber Rujukan"):
                if art.get("cuplikan"):
                    st.markdown(f"**Cuplikan (Excerpt):** *{art.get('cuplikan')}*")
                if art.get("rujukan_urls"):
                    st.markdown("**URL Rujukan Cek Fakta:**")
                    for u in art.get("rujukan_urls"):
                        st.write(f"- [{u}]({u})")
                if art.get("gambar"):
                    st.image(art.get("gambar"), width=420)
                    caption_str = art.get('caption_gambar') or art.get('sumber_gambar') or 'Tanpa caption'
                    st.caption(f"Caption: {caption_str}")
                    if art.get("url_sumber"):
                        st.caption(f"URL Sumber Foto: {art.get('url_sumber')}")
                st.markdown(art.get("isi"))

            st.markdown("**Keputusan Editorial:**")
            c_act1, c_act2, c_act3 = st.columns(3)

            with c_act1:
                if st.button(f"✅ Terbitkan (Tayang)", key=f"pub_{art_id}"):
                    for a in st.session_state.articles:
                        if a.get("id") == art_id:
                            a["status"] = "Diterbitkan"
                            a["catatan"] = "Lolos kurasi redaksi dan telah diterbitkan resmi."
                    update_and_persist(st.session_state.articles)
                    st.success(f"Artikel '{art.get('judul')}' berhasil diterbitkan!")
                    st.rerun()

            with c_act2:
                catatan_revisi = st.text_input("Catatan revisi:", key=f"rev_txt_{art_id}", placeholder="Misal: Tambah subjudul / perbaiki caption gambar...")
                if st.button(f"🔧 Minta Revisi", key=f"rev_btn_{art_id}"):
                    for a in st.session_state.articles:
                        if a.get("id") == art_id:
                            a["status"] = "Perlu Perbaikan"
                            a["catatan"] = catatan_revisi or "Mohon sesuaikan dengan kaidah teknis redaksi."
                    update_and_persist(st.session_state.articles)
                    st.warning("Status diubah menjadi Perlu Perbaikan.")
                    st.rerun()

            with c_act3:
                alasan_tolak = st.text_input("Alasan penolakan:", key=f"rej_txt_{art_id}", placeholder="Misal: Kurang 500 kata / terindikasi plagiasi...")
                if st.button(f"❌ Tolak Naskah", key=f"rej_btn_{art_id}"):
                    for a in st.session_state.articles:
                        if a.get("id") == art_id:
                            a["status"] = "Ditolak"
                            a["catatan"] = alasan_tolak or "Naskah tidak memenuhi syarat penerbitan redaksi."
                    update_and_persist(st.session_state.articles)
                    st.error("Naskah ditolak.")
                    st.rerun()

            if art.get("status") == "Diterbitkan":
                st.markdown("##### 🚀 Integrasi & Dispatch ke Portal IDN Times Community:")
                c_dsp1, c_dsp2 = st.columns([1, 1])
                with c_dsp1:
                    st.link_button("🌐 Buka Form Tulis Berita IDN Times ↗", "https://community.idntimes.com/create-post")
                with c_dsp2:
                    exp_payload = format_idn_times_payload(art)
                    st.download_button(
                        label="📥 Download Paket Naskah Siap Terbit (.txt)",
                        data=exp_payload,
                        file_name=f"IDN_Times_Ready_{art_id}.txt",
                        mime="text/plain",
                        key=f"dl_pub_{art_id}"
                    )

            st.divider()

# ==============================================================================
# 5. 10 PEDOMAN EMAS REDAKSI
# ==============================================================================
elif menu == "📖 10 Pedoman Emas Redaksi":
    st.title("📖 10 Pedoman Emas Penulisan IDN Times Community")
    st.write("Terapkan 10 aturan emas ini agar naskahmu langsung lolos kurasi editor tanpa revisi (Zero Reject).")

    p1, p2, p3, p4, p5 = st.tabs([
        "1–2. Judul & Cuplikan",
        "3–4. Listicle & Pola",
        "5–6. Gambar & Sumber Rujukan",
        "7–8. Paragraf & Kedalaman",
        "9–10. Self-Audit & Submit",
    ])

    with p1:
        st.markdown(
            """
            ### 1. Judul Menarik & Sesuai Kaidah EYD V
            * **Lugas & Jelas**: Tidak bertele-tele, langsung sampaikan inti pesan tulisan.
            * **Gunakan Angka**: Pasang angka numerik untuk artikel listicle (contoh: *5 Fakta Unik...*, *7 Cara Jitu...*).
            * **Aturan Huruf Kapital**: Setiap huruf pertama di awal kata wajib kapital, **KECUALI** partikel kecil di tengah:
              * *atau, dan, dengan, ke, per, oleh, ala, buat, tetapi, setelah, tapi, untuk, bagi, dari, di, kepada, pun, sebelum, tentang, yang, daripada, karena, pada, sampai, tanpa, agar*.
            * *Contoh Benar:* `"5 Tips Mengatur Keuangan untuk Gen Z agar Cepat Mandiri"`

            ---
            ### 2. Cuplikan (Excerpt) Menarik
            * Terletak tepat di bawah judul berupa **satu kalimat** inti pesan tulisan.
            * Berfungsi sebagai *hook* dan caption ketika dibagikan ke media sosial.
            * Boleh dibuat sedikit nyeleneh dan santai asalkan tetap relevan dengan konteks tulisan.
            """
        )

    with p2:
        st.markdown(
            """
            ### 3. Bentuk Artikel Listicle & Kuota Subjudul
            * **Artikel Deskriptif / Tips / Opini / Zodiak / Kuliner**: Minimal **3 subjudul**.
            * **Kompilasi Foto / Galeri**: Minimal **7 subjudul** relevan dengan narasi informatif.
            * Setiap subjudul wajib memiliki nomor angka numerik.

            ---
            ### 4. Pola Listicle Baku IDN Times
            Pola urutan yang benar di setiap subjudul:
            1. **Subjudul (H2)**
            2. **Foto / Gambar Pendukung**
            3. **Narasi Penjelas**
            """
        )

    with p3:
        st.markdown(
            """
            ### 5. Ketentuan Gambar & Atribusi Lengkap
            * **Ukuran & Rasio**: Maksimal 1 MB, rasio **3:2** (landscape, min. 800x350 px), tanpa watermark.
            * **Objek Hidup**: Gambarkan aktivitas manusia (mengetik laptop, menyiram tanaman, menyesap kopi).
            * **Format Caption**:
              * *Frasa:* Huruf kecil tanpa titik ➜ `ilustrasi orang bekerja (pexels.com/Burst)`
              * *Kalimat Peristiwa:* Huruf kapital dengan titik ➜ `Penulis menghadiri workshop di Jakarta, Senin (17/10/2026). (IDN Times/Indri)`

            ---
            ### 6. Wajib Cantumkan URL Rujukan Asli (Cek Fakta)
            * Wajib minimal **2 tautan rujukan kredibel** di awal tulisan untuk kategori sains, kesehatan, bisnis, entertainment, dll.
            * Rujukan harus dari sumber asli (jurnal, buku, situs resmi institusi).
            * Dilarang menggunakan Wikipedia, Kaskus, blog pribadi orang, atau media lokal kompetitor.
            * Penyebutan dalam teks dicetak miring, contoh: *dilansir Live Science*, *dilansir Mashable*.
            """
        )

    with p4:
        st.markdown(
            """
            ### 7. Paragraf Pembuka & Penutup
            * **Pembuka**: 1–2 paragraf dengan 2–3 kalimat saja. Buat pembaca penasaran!
            * **Penutup**: Cukup 1 paragraf dengan 2 kalimat melalui 3 opsi pilihan:
              * *Kesimpulan:* Merangkum solusi dari poin yang telah dibahas.
              * *Punchline:* Kalimat bijak atau inspirasi penutup yang menyentuh.
              * *Pertanyaan:* Mengajak pembaca berdiskusi di kolom komentar.

            ---
            ### 8. Informasi Mendalam (Anti-Satu Kalimat)
            * Setiap paragraf narasi wajib berisi **minimal 3 kalimat**.
            * Berikan penjelasan mendalam agar pembaca merasakan nilai tambah dari karyamu.
            """
        )

    with p5:
        st.markdown(
            """
            ### 9. Cek Typo (Saltik) & Ejaan Sebelum Kirim
            * Baca ulang naskah secara perlahan sebelum submit.
            * Pastikan tidak ada kata yang terlewat, huruf tertukar, atau salah penempatan tanda baca.

            ---
            ### 10. Submit Percaya Diri ke Tim Editor
            * Bila seluruh daftar periksa 1–9 sudah terpenuhi, klik tombol kirim!
            * Hindari mengirim ulang artikel yang sama berulang kali agar tidak terdeteksi sebagai spam.
            """
        )

# ==============================================================================
# 6. ENSIKLOPEDIA 20 PANDUAN RESMI & KALKULATOR POIN
# ==============================================================================
elif menu == "📚 Ensiklopedia 20 Panduan IDN":
    st.title("📚 Ensiklopedia 20 Panduan Resmi IDN Times Community")
    st.write(
        "Hasil ekstraksi (reverse engineering) seluruh basis pengetahuan editorial resmi IDN Times: "
        "hierarki penulis, skema monetisasi poin, dan 20 artikel panduan kurasi redaksi."
    )

    t_mod, t_poin, t_tier, t_lic = st.tabs([
        "📖 20 Modul Panduan Resmi",
        "💰 Kalkulator Poin & Monetisasi",
        "🎖️ Jenjang Karir Penulis (Tier)",
        "📜 Lisensi & Ketentuan Hukum",
    ])

    with t_mod:
        st.subheader("Daftar 20 Artikel Panduan Resmi Terintegrasi")
        cari = st.text_input("🔍 Cari panduan atau topik spesifik:", placeholder="Misal: judul, revisi, poin, piala dunia, puisi...")

        filtered_modul = PANDUAN_20_MODUL
        if cari:
            filtered_modul = [
                m for m in PANDUAN_20_MODUL
                if cari.lower() in m["judul"].lower() or cari.lower() in m["inti"].lower() or cari.lower() in m["kategori"].lower()
            ]

        for m in filtered_modul:
            with st.expander(f"#{m['id']} [{m['kategori']}] — {m['judul']}"):
                st.write(f"**Intisari Aturan Redaksi:** {m['inti']}")

    with t_poin:
        st.subheader("Simulasi Finansial & Konversi IDN Points")
        st.markdown(
            f"""
            - **Rasio Views**: {SKEMA_POIN_MONETISASI['rasio_views']}
            - **Konversi Nilai**: {SKEMA_POIN_MONETISASI['konversi_rupiah']}
            - **Ambang Batas Pencairan**: {SKEMA_POIN_MONETISASI['ambang_pencairan']}
            - **Metode Pembayaran**: {', '.join(SKEMA_POIN_MONETISASI['metode_redeem'])}
            """
        )
        st.markdown("---")
        sim_views = st.number_input("Masukkan Perkiraan Akumulasi Views Artikelmu:", min_value=0, value=25000, step=1000)
        poin_est, rupiah_est = hitung_estimasi_poin(sim_views)

        k1, k2 = st.columns(2)
        k1.metric("Perolehan Poin", f"{poin_est:,} Poin")
        k2.metric("Estimasi Rupiah", f"Rp{rupiah_est:,}")

        if poin_est >= 2500:
            st.success("🎉 Ambang batas minimal 2.500 poin telah tercapai! Saldo siap ditarik (redeem).")
        else:
            st.warning(f"Kurang {2500 - poin_est:,} poin lagi untuk mencapai ambang batas pencairan pertama.")

    with t_tier:
        st.subheader("Tingkatan & Lencana Penulis IDN Times")
        for tier_name, tier_info in HIERARKI_PENULIS.items():
            with st.container():
                st.markdown(f"### 🏅 {tier_name}")
                st.write(tier_info["deskripsi"])
                st.caption(f"**Syarat:** {tier_info['syarat']} | **Keuntungan:** {tier_info['benefit']}")
                st.divider()

    with t_lic:
        st.subheader("📜 Lisensi Perangkat Lunak & Hak Cipta Konten")
        st.markdown(
            """
            **MIT License (Open Source Software)**  
            *Copyright (c) 2026 Indri Kartika (IDMedia)*

            Platform ini dilisensikan secara resmi menggunakan **MIT License**. Siapa pun diberikan izin secara gratis untuk menggunakan, menyalin, memodifikasi, menggabungkan, mempublikasikan, dan mendistribusikan salinan perangkat lunak ini sesuai dengan syarat lisensi MIT.

            ---

            ### ⚖️ Ketentuan Hak Cipta Konten & Kode Etik Redaksi:
            1. **Kepemilikan Hak Cipta**: Seluruh teks artikel yang ditulis dan dikirimkan oleh penulis tetap merupakan hak cipta intelektual masing-masing kontributor.
            2. **Keaslian Naskah**: Penulis wajib menjamin tulisan orisinal dan bebas dari segala bentuk plagiarisme atau pelanggaran hak cipta pihak ketiga.
            3. **Atribusi Sumber Gambar**: Penggunaan foto/ilustrasi wajib mencantumkan sumber asli sesuai SOP gambar beresolusi baik tanpa watermark.
            4. **Bebas SARA & Netral**: Konten yang diterbitkan tidak boleh mengandung unsur kebencian, pencemaran nama baik, atau kampanye terselubung.
            """
        )
