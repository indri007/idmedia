"""
IDMedia Supabase Client Module
Menyediakan koneksi opsional ke basis data awan Supabase.
Jika secrets SUPABASE_URL & SUPABASE_KEY belum diisi, sistem otomatis menggunakan SQLite lokal.
"""

import streamlit as st

def dapat_klien():
    """Mengembalikan klien Supabase jika credentials tersedia di secrets, atau None."""
    try:
        supabase_url = st.secrets.get("SUPABASE_URL")
        supabase_key = st.secrets.get("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            return None

        from supabase import create_client
        return create_client(supabase_url, supabase_key)
    except Exception:
        return None

# Klien Supabase (akan bernilai None jika belum dikonfigurasi)
db = dapat_klien()
