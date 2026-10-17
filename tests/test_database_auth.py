"""
Unit test suite untuk database.py, auth.py, dan aturan kurasi EYD V IDMedia.
Menjalankan pengujian fungsional terisolasi tanpa memerlukan akses akun eksternal.
"""

import unittest
from pathlib import Path
import sqlite3

from database import (
    init_db,
    tambah_pengguna,
    cek_pengguna,
    kirim_artikel,
    ambil_artikel_penulis,
    ambil_semua_artikel,
    ambil_artikel_terbit,
    update_status_artikel,
    ambil_statistik_platform,
)
from app import validate_eyd_title


class TestDatabaseAndAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_database_initialization(self):
        """Memverifikasi skema database dan tabel users & articles terbuat."""
        stats = ambil_statistik_platform()
        self.assertIn("total_users", stats)
        self.assertIn("total_articles", stats)
        self.assertGreaterEqual(stats["total_users"], 1)

    def test_user_authentication_flow(self):
        """Memverifikasi penambahan pengguna baru dan pengecekan login."""
        username = "qa_tester_unit"
        email = "qa_tester_unit@idmedia.id"
        password = "qa_secret_pass"

        # Tambah pengguna baru
        sukses, pesan = tambah_pengguna(username, email, password, role="penulis", full_name="QA Unit Tester")
        # Jika sudah ada dari run sebelumnya, abaikan integritas
        if not sukses:
            self.assertIn("sudah", pesan)

        # Cek login valid
        user = cek_pengguna(username, password)
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], username)
        self.assertEqual(user["role"], "penulis")

        # Cek login gagal (password salah)
        user_invalid = cek_pengguna(username, "salah_password")
        self.assertIsNone(user_invalid)

    def test_article_submission_and_status_update(self):
        """Memverifikasi alur pengiriman naskah artikel ke database dan pembaruan status oleh editor."""
        title = "5 Fakta Ilmiah Pengujian Perangkat Lunak untuk Pemula"
        content = "## 1. Subjudul Pertama\nNarasi penjelasan minimal tiga kalimat yang runtut dan informatif."
        excerpt = "Ulasan lengkap seputar pengujian perangkat lunak modern."

        art_id = kirim_artikel(
            author_id=1,
            author_name="QA Unit Tester",
            title=title,
            content=content,
            excerpt=excerpt,
            category="Tech"
        )
        self.assertIsInstance(art_id, int)
        self.assertGreater(art_id, 0)

        # Status awal harus 'pending'
        all_pending = ambil_semua_artikel("pending")
        self.assertTrue(any(row["id"] == art_id for _, row in all_pending.iterrows()))

        # Editor memperbarui status menjadi 'published'
        update_sukses = update_status_artikel(art_id, "published", "Lolos uji unit.")
        self.assertTrue(update_sukses)

        # Verifikasi masuk ke artikel terbit
        df_terbit = ambil_artikel_terbit("Tech")
        self.assertTrue(any(row["id"] == art_id for _, row in df_terbit.iterrows()))

    def test_eyd_title_validator(self):
        """Memverifikasi logika validasi kapitalisasi huruf judul EYD V."""
        # Judul benar (partikel kecil di tengah)
        ok, issues = validate_eyd_title("5 Tips Mengatur Keuangan untuk Gen Z agar Cepat Mandiri")
        self.assertTrue(ok)
        self.assertEqual(len(issues), 0)

        # Judul salah (kata pertama huruf kecil)
        ok_wrong1, issues1 = validate_eyd_title("rahasia sukses menulis artikel listicle")
        self.assertFalse(ok_wrong1)
        self.assertTrue(any("wajib diawali huruf kapital" in s for s in issues1))

        # Judul salah (partikel di tengah huruf kapital)
        ok_wrong2, issues2 = validate_eyd_title("5 Tips Mengatur Keuangan Untuk Gen Z Agar Cepat Mandiri")
        self.assertFalse(ok_wrong2)
        self.assertTrue(any("sebaiknya ditulis huruf kecil" in s for s in issues2))


if __name__ == "__main__":
    unittest.main()
