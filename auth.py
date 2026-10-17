"""
IDMedia Authentication & Session Management Module
Mengelola autentikasi pengguna, hak akses berbasis peran (Role-Based Access Control),
serta integrasi sesi Streamlit.
"""

import streamlit as st
from database import tambah_pengguna, cek_pengguna


import json
from pathlib import Path

IDN_CONFIG_FILE = Path(__file__).parent / "data" / "idn_account.json"
IDN_CARD_IMG = Path(__file__).parent / "assets" / "idn_user_card.png"


def inisialisasi_sesi():
    """Memastikan variabel sesi dasar sudah terdefinisi dan menghubungkan akun resmi IDN."""
    if "sudah_login" not in st.session_state:
        # Otomatis hubungkan akun resmi jika berkas konfigurasi akun IDN ada
        if IDN_CONFIG_FILE.exists():
            try:
                with open(IDN_CONFIG_FILE, "r", encoding="utf-8") as f:
                    acc = json.load(f)
                    st.session_state.sudah_login = True
                    st.session_state.user_id = 2
                    st.session_state.username = acc.get("username", "ind-juv5brthzlf")
                    st.session_state.idn_handle = acc.get("idn_handle", "@ind-juv5brthzlf")
                    st.session_state.email = acc.get("email", "indri007@idmedia.id")
                    st.session_state.peran = acc.get("role", "admin")
                    st.session_state.full_name = acc.get("full_name", "INDRI ANJAR KARTIKA Sari")
                    st.session_state.is_idn_connected = True
                    st.session_state.client_id = acc.get("cognito", {}).get("client_id", "2lnitap1rj2b3mb00iifvnj3ni")
                    st.session_state.device_id = acc.get("session", {}).get("device_id", "01a149ab-1869-7792-9d3a-d18f1ddf5200")
                    return
            except Exception:
                pass

        st.session_state.sudah_login = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.idn_handle = None
        st.session_state.peran = "tamu"
        st.session_state.full_name = "Tamu Pembaca"
        st.session_state.is_idn_connected = False
        st.session_state.client_id = None
        st.session_state.device_id = None


def atur_sesi(user_data):
    """Menyimpan data pengguna ke dalam st.session_state setelah login berhasil."""
    inisialisasi_sesi()
    st.session_state.sudah_login = True
    st.session_state.user_id = user_data["id"]
    st.session_state.username = user_data["username"]
    st.session_state.idn_handle = user_data.get("idn_handle", f"@{user_data['username']}")
    st.session_state.email = user_data.get("email", "")
    st.session_state.peran = user_data.get("role", "penulis")
    st.session_state.full_name = user_data.get("full_name", user_data["username"].capitalize())
    st.session_state.is_idn_connected = (user_data["username"] == "ind-juv5brthzlf" or "@ind-juv5brthzlf" in st.session_state.idn_handle)
    st.session_state.client_id = "2lnitap1rj2b3mb00iifvnj3ni" if st.session_state.is_idn_connected else None


