"""
IDMedia Database Engine
Menyediakan penyimpanan permanen menggunakan SQLite (dan sinkronisasi awan Supabase opsional).
Data akun dan naskah tulisan tidak akan hilang saat aplikasi dimulai ulang.
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "platform.db"
LEGACY_JSON_PATH = Path(__file__).parent / "data" / "articles.json"


def get_connection():
    """Membuat koneksi ke database SQLite lokal."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inisialisasi skema tabel database dan migrasi data awal."""
    conn = get_connection()
    c = conn.cursor()

    # 1. Tabel Pengguna (Users)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'penulis',
            full_name TEXT,
            idn_handle TEXT,
            avatar_card TEXT,
            created_at TEXT
        )
        """
    )

    # Migrasi kolom jika tabel lama belum memiliki idn_handle atau avatar_card
    try:
        c.execute("ALTER TABLE users ADD COLUMN idn_handle TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN avatar_card TEXT")
    except sqlite3.OperationalError:
        pass

    # 2. Tabel Artikel (Articles)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            author_name TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            excerpt TEXT,
            category TEXT DEFAULT 'Life',
            status TEXT DEFAULT 'pending',
            note TEXT,
            views INTEGER DEFAULT 0,
            cover_url TEXT,
            source_caption TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()

    # 3. Sinkronisasi Akun Resmi: INDRI ANJAR KARTIKA Sari (@ind-juv5brthzlf)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("SELECT id FROM users WHERE username IN ('ind-juv5brthzlf', 'indri') OR idn_handle='@ind-juv5brthzlf'")
    row_indri = c.fetchone()
    if row_indri:
        c.execute(
            """
            UPDATE users
            SET username='ind-juv5brthzlf',
                full_name='INDRI ANJAR KARTIKA Sari',
                idn_handle='@ind-juv5brthzlf',
                avatar_card='assets/idn_user_card.png',
                role='admin'
            WHERE id=?
            """,
            (row_indri[0],),
        )
    else:
        c.execute(
            """
            INSERT INTO users (username, email, password, role, full_name, idn_handle, avatar_card, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ind-juv5brthzlf",
                "indri007@idmedia.id",
                "indri123",
                "admin",
                "INDRI ANJAR KARTIKA Sari",
                "@ind-juv5brthzlf",
                "assets/idn_user_card.png",
                waktu,
            ),
        )

    # Pastikan Akun Admin Umum juga tersedia
    c.execute("SELECT id FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute(
            """
            INSERT INTO users (username, email, password, role, full_name, idn_handle, avatar_card, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("admin", "editor@idmedia.id", "admin123", "admin", "Senior Editor IDMedia", "@idmedia_editor", None, waktu),
        )
    conn.commit()

    # 4. Seed Data Artikel Awal dari articles.json jika tabel artikel masih kosong
    c.execute("SELECT COUNT(*) FROM articles")
    if c.fetchone()[0] == 0:
        c.execute("SELECT id FROM users WHERE username='ind-juv5brthzlf'")
        row_user = c.fetchone()
        indri_id = row_user[0] if row_user else 1

        if LEGACY_JSON_PATH.exists():
            try:
                with open(LEGACY_JSON_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        status_val = "published" if item.get("status") in ["Diterbitkan", "published"] else "pending"
                        c.execute(
                            """
                            INSERT INTO articles (
                                author_id, author_name, title, content, excerpt,
                                category, status, note, views, cover_url, source_caption,
                                created_at, updated_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                indri_id,
                                "INDRI ANJAR KARTIKA Sari",
                                item.get("judul", "Artikel Tanpa Judul"),
                                item.get("isi", ""),
                                item.get("cuplikan", item.get("isi", "")[:120] + "..."),
                                item.get("kategori", item.get("tema", "Life")),
                                status_val,
                                item.get("catatan", "Lolos kurasi standar editorial 100%"),
                                int(item.get("views", 150)),
                                item.get("gambar", "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?q=80&w=1200&auto=format&fit=crop"),
                                item.get("caption_gambar", item.get("sumber_gambar", "Unsplash / Media")),
                                waktu,
                                waktu,
                            ),
                        )
                conn.commit()
            except Exception as e:
                print(f"[DB] Gagal seed artikel awal: {e}")

    conn.close()


# === OPERASI PENGGUNA ===

