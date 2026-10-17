# Scientific Manuscript QA

Streamlit MVP untuk pemeriksaan awal manuskrip PDF/DOCX.

## Fitur
- Ekstraksi teks PDF dan DOCX
- Batas PDF 175 halaman
- Pemeriksaan struktur dasar, pola sitasi, nilai p, dan istilah kausal
- Unduh laporan JSON
- Tes otomatis dengan pytest

## Menjalankan lokal
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

Temuan bersifat indikatif dan tidak menjamin validitas ilmiah atau penerimaan jurnal.