def keluar_sesi():
    """Menghapus sesi login dan mereset status pengguna menjadi tamu."""
    for key in ["sudah_login", "user_id", "username", "idn_handle", "email", "peran", "full_name", "is_idn_connected", "client_id", "device_id"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.sudah_login = False
    st.session_state.peran = "tamu"
    st.rerun()


def tombol_keluar():
    """Menampilkan tombol keluar di sidebar."""
    inisialisasi_sesi()
    if st.session_state.sudah_login:
        if st.sidebar.button("🚪 Keluar Akun", use_container_width=True):
            keluar_sesi()


def render_user_badge_sidebar():
    """Menampilkan kartu profil pengguna aktif di sidebar dengan status akun IDN resmi."""
    inisialisasi_sesi()
    if st.session_state.sudah_login:
        is_admin = st.session_state.peran == "admin"
        is_connected = st.session_state.get("is_idn_connected", False)

        badge_role = "👑 Senior Editor" if is_admin else "✍️ Community Writer"
        badge_color = "#dc2626" if is_admin else "#2563eb"
        handle_display = st.session_state.get("idn_handle", f"@{st.session_state.username}")

        # Tampilkan QR card jika akun terhubung resmi
        if is_connected and IDN_CARD_IMG.exists():
            st.sidebar.image(str(IDN_CARD_IMG), caption="Kartu Penulis Resmi IDN Media", use_container_width=True)

        st.sidebar.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 12px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.75rem; color: #10b981; font-weight: 700;">● TERHUBUNG RESMI</span>
                    <span style="font-size: 0.7rem; color: #94a3b8;">IDN App</span>
                </div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-top: 4px; color: #ffffff;">{st.session_state.full_name}</div>
                <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 600;">{handle_display}</div>
                <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 8px;">
                    <span style="background: {badge_color}; color: #ffffff; padding: 2px 8px; border-radius: 999px; font-size: 0.7rem; font-weight: 600;">
                        {badge_role}
                    </span>
                    <span style="background: #059669; color: #ffffff; padding: 2px 8px; border-radius: 999px; font-size: 0.7rem; font-weight: 600;">
                        🏅 Verified Writer
                    </span>
                </div>
                <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 8px; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 6px;">
                    Client ID: <code>2lnitap1rj2b...</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        tombol_keluar()
    else:
        st.sidebar.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 12px; margin-bottom: 12px;">
                <div style="font-size: 0.8rem; color: #94a3b8;">Status Pengguna:</div>
                <div style="font-weight: 700; font-size: 0.95rem;">👤 Mode Pembaca Publik</div>
                <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 4px;">Masuk untuk mulai menulis naskah atau mengelola redaksi.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def halaman_login(pesan_peringatan=None):
    """Menampilkan antarmuka login dan registrasi dengan gaya estetika Material 3."""
    inisialisasi_sesi()
    st.markdown("### 🔐 Autentikasi Pengguna IDMedia")

    if pesan_peringatan:
        st.info(pesan_peringatan)

    tab_login, tab_daftar, tab_demo = st.tabs(["🔑 Masuk Akun", "📝 Daftar Penulis Baru", "⚡ Uji Coba Cepat (Demo)"])

    with tab_login:
        st.subheader("Masuk ke Akun Anda")
        username = st.text_input("Nama Pengguna atau Email", key="auth_login_user")
        password = st.text_input("Kata Sandi", type="password", key="auth_login_pass")

        if st.button("🚀 Masuk Sekarang", type="primary", use_container_width=True, key="btn_login_submit"):
            if username and password:
                user = cek_pengguna(username, password)
                if user:
                    atur_sesi(user)
                    st.success(f"Selamat datang kembali, **{user['full_name']}**! 🎉")
                    st.rerun()
                else:
                    st.error("Kombinasi nama pengguna/email dan kata sandi tidak ditemukan.")
            else:
                st.warning("Silakan lengkapi nama pengguna dan kata sandi.")

    with tab_daftar:
        st.subheader("Registrasi Penulis Komunitas")
        st.caption("Daftarkan diri Anda untuk mulai mempublikasikan karya dan meraih penghasilan poin.")
        nama_lengkap = st.text_input("Nama Lengkap (Sesuai KTP)", key="auth_reg_fullname", placeholder="Contoh: Indri Kartika")
        username_baru = st.text_input("Nama Pengguna (Username)", key="auth_reg_user", placeholder="misal: indrikartika")
        email_baru = st.text_input("Alamat Email Aktif", key="auth_reg_email", placeholder="nama@email.com")
        sandi_baru = st.text_input("Kata Sandi Akun", type="password", key="auth_reg_pass")
        peran_pilihan = st.selectbox("Daftar Sebagai Peran:", ["penulis", "admin"], format_func=lambda x: "✍️ Penulis Kontributor" if x == "penulis" else "👑 Editor Redaksi (Admin)")

        if st.button("✨ Buat Akun Baru", type="primary", use_container_width=True, key="btn_reg_submit"):
            if nama_lengkap and username_baru and email_baru and sandi_baru:
                sukses, pesan = tambah_pengguna(username_baru, email_baru, sandi_baru, role=peran_pilihan, full_name=nama_lengkap)
                if sukses:
                    st.success(pesan)
                    # Otomatis login
                    user_baru = cek_pengguna(username_baru, sandi_baru)
                    if user_baru:
                        atur_sesi(user_baru)
                        st.rerun()
                else:
                    st.error(pesan)
            else:
                st.warning("Mohon isi seluruh data pendaftaran.")

    with tab_demo:
        st.subheader("Akun Pengujian Instan")
        st.write("Klik salah satu tombol di bawah untuk langsung mencoba platform tanpa perlu mengisi formulir:")
        c_adm, c_pen = st.columns(2)
        with c_adm:
            if st.button("👑 Masuk sebagai Editor (Admin)", use_container_width=True):
                user_admin = cek_pengguna("admin", "admin123")
                if user_admin:
                    atur_sesi(user_admin)
                    st.success("Berhasil masuk sebagai Senior Editor!")
                    st.rerun()
        with c_pen:
            if st.button("✍️ Masuk sebagai Penulis (Indri)", use_container_width=True):
                user_penulis = cek_pengguna("indri", "indri123")
                if user_penulis:
                    atur_sesi(user_penulis)
                    st.success("Berhasil masuk sebagai Penulis Komunitas!")
                    st.rerun()


def cek_login(pesan=None):
    """
    Memeriksa apakah sesi pengguna sudah aktif.
    Jika belum, menampilkan form login dan menghentikan eksekusi kode di bawahnya.
    """
    inisialisasi_sesi()
    if not st.session_state.sudah_login:
        halaman_login(pesan_peringatan=pesan or "🔒 Anda perlu masuk ke akun terlebih dahulu untuk mengakses halaman ini.")
        st.stop()


def cek_peran_admin():
    """Memeriksa apakah pengguna memiliki hak akses sebagai admin/editor."""
    inisialisasi_sesi()
    if not st.session_state.sudah_login:
        halaman_login("🔒 Silakan masuk sebagai Editor/Admin untuk mengakses Panel Moderasi.")
        st.stop()
    if st.session_state.peran != "admin":
        st.error("⛔ Akses Terbatas: Halaman ini hanya diperuntukkan bagi Tim Editor Redaksi.")
        st.info("Tip: Anda sedang masuk sebagai **Penulis**. Anda dapat keluar dan masuk menggunakan akun admin.")
        if st.button("🚪 Keluar & Ganti Akun"):
            keluar_sesi()
        st.stop()