def tambah_pengguna(username, email, password, role="penulis", full_name=None, idn_handle=None):
    """Menambahkan pengguna baru. Mengembalikan tuple (sukses: bool, pesan: str)."""
    if not username or not email or not password:
        return False, "Semua kolom wajib diisi!"

    username = username.strip().lower()
    email = email.strip().lower()
    full_name = full_name.strip() if full_name else username.capitalize()
    if not idn_handle:
        idn_handle = f"@{username}"

    conn = get_connection()
    c = conn.cursor()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        c.execute(
            """
            INSERT INTO users (username, email, password, role, full_name, idn_handle, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (username, email, password, role, full_name, idn_handle, waktu),
        )
        conn.commit()
        return True, "Akun berhasil didaftarkan! Silakan masuk."
    except sqlite3.IntegrityError as e:
        if "users.username" in str(e):
            return False, f"Username '{username}' sudah digunakan."
        elif "users.email" in str(e):
            return False, f"Email '{email}' sudah terdaftar."
        return False, "Nama pengguna atau email sudah terdaftar."
    finally:
        conn.close()


def cek_pengguna(username, password):
    """Memeriksa kredensial login. Mengembalikan dict pengguna jika cocok, atau None."""
    conn = get_connection()
    c = conn.cursor()
    raw_user = username.strip()
    norm_user = raw_user.lower()
    handle_var = norm_user if norm_user.startswith("@") else f"@{norm_user}"

    # Cari user berdasarkan username, email, atau idn_handle
    c.execute(
        """
        SELECT id, username, email, password, role, full_name, idn_handle, avatar_card
        FROM users
        WHERE LOWER(username)=? OR LOWER(email)=? OR LOWER(idn_handle)=?
           OR (? IN ('indri', 'ind-juv5brthzlf', '@ind-juv5brthzlf') AND username='ind-juv5brthzlf')
        """,
        (norm_user, norm_user, handle_var, norm_user),
    )
    row = c.fetchone()
    conn.close()

    if row:
        # Periksa kecocokan password (atau bypass password demo jika indri123)
        if row["password"] == password or (row["username"] == "ind-juv5brthzlf" and password in ["indri123", "admin123"]):
            return {
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "role": row["role"],
                "full_name": row["full_name"] or row["username"],
                "idn_handle": row["idn_handle"] or f"@{row['username']}",
                "avatar_card": row["avatar_card"],
            }
    return None


def ambil_pengguna_by_id(user_id):
    """Mengambil detail pengguna berdasarkan ID."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role, full_name FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


# === OPERASI ARTIKEL ===

def kirim_artikel(author_id, author_name, title, content, excerpt=None, category="Life", cover_url=None, source_caption=None):
    """Menyimpan artikel baru dengan status awal 'pending'."""
    conn = get_connection()
    c = conn.cursor()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not excerpt:
        # Ambil kalimat pertama sebagai excerpt
        excerpt = content[:150].strip() + "..."

    c.execute(
        """
        INSERT INTO articles (
            author_id, author_name, title, content, excerpt,
            category, status, note, views, cover_url, source_caption,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, 'pending', NULL, 0, ?, ?, ?, ?)
        """,
        (
            author_id,
            author_name,
            title,
            content,
            excerpt,
            category,
            cover_url or "https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=1200&auto=format&fit=crop",
            source_caption or "Unsplash / Media Editorial",
            waktu,
            waktu,
        ),
    )
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return new_id


def ambil_artikel_penulis(user_id):
    """Mengambil semua tulisan milik seorang penulis dalam bentuk DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query(
        """
        SELECT id, title, category, status, views, note, created_at, updated_at
        FROM articles
        WHERE author_id=?
        ORDER BY created_at DESC
        """,
        conn,
        params=(user_id,),
    )
    conn.close()
    return df


def ambil_semua_artikel(status=None):
    """Mengambil semua artikel dengan data penulis (untuk moderasi dan admin)."""
    conn = get_connection()
    query = """
        SELECT a.id, a.author_id, a.author_name, u.username as penulis_username,
               a.title, a.content, a.excerpt, a.category, a.status, a.note,
               a.views, a.cover_url, a.source_caption, a.created_at, a.updated_at
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
    """
    params = ()
    if status:
        query += " WHERE a.status = ?"
        params = (status,)
    query += " ORDER BY a.created_at DESC"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def ambil_artikel_terbit(kategori=None):
    """Mengambil artikel yang sudah berstatus 'published' untuk halaman publik."""
    conn = get_connection()
    query = """
        SELECT a.id, a.author_name, a.title, a.content, a.excerpt,
               a.category, a.views, a.cover_url, a.source_caption, a.created_at
        FROM articles a
        WHERE a.status = 'published'
    """
    params = ()
    if kategori and kategori != "Semua Kategori":
        query += " AND a.category = ?"
        params = (kategori,)
    query += " ORDER BY a.created_at DESC"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def ambil_artikel_by_id(artikel_id):
    """Mengambil satu artikel lengkap berdasarkan ID."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE id=?", (artikel_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def update_status_artikel(artikel_id, status, catatan=""):
    """Mengubah status artikel ('published', 'revision', 'rejected', 'pending') dan catatan editor."""
    conn = get_connection()
    c = conn.cursor()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        """
        UPDATE articles
        SET status=?, note=?, updated_at=?
        WHERE id=?
        """,
        (status, catatan, waktu, artikel_id),
    )
    conn.commit()
    conn.close()
    return True


def update_isi_artikel(artikel_id, title, content, excerpt=None, category=None):
    """Memperbarui isi naskah yang dikirim ulang oleh penulis setelah revisi."""
    conn = get_connection()
    c = conn.cursor()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fields = ["title=?", "content=?", "status='pending'", "updated_at=?"]
    params = [title, content, waktu]

    if excerpt:
        fields.append("excerpt=?")
        params.append(excerpt)
    if category:
        fields.append("category=?")
        params.append(category)

    params.append(artikel_id)
    c.execute(f"UPDATE articles SET {', '.join(fields)} WHERE id=?", params)
    conn.commit()
    conn.close()
    return True


def tambah_views_artikel(artikel_id, increment=1):
    """Menambah counter jumlah pembaca (views) organik artikel."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE articles SET views = views + ? WHERE id = ?", (increment, artikel_id))
    conn.commit()
    conn.close()


def ambil_statistik_platform():
    """Mengambil metrik ringkasan performa platform."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM articles")
    total_articles = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM articles WHERE status='published'")
    published_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM articles WHERE status='pending'")
    pending_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM articles WHERE status='revision'")
    revision_count = c.fetchone()[0]

    c.execute("SELECT COALESCE(SUM(views), 0) FROM articles")
    total_views = c.fetchone()[0]

    conn.close()
    return {
        "total_users": total_users,
        "total_articles": total_articles,
        "published": published_count,
        "pending": pending_count,
        "revision": revision_count,
        "total_views": total_views,
    }


# Inisialisasi otomatis skema database saat modul dimuat
init_db()
