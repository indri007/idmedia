"""
IDMedia Database Proxy
Meneruskan fungsi dari modul database utama untuk kompatibilitas impor.
"""

from database import (
    init_db,
    tambah_pengguna,
    cek_pengguna,
    ambil_pengguna_by_id,
    kirim_artikel,
    ambil_artikel_penulis,
    ambil_semua_artikel,
    ambil_artikel_terbit,
    ambil_artikel_by_id,
    update_status_artikel,
    update_isi_artikel,
    tambah_views_artikel,
    ambil_statistik_platform,
    get_connection,
)

__all__ = [
    "init_db",
    "tambah_pengguna",
    "cek_pengguna",
    "ambil_pengguna_by_id",
    "kirim_artikel",
    "ambil_artikel_penulis",
    "ambil_semua_artikel",
    "ambil_artikel_terbit",
    "ambil_artikel_by_id",
    "update_status_artikel",
    "update_isi_artikel",
    "tambah_views_artikel",
    "ambil_statistik_platform",
    "get_connection",
]
