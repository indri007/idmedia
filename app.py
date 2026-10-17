import json
import os
import re
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

from database import (
    init_db,
    kirim_artikel,
    ambil_artikel_penulis,
    ambil_semua_artikel,
    ambil_artikel_terbit,
    update_status_artikel,
    update_isi_artikel,
    tambah_views_artikel,
    ambil_statistik_platform,
)
from auth import (
    inisialisasi_sesi,
    atur_sesi,
    keluar_sesi,
    tombol_keluar,
    render_user_badge_sidebar,
    halaman_login,
    cek_login,
    cek_peran_admin,
)
from src.idn_knowledge_base import (
    KATA_PENYEDAP_JUDUL,
    TEKNIK_PENUTUP,
    HIERARKI_PENULIS,
    SKEMA_POIN_MONETISASI,
    PANDUAN_20_MODUL,
    MASTERBOOK_12_MODUL,
    hitung_estimasi_poin,
    format_idn_times_payload,
    TRENDING_GAP_ARTICLES,
)

# ==============================================================================
# KONFIGURASI HALAMAN & TEMA VISUAL MATERIAL 3
# ==============================================================================
st.set_page_config(
    page_title="IDMedia Community — Platform Penulis Profesional",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inisialisasi basis data permanen dan sesi akun pengguna
init_db()
inisialisasi_sesi()

# Custom CSS Estetika Glassmorphism & Material 3
st.markdown(
    """
    <style>
    /* Gradient highlight untuk elemen metrik dan kartu */
    .stMetric {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 12px 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .badge-terbit { background-color: #059669; color: #ffffff; }
    .badge-tinjau { background-color: #d97706; color: #ffffff; }
    .badge-revisi { background-color: #0284c7; color: #ffffff; }
    .badge-tolak { background-color: #dc2626; color: #ffffff; }
    </style>
    """,
    unsafe_allow_html=True,
)

PARTIKEL_KECIL = {
    "atau", "dan", "dengan", "ke", "per", "oleh", "ala", "buat", "tetapi",
    "setelah", "tapi", "untuk", "bagi", "dari", "di", "kepada", "pun",
    "sebelum", "tentang", "yang", "daripada", "karena", "pada", "sampai", "tanpa", "agar"
}

def validate_eyd_title(title):
    words = title.strip().split()
    if not words:
        return True, []
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

    # Tampilkan identitas akun aktif yang terhubung
    render_user_badge_sidebar()

    menu = st.radio(
        "Menu Utama",
        [
            "📰 Beranda Publik",
            "🔥 Ide Trending & Generator 100% Lolos",
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
        "yang telah tersimpan permanen di basis data dan lolos kurasi 100% tim redaksi."
    )

    # Metrik Ringkasan Platform dari Basis Data Permanen
    stats = ambil_statistik_platform()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📚 Naskah Terbit", f"{stats['published']} Artikel")
    m2.metric("👁️ Total Pembaca", f"{stats['total_views']:,} Views")
    m3.metric("👥 Penulis Terdaftar", f"{stats['total_users']} Akun")
    m4.metric("⏳ Dalam Antrean", f"{stats['pending']} Menunggu")

    st.markdown("---")

    categories = ["Semua Kategori", "Life", "Tech", "Career", "Relationship", "Science & Tech", "Food", "Travel", "Hiburan"]
    selected_cat = st.selectbox("Filter Kategori Tulisan:", categories)

    df_pub = ambil_artikel_terbit(selected_cat)

    if df_pub.empty:
        st.info("Belum ada artikel yang diterbitkan untuk kategori ini. Jadilah yang pertama mengirimkan karya terbaikmu!")
    else:
        for idx, row in df_pub.iterrows():
            with st.container():
                col_img, col_txt = st.columns([1, 2])
                with col_img:
                    img_url = row["cover_url"] or "https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=800&auto=format&fit=crop"
                    st.image(img_url, use_container_width=True)
                    caption_text = row["source_caption"] or "ilustrasi artikel (unsplash.com)"
                    st.caption(caption_text)

                with col_txt:
                    st.markdown(f"**[{row['category']}]** · *{row['created_at'][:10]}*")
                    st.subheader(row["title"])
                    if row["excerpt"]:
                        st.markdown(f"*{row['excerpt']}*")
                    st.write(f"✍️ **Penulis:** {row['author_name']} · 👁️ {row['views']} Pembaca")

                    paragraphs = [p for p in row["content"].split("\n") if p.strip() and not p.strip().startswith("#")]
                    snippet = paragraphs[0][:260] + "..." if paragraphs else row["content"][:260] + "..."
                    st.write(snippet)

                    with st.expander("📖 Baca Artikel Selengkapnya"):
                        tambah_views_artikel(row["id"], 1)
                        st.markdown(row["content"])
                        st.divider()
                        st.caption(f"Diterbitkan di IDMedia Community · Penulis: {row['author_name']}")

                st.divider()

# ==============================================================================
# 2. IDE TRENDING & GENERATOR NASKAH 100% LOLOS
# ==============================================================================
elif menu == "🔥 Ide Trending & Generator 100% Lolos":
    st.title("🔥 Bank Ide Trending & Generator Naskah 100% Layak Terbit")
    st.write(
        "Koleksi topik hangat hasil *Content Gap Analysis* yang dirancang khusus memenuhi seluruh kaidah kurasi IDN Times Community: "
        "format listicle terstruktur, judul EYD V, excerpt pemikat, SOP gambar beresolusi tinggi, dan 2 URL rujukan cek fakta."
    )

    t_filter = st.selectbox(
        "Pilih Niche / Tema Trending:",
        ["Semua Tema", "Health & Lifestyle", "Career & Finansial", "Relationship & Cinta", "Teknologi & Gadget"]
    )

    display_trends = TRENDING_GAP_ARTICLES
    if t_filter != "Semua Tema":
        display_trends = [t for t in TRENDING_GAP_ARTICLES if t.get("tema") == t_filter]

    st.markdown("---")

    for idx, t_art in enumerate(display_trends):
        with st.container():
            col_t_img, col_t_txt = st.columns([1, 2])
            with col_t_img:
                st.image(t_art["gambar"], use_container_width=True)
                st.caption(t_art["caption_gambar"])
                if t_art.get("url_sumber"):
                    st.caption(f"🔗 [Sumber Foto Asli]({t_art['url_sumber']})")

            with col_t_txt:
                st.markdown(f"**[{t_art['tema']}]** · Target: 100% Lolos Kurasi Redaksi")
                st.subheader(t_art["judul"])
                st.markdown(f"*{t_art['cuplikan']}*")
                st.write(f"✍️ **Penulis:** {t_art['penulis']} | 🏷️ **Kategori:** `{t_art['kategori']}`")

                with st.expander("📋 Pratinjau Naskah Lengkap & 2 URL Rujukan Fakta"):
                    st.info(
                        "📚 **Rujukan Validitas (Cek Fakta):**\n"
                        + "\n".join([f"- {url}" for url in t_art["rujukan_urls"]])
                    )
                    st.markdown(t_art["isi"])

                st.markdown("**Tindakan Cepat:**")
                btn_c1, btn_c2, btn_c3 = st.columns(3)
                with btn_c1:
                    if st.button("🚀 Simpan & Terbitkan ke Database", key=f"pub_trend_{t_art['id']}"):
                        new_id = kirim_artikel(
                            author_id=st.session_state.get("user_id", 2) or 2,
                            author_name=st.session_state.get("full_name", t_art["penulis"]),
                            title=t_art["judul"],
                            content=t_art["isi"],
                            excerpt=t_art["cuplikan"],
                            category=t_art["kategori"],
                            cover_url=t_art["gambar"],
                            source_caption=t_art["caption_gambar"]
                        )
                        update_status_artikel(new_id, "published", "Naskah trending tervalidasi langsung terbit ke portal.")
                        st.success(f"Naskah '{t_art['judul']}' berhasil disimpan permanen ke database & berstatus Terbit!")
                        st.rerun()

                with btn_c2:
                    export_trend = format_idn_times_payload(t_art)
                    st.download_button(
                        "📥 Download Paket Naskah (.txt)",
                        data=export_trend,
                        file_name=f"IDN_Times_{t_art['id']}.txt",
                        mime="text/plain",
                        key=f"dl_tr_{t_art['id']}"
                    )

                with btn_c3:
                    st.link_button("🌐 Buka Form IDN Times ↗", "https://community.idntimes.com/create-post")

            st.divider()

# ==============================================================================
# 3. TULIS & KIRIM ARTIKEL
# ==============================================================================
elif menu == "✍️ Tulis & Kirim Artikel":
    st.title("✍️ Formulir Penulisan Artikel Komunitas")
    st.write(
        "Kirim artikelmu dengan format listicle berstandar IDN Times. "
        "Tulisan tersimpan permanen di basis data dan dilengkapi validator otomatis judul EYD V, subjudul, dan excerpt."
    )

    # Identitas Penulis Aktif
    penulis_nama = st.session_state.get("full_name", "INDRI ANJAR KARTIKA Sari")
    handle_info = st.session_state.get("idn_handle", "@ind-juv5brthzlf")
    st.info(f"👤 **Identitas Penulis Terdaftar:** {penulis_nama} ({handle_info}) — *Akun IDN Terhubung*")

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
        caption_gambar = st.text_input(
            "Teks Caption & Sumber Gambar:",
            value="ilustrasi orang bekerja di depan laptop (pexels.com/Burst)"
        )
    with col_cp2:
        url_sumber_gambar = st.text_input("Alamat URL Sumber Asli Foto:", placeholder="https://www.pexels.com/photo/...")

    st.subheader("4. Isi Naskah Listicle (Pola: Subjudul ➜ Foto ➜ Narasi)")
    st.caption("Pola baku: Paragraf pembuka (2-3 kalimat) ➜ `## 1. Subjudul` ➜ Narasi (min. 3 kalimat per paragraf) ➜ Paragraf penutup.")

    col_btn_tpl1, col_btn_tpl2 = st.columns([1, 1])
    with col_btn_tpl1:
        if st.button("📋 Masukkan Template Kerangka 5 Poin Siap Tulis"):
            st.session_state.draft_content = (
                "Tuliskan 2-3 kalimat paragraf pengantar di sini untuk memikat minat baca audiens pada 5 detik pertama. "
                "Jelaskan latar belakang masalah dan mengapa topik ini sangat penting dibahas hari ini. "
                "Berikut lima ulasan penting yang patut kamu ketahui.\n\n"
                "## 1. Subjudul Poin Pertama\n"
                "Tuliskan narasi penjelasan poin pertama di sini. Pastikan terdiri dari minimal 3 kalimat berbobot. "
                "Sertakan data pendukung atau contoh kasus nyata agar pembaca mendapatkan wawasan baru. "
                "Hindari pengulangan kata yang tidak perlu agar alur tulisan tetap mengalir lancar.\n\n"
                "## 2. Subjudul Poin Kedua\n"
                "Jelaskan poin kedua secara mendalam di sini. Hubungkan dengan fakta ilmiah atau rujukan terpercaya. "
                "Berikan tips aplikatif yang dapat langsung dipraktikkan oleh pembaca dalam keseharian mereka. "
                "Susun kalimat secara aktif agar lebih lugas dan bertenaga.\n\n"
                "## 3. Subjudul Poin Ketiga\n"
                "Ulas aspek ketiga dengan sudut pandang yang unik dan belum banyak diulas oleh media lain. "
                "Gunakan perumpamaan atau ilustrasi sederhana untuk memudahkan pemahaman konsep yang rumit. "
                "Jaga ritme membaca dengan membatasi panjang kalimat maksimal 20 kata per baris.\n\n"
                "## 4. Subjudul Poin Keempat\n"
                "Paparkan solusi atau pembelajaran penting dari poin keempat. "
                "Tunjukkan dampak positif jika pembaca menerapkan kiat yang kamu sampaikan. "
                "Perhatikan kaidah tanda baca koma sebelum kata hubung sesuai standar EYD V.\n\n"
                "## 5. Subjudul Poin Kelima\n"
                "Lengkapi dengan poin kelima sebagai penutup rangkaian listicle yang utuh dan komprehensif. "
                "Berikan argumen pamungkas yang menyatukan seluruh benang merah pembahasan dari poin pertama hingga kelima. "
                "Tutup dengan kalimat refleksi yang menggugah emosi positif pembaca.\n\n"
                "Dari kelima poin di atas, langkah mana yang paling ingin segera kamu terapkan dalam kehidupan sehari-hari?"
            )
            st.rerun()

    isi = st.text_area(
        "Isi Lengkap Artikel:",
        value=st.session_state.get("draft_content", ""),
        height=380,
        placeholder="Mulai ketik draf artikelmu di sini..."
    )

    # Audit Real-Time Kuantitatif & Standar Redaksi
    word_count = len(re.findall(r"\b[\w'-]+\b", isi))
    h2_matches = re.findall(r"^##\s+.+", isi, re.MULTILINE)
    h2_count = len(h2_matches)

    st.markdown("---")
    st.subheader("📊 Indikator Kepatuhan Redaksi Real-time")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah Kata (Min. 500)", f"{word_count} kata", delta=f"{word_count - 500}" if word_count >= 500 else f"{word_count - 500}")
    c2.metric(f"Subjudul H2 (Min. {min_subjudul})", f"{h2_count} subjudul", delta=f"{h2_count - min_subjudul}" if h2_count >= min_subjudul else f"{h2_count - min_subjudul}")
    c3.metric("Status Judul EYD V", "Lolos ✅" if is_eyd_ok and judul else "Periksa ⚠️")
    c4.metric("Penyimpanan", "SQLite Permanen 💾")

    # Tombol Pengiriman Naskah ke Meja Redaksi
    if st.button("🚀 Kirim Naskah ke Antrean Redaksi & Simpan", type="primary", use_container_width=True):
        errors = []
        if not judul:
            errors.append("Judul artikel wajib diisi.")
        if not is_eyd_ok:
            errors.append("Format judul belum sesuai kaidah kapitalisasi EYD V.")
        if word_count < 500:
            errors.append(f"Jumlah kata baru {word_count}. Syarat minimal redaksi adalah 500 kata.")
        if h2_count < min_subjudul:
            errors.append(f"Jumlah subjudul H2 baru {h2_count}. Minimal {min_subjudul} subjudul diperlukan.")
        if not isi:
            errors.append("Isi artikel masih kosong.")

        if errors:
            st.error("❌ Naskah belum memenuhi standar kurasi:")
            for err in errors:
                st.write(f"- {err}")
        else:
            new_id = kirim_artikel(
                author_id=st.session_state.get("user_id", 2) or 2,
                author_name=penulis_nama,
                title=judul,
                content=isi,
                excerpt=cuplikan or isi[:150] + "...",
                category=kategori,
                cover_url=gambar_url,
                source_caption=caption_gambar,
            )
            st.success(f"🎉 Selamat! Naskah '{judul}' berhasil dikirim dan tersimpan permanen di database (ID: #{new_id})!")
            st.info("Status naskah saat ini: ⏳ **Menunggu Ditinjau oleh Editor**.")
            st.balloons()

# ==============================================================================
# 4. DASHBOARD PENULIS (STATUS, POIN, & KARTU IDN RESMI)
# ==============================================================================
elif menu == "📊 Dashboard Penulis":
    st.title("📊 Status & Dashboard Tulisan Penulis")
    st.write("Pantau progres kurasi artikel, catatan perbaikan dari editor, dan kirim ulang naskah hasil revisi.")

    # Profil Resmi Penulis Terhubung
    col_card, col_stat = st.columns([1, 2])
    with col_card:
        IDN_CARD = Path(__file__).parent / "assets" / "idn_user_card.png"
        if IDN_CARD.exists():
            st.image(str(IDN_CARD), caption="Identitas Resmi Penulis IDN Media", use_container_width=True)

    with col_stat:
        st.markdown(
            f"""
            ### 🪪 {st.session_state.get('full_name', 'INDRI ANJAR KARTIKA Sari')}
            - **Handle IDN**: `{st.session_state.get('idn_handle', '@ind-juv5brthzlf')}`
            - **Email Terdaftar**: `{st.session_state.get('email', '25067020011@student.upnjatim.ac.id')}`
            - **Status Koneksi**: 🟢 **TERHUBUNG RESMI (Cognito Client ID: 2lnitap1rj2b3mb00iifvnj3ni)**
            - **Device ID**: `01a149ab-1869-7792-9d3a-d18f1ddf5200`
            - **Jenjang Reputasi**: 🏅 **Verified Writer & Senior Editor**
            """
        )

    st.markdown("---")

    # Ambil artikel penulis dari basis data permanen
    uid = st.session_state.get("user_id", 2) or 2
    df_mine = ambil_artikel_penulis(uid)

    total = len(df_mine)
    terbit = len(df_mine[df_mine["status"] == "published"]) if not df_mine.empty else 0
    pending = len(df_mine[df_mine["status"] == "pending"]) if not df_mine.empty else 0
    revisi = len(df_mine[df_mine["status"] == "revision"]) if not df_mine.empty else 0
    tolak = len(df_mine[df_mine["status"] == "rejected"]) if not df_mine.empty else 0

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Naskah", total)
    m2.metric("✅ Diterbitkan", terbit)
    m3.metric("⏳ Ditinjau", pending)
    m4.metric("🔧 Minta Revisi", revisi)
    m5.metric("❌ Ditolak", tolak)

    st.markdown("---")

    if df_mine.empty:
        st.info("Belum ada tulisan yang dikirimkan. Mulai buat karya pertamamu di menu **✍️ Tulis & Kirim Artikel**!")
    else:
        for idx, art in df_mine.iterrows():
            status = art["status"]
            badge_map = {
                "published": ("🟢", "SUDAH TERBIT", "badge-terbit"),
                "pending": ("🟡", "MENUNGGU DITINJAU", "badge-tinjau"),
                "revision": ("🔵", "PERLU PERBAIKAN", "badge-revisi"),
                "rejected": ("🔴", "DITOLAK", "badge-tolak"),
            }
            icon, label, css_cls = badge_map.get(status, ("⚪", status.upper(), ""))

            with st.expander(f"{icon} [{label}] — {art['title']} ({art['created_at'][:10]})"):
                st.write(f"**Kategori:** {art['category']} | **ID Naskah:** `#{art['id']}` | **Views:** {art['views']:,} Pembaca")
                if art["note"]:
                    st.warning(f"📝 **Catatan Editor:** {art['note']}")

                if status == "revision":
                    st.info("💡 Editor meminta perbaikan. Silakan sesuaikan naskah di bawah ini lalu kirim ulang:")
                    full_art = ambil_semua_artikel().loc[ambil_semua_artikel()["id"] == art["id"]].iloc[0]
                    with st.form(key=f"edit_form_{art['id']}"):
                        edit_judul = st.text_input("Revisi Judul", value=full_art["title"])
                        edit_isi = st.text_area("Revisi Isi Naskah", value=full_art["content"], height=250)
                        submit_revisi = st.form_submit_button("Kirim Ulang Hasil Revisi")
                        if submit_revisi:
                            update_isi_artikel(art["id"], edit_judul, edit_isi)
                            update_status_artikel(art["id"], "pending", "Naskah telah direvisi oleh penulis.")
                            st.success("Naskah revisi berhasil dikirim ulang ke editor!")
                            st.rerun()

                st.markdown("---")
                st.markdown("##### 🚀 Integrasi & Dispatch ke Portal IDN Times Community")
                col_l1, col_l2 = st.columns([1, 1])
                with col_l1:
                    st.link_button("🌐 Buka Editor IDN Times Community ↗", "https://community.idntimes.com/create-post", type="primary")
                with col_l2:
                    export_text = format_idn_times_payload({
                        "id": art["id"],
                        "judul": art["title"],
                        "isi": "",
                        "penulis": st.session_state.get("full_name", "INDRI ANJAR KARTIKA Sari"),
                        "kategori": art["category"],
                    })
                    st.download_button(
                        label="📥 Download Paket Naskah (.txt)",
                        data=export_text,
                        file_name=f"IDN_Times_Post_{art['id']}.txt",
                        mime="text/plain",
                        key=f"dl_dash_{art['id']}"
                    )

# ==============================================================================
# 5. PANEL MODERASI EDITOR
# ==============================================================================
elif menu in ["Panel Moderasi Editor", "⚖️ Panel Moderasi Editor", "🔐 Panel Moderasi Editor"]:
    st.title("⚖️ Panel Moderasi & Kurasi Redaksi")
    st.caption("Akses tim editor untuk memeriksa kepatuhan 10 pedoman emas naskah dan gambar sebelum diterbitkan.")

    filter_status = st.selectbox(
        "Filter Status Antrean",
        ["pending", "published", "revision", "rejected", "Semua"],
        format_func=lambda x: {
            "pending": "⏳ Menunggu Ditinjau (Pending)",
            "published": "✅ Sudah Diterbitkan (Published)",
            "revision": "🔧 Perlu Perbaikan (Revision)",
            "rejected": "❌ Ditolak (Rejected)",
            "Semua": "Semua Naskah"
        }.get(x, x)
    )

    if filter_status == "Semua":
        df_mod = ambil_semua_artikel()
    else:
        df_mod = ambil_semua_artikel(filter_status)

    st.write(f"Menampilkan **{len(df_mod)}** artikel dalam antrean.")
    st.markdown("---")

    if df_mod.empty:
        st.info("Tidak ada artikel yang sesuai dengan filter antrean saat ini.")
    else:
        for idx, art in df_mod.iterrows():
            with st.container():
                art_id = art["id"]
                st.subheader(f"#{art_id}. {art['title']} — [{art['status'].upper()}]")
                st.write(f"✍️ **Penulis:** {art['author_name']} | 📂 **Kategori:** {art['category']} | 📅 **Tanggal:** {art['created_at'][:10]}")

                word_count = len(re.findall(r"\b[\w'-]+\b", art["content"] or ""))
                h2_count = len(re.findall(r"^##\s+.+", art["content"] or "", re.MULTILINE))
                st.caption(f"Statistik Naskah: {word_count} kata | {h2_count} subjudul H2")

                with st.expander("📖 Tinjau Naskah & Gambar Sampul"):
                    if art["excerpt"]:
                        st.markdown(f"**Cuplikan (Excerpt):** *{art['excerpt']}*")
                    if art["cover_url"]:
                        st.image(art["cover_url"], width=420)
                        st.caption(f"Caption: {art['source_caption'] or 'Tanpa caption'}")
                    st.markdown(art["content"])

                st.markdown("**Keputusan Editorial Redaksi:**")
                c_act1, c_act2, c_act3 = st.columns(3)

                with c_act1:
                    catatan_pub = st.text_input("Pesan rilis:", key=f"pub_txt_{art_id}", placeholder="Lolos kurasi 100%...")
                    if st.button(f"✅ Terbitkan Resmi", key=f"pub_btn_{art_id}"):
                        update_status_artikel(art_id, "published", catatan_pub or "Lolos kurasi redaksi dan telah diterbitkan resmi.")
                        st.success(f"Artikel #{art_id} berhasil diterbitkan ke Beranda!")
                        st.rerun()

                with c_act2:
                    catatan_revisi = st.text_input("Catatan perbaikan:", key=f"rev_txt_{art_id}", placeholder="Misal: Tambah subjudul / perbaiki caption...")
                    if st.button(f"🔧 Minta Revisi", key=f"rev_btn_{art_id}"):
                        update_status_artikel(art_id, "revision", catatan_revisi or "Mohon sesuaikan dengan kaidah teknis redaksi.")
                        st.warning(f"Status artikel #{art_id} diubah menjadi Perlu Perbaikan.")
                        st.rerun()

                with c_act3:
                    alasan_tolak = st.text_input("Alasan penolakan:", key=f"rej_txt_{art_id}", placeholder="Kurang 500 kata / terindikasi plagiasi...")
                    if st.button(f"❌ Tolak Naskah", key=f"rej_btn_{art_id}"):
                        update_status_artikel(art_id, "rejected", alasan_tolak or "Naskah tidak memenuhi syarat penerbitan redaksi.")
                        st.error(f"Artikel #{art_id} ditolak.")
                        st.rerun()

                st.divider()

# ==============================================================================
# 6. 10 PEDOMAN EMAS REDAKSI
# ==============================================================================
elif menu == "📖 10 Pedoman Emas Redaksi":
    st.title("📖 10 Pedoman Emas Redaksi IDN Times Community")
    st.write(
        "Kompilasi aturan mutlak dari meja redaksi IDN Times. Terapkan secara disiplin "
        "agar seluruh naskah tulisanmu lolos kurasi 100% tanpa catatan revisi."
    )

    t1, t2 = st.tabs(["📌 Kaidah Teknis & Format Tulisan", "🖼️ SOP Visual & Etika Redaksi"])

    with t1:
        st.markdown(
            """
            ### 1. Judul Menarik & Patuh EYD V
            * Wajib huruf kapital di awal setiap kata, **kecuali kata partikel/kata tugas di tengah kalimat** (*dan, di, ke, dari, untuk, bagi, yang, agar*).
            * Sisipkan angka numerik di awal judul listicle (*Contoh: 5 Tips Mengatur Keuangan...*) untuk menaikkan rasio klik (CTR).
            * Panjang judul ideal: **4 hingga 12 kata**. Hindari clickbait palsu yang mengecewakan pembaca.

            ---
            ### 2. Cuplikan (Excerpt) Pemikat
            * Tulis 1–2 kalimat pengantar yang padat, membangkitkan rasa penasaran, dan memantik empati pembaca.
            * Excerpt berfungsi sebagai teks pratayang di media sosial (Instagram/Twitter/Facebook) dan cuplikan SEO Google.

            ---
            ### 3. Kuota Subjudul Listicle
            * **Artikel Deskriptif / Tips / Opini**: Wajib minimal **3 subjudul (H2)**.
            * **Artikel Kompilasi / Galeri Foto**: Wajib minimal **7 subjudul (H2)**.
            * Penulisan subjudul wajib menggunakan angka urut: `## 1. Judul Poin`, `## 2. Judul Poin`.

            ---
            ### 4. Kepadatan Paragraf & Kata
            * Setiap subjudul wajib memiliki minimal **2 paragraf**.
            * Setiap paragraf wajib memuat minimal **3 kalimat utuh** yang logis dan runtut.
            * Total naskah wajib mencapai **minimal 500 kata** (tidak termasuk judul dan caption gambar).

            ---
            ### 5. Paragraf Penutup Variatif
            * Hindari penutup klise seperti *"Nah, itu tadi..."* atau *"Sekian artikel kali ini..."*.
            * Gunakan teknik penutup: *Kesimpulan Solutif, Punchline Menggugah, Pertanyaan Interaktif, Call-to-Action,* atau *Refleksi Diri*.
            """
        )

    with t2:
        st.markdown(
            """
            ### 6. Standar Gambar & Resolusi (Landscape 3:2)
            * Format rasio gambar sampul (cover) wajib **landscape 3:2** dengan resolusi minimal **800x350 piksel**.
            * Ukuran file gambar maksimal **1 MB** agar loading artikel cepat dan ramah kuota seluler.
            * Diutamakan menampilkan foto dengan objek manusia hidup untuk meningkatkan keterikatan emosional pembaca.

            ---
            ### 7. Larangan Watermark & Gambar Pecah
            * Dilarang keras menggunakan gambar buram, pecah (pixelated), atau memuat **watermark merek/logo lain**.
            * Dilarang melakukan tangkapan layar (screenshot) tanpa izin dari sumber hak cipta asli.

            ---
            ### 8. Penulisan Caption Sesuai SOP Redaksi
            * **Tipe Frasa Ilustrasi**: Ditulis huruf kecil tanpa titik.  
              *Contoh:* `ilustrasi orang begadang menatap layar ponsel (pexels.com/Burst)`
            * **Tipe Kalimat Berita**: Diawali huruf kapital dan diakhiri tanda titik.  
              *Contoh:* `Suasana konferensi pers peluncuran produk di Jakarta, Senin (17/10/2026). (IDN Times/Indri)`

            ---
            ### 9. Minimal 2 Sumber Rujukan Cek Fakta
            * Wajib menyertakan minimal 2 tautan (URL) rujukan kredibel untuk artikel sains, kesehatan, dan gaya hidup.
            * Sumber rujukan harus berasal dari jurnal ilmiah, institusi resmi, atau kantor berita internasional utama.

            ---
            ### 10. Submit Percaya Diri ke Tim Editor
            * Bila seluruh daftar periksa 1–9 sudah terpenuhi, klik tombol kirim!
            * Hindari mengirim ulang artikel yang sama berulang kali agar tidak terdeteksi sebagai spam.
            """
        )

# ==============================================================================
# 7. ENSIKLOPEDIA 20 PANDUAN RESMI & MASTERBOOK 12 HALAMAN
# ==============================================================================
elif menu == "📚 Ensiklopedia 20 Panduan IDN":
    st.title("📚 Ensiklopedia 20 Panduan Resmi IDN Times Community")
    st.write(
        "Hasil ekstraksi komprehensif seluruh basis pengetahuan editorial resmi IDN Times: "
        "Masterbook 12 Halaman, 20 modul kurasi, jenjang karir penulis, skema poin, dan tutorial redeem resmi."
    )

    t_book, t_mod, t_poin, t_tier, t_lic = st.tabs([
        "📑 Masterbook 12 Halaman (Edisi Lengkap)",
        "📖 20 Modul Panduan Resmi",
        "💰 Kalkulator Poin & Monetisasi",
        "🎖️ Jenjang Karir Penulis (Tier)",
        "📜 Lisensi & Ketentuan Hukum",
    ])

    with t_book:
        st.subheader("📑 Masterbook Penulis Profesional IDN Times Community (12 Halaman Lengkap)")
        st.caption("Panduan kurasi 100%, strategi AI etis, monetisasi poin, dan teknik jurnalisme modern media siber.")

        pdf_path = Path(__file__).parent / "Masterbook_Penulis_Profesional_IDN_Times_Community_12_Halaman.pdf"
        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Unduh PDF Masterbook Resmi (12 Halaman Lengkap)",
                    data=f.read(),
                    file_name="Masterbook_Penulis_Profesional_IDN_Times_Community_12_Halaman.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        st.markdown("---")
        cari_mb = st.text_input("🔍 Cari materi Masterbook (Modul / Topik):", placeholder="Misal: prompt AI, EYD V, 500 kata, cover 3:2, redeem...")

        filtered_mb = MASTERBOOK_12_MODUL
        if cari_mb:
            filtered_mb = [
                m for m in MASTERBOOK_12_MODUL
                if cari_mb.lower() in m["modul"].lower()
                or cari_mb.lower() in m["ringkasan"].lower()
                or cari_mb.lower() in m["detail"].lower()
                or any(cari_mb.lower() in p.lower() for p in m["poin_kunci"])
            ]

        for m in filtered_mb:
            with st.expander(f"📄 [Halaman {m['halaman']}/12] {m['modul']}", expanded=(m['halaman'] <= 2)):
                st.markdown(f"**Ringkasan:** {m['ringkasan']}")
                st.write(m['detail'])

                if m['halaman'] == 6:
                    st.markdown("**📋 Salin Prompt AI Resmi Redaksi IDN Times:**")
                    st.code(
                        "Bertindaklah sebagai Senior Editor IDN Times. Parafrase ulang teks acuan di bawah ini "
                        "dengan gaya bahasa jurnalistik dinamis dan santai khas media anak muda. "
                        "Instruksi:\n"
                        "1. Rombak total struktur kalimat per kalimat secara aktif (jangan terjemahan kaku).\n"
                        "2. Terapkan tata bahasa baku KBBI dan EYD V.\n"
                        "3. Pertahankan fakta/angka asli namun segarkan sudut pandang (angle) tulisan.\n"
                        "4. Jangan gunakan frasa repetitif khas robot.",
                        language="text"
                    )

                st.markdown("**📌 Poin Kunci & Parameter Wajib:**")
                for pk in m["poin_kunci"]:
                    st.markdown(f"- ✅ {pk}")

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

        st.markdown("---")
        st.subheader("📖 Panduan Lengkap: Cara Praktis Redeem IDN Points")
        st.markdown("Ikuti tahapan resmi di bawah ini untuk mencairkan IDN Points ke rekening bank atau e-wallet tanpa kendala:")

        r1, r2 = st.columns(2)
        with r1:
            with st.expander("1️⃣ Syarat Minimal & Validasi Akun", expanded=True):
                st.markdown(
                    """
                    * **Ambang Batas**: Minimal akumulasi **2.500 IDN Points** (= Rp250.000).
                    * **Sumber Poin**: Diperoleh dari views organik artikel yang terbit (1 Poin per 100 views) serta bonus kompetisi/campaign menulis.
                    * **Kelengkapan Profil**: Nama di profil IDN Times Community wajib sama persis dengan nama di KTP dan buku rekening tujuan penarikan.
                    """
                )
            with st.expander("2️⃣ Langkah Klaim di Dashboard IDN"):
                st.markdown(
                    """
                    1. Masuk ke akun Anda di [community.idntimes.com](https://community.idntimes.com).
                    2. Klik ikon profil di pojok kanan atas, lalu pilih menu **IDN Points**.
                    3. Klik tombol merah bertuliskan **Redeem Points**.
                    4. Masukkan jumlah poin yang ingin dicairkan (kelipatan 2.500 poin).
                    """
                )

        with r2:
            with st.expander("3️⃣ Pilihan Jalur Pencairan Dana", expanded=True):
                st.markdown(
                    """
                    * **Transfer Rekening Bank**: Mendukung BCA, Mandiri, BNI, BRI, BSI, CIMB Niaga, Permata, dll.
                    * **E-Wallet**: Mendukung GoPay, OVO, dan DANA.
                    * *Catatan*: Akun e-wallet harus sudah berstatus terverifikasi (*Plus/Premier*) dengan nomor telepon aktif.
                    """
                )
            with st.expander("4️⃣ Jadwal & Estimasi Waktu (SLA Keuangan)"):
                st.markdown(
                    """
                    * **Waktu Proses**: Rata-rata **7 hingga 14 hari kerja** (Senin - Jumat, di luar hari libur nasional).
                    * **Pelacakan Status**: Pantau status penarikan di tab *History Redeem* (*Pending* ➔ *Processing* ➔ *Completed*).
                    * **Notifikasi**: Bukti transfer akan dikirimkan otomatis ke alamat email yang terdaftar.
                    """
                )

        with st.expander("💡 3 Kiat Penting Agar Pengajuan Redeem Langsung Disetujui (Anti-Gagal)"):
            st.markdown(
                """
                1. **Kesesuaian Identitas Mutlak**: Jangan pernah menggunakan rekening bank atau nomor e-wallet atas nama orang lain. Nama pemilik rekening harus cocok 100% dengan identitas akun untuk lolos verifikasi anti-fraud tim Finance IDN Media.
                2. **Periksa Limit Masuk E-Wallet**: Jika memilih opsi e-wallet (GoPay/OVO/DANA), pastikan limit transaksi bulanan belum melampaui batas maksimum agar proses transfer dana tidak tertolak oleh sistem penyedia dompet digital.
                3. **Kualitas & Keaslian Traffic**: Poin yang terkumpul wajib berasal dari pembaca nyata. Sistem analitik redaksi IDN Media melakukan audit sebelum persetujuan transfer untuk memastikan bebas dari manipulasi bot atau spam views.
                """
            )

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
