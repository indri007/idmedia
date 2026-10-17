import re

SECTION_PATTERNS = {
    "Abstrak": r"\b(abstract|abstrak)\b",
    "Pendahuluan": r"\b(introduction|pendahuluan|latar belakang)\b",
    "Metode": r"\b(methods?|methodology|metodologi|metode penelitian)\b",
    "Hasil": r"\b(results?|hasil penelitian|temuan)\b",
    "Pembahasan": r"\b(discussion|pembahasan)\b",
    "Kesimpulan": r"\b(conclusion|conclusions|kesimpulan)\b",
    "Daftar pustaka": r"\b(references|bibliography|daftar pustaka)\b",
}

def finding(category, severity, location, issue, recommendation):
    return {
        "kategori": category, "prioritas": severity, "lokasi": location,
        "temuan": issue, "saran": recommendation,
    }

def audit_document(document):
    findings = []
    pages = document["pages"]
    text = "\n".join(p["text"] for p in pages)
    lower = text.lower()

    for section, pattern in SECTION_PATTERNS.items():
        if not re.search(pattern, lower):
            findings.append(finding(
                "Struktur", "Sedang", "Dokumen",
                f"Bagian {section} tidak terdeteksi.",
                "Periksa apakah bagian wajib tersedia dan memakai judul yang dapat dikenali."
            ))

    abstract_match = re.search(
        r"\b(abstract|abstrak)\b(.*?)(?=\n\s*(introduction|pendahuluan|keywords|kata kunci)\b|\Z)",
        text, re.I | re.S
    )
    if abstract_match:
        words = re.findall(r"\b[\w'-]+\b", abstract_match.group(2))
        if len(words) < 100:
            findings.append(finding(
                "Struktur", "Rendah", "Abstrak",
                f"Abstrak terdeteksi hanya sekitar {len(words)} kata.",
                "Periksa batas kata abstrak pada pedoman jurnal target; batas tiap jurnal berbeda."
            ))

    # DOCX: gunakan nama style heading jika tersedia.
    for p in pages:
        if p.get("style", "").lower().startswith("heading"):
            continue
        if p["text"].isupper() and 3 <= len(p["text"].split()) <= 12:
            findings.append(finding(
                "Format", "Rendah", p["location"],
                "Teks kapital penuh mungkin merupakan heading.",
                "Gunakan style heading Word yang konsisten agar struktur mudah dinavigasi."
            ))

    if document.get("tables") is not None:
        if not document["tables"]:
            findings.append(finding(
                "Tabel", "Rendah", "Dokumen",
                "Tidak ada tabel yang terdeteksi pada DOCX.",
                "Jika penelitian membutuhkan tabel, pastikan tabel ada, diberi nomor, judul, dan dirujuk di teks."
            ))
        for table in document["tables"]:
            if not table["rows"] or len(table["rows"][0]) < 2:
                findings.append(finding(
                    "Tabel", "Rendah", f"Tabel {table['table']}",
                    "Tabel mungkin tidak memiliki struktur kolom yang jelas.",
                    "Periksa header, satuan, catatan kaki, dan sumber tabel."
                ))

    # Pemeriksaan nilai p yang jelas perlu diverifikasi; bukan penghitungan ulang.
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"\bp\s*[=<]\s*0[.,]0\b", line, re.I):
            findings.append(finding(
                "Statistik", "Tinggi", f"Baris teks {i}",
                "Nilai p tampak ditulis sebagai p = 0.0... atau p < 0.0....",
                "Cocokkan dengan output analisis asli dan pedoman pelaporan statistik. Jangan ubah angka tanpa verifikasi."
            ))
        if re.search(r"\bp\s*=\s*0[.,]0{3,}\b", line, re.I):
            findings.append(finding(
                "Statistik", "Tinggi", f"Baris teks {i}",
                "Nilai p nol persis terdeteksi.",
                "Nilai p biasanya dilaporkan sebagai batas, misalnya p < .001, bila sesuai output dan pedoman jurnal."
            ))

    # Cari ukuran sampel; bandingkan hanya jika beberapa pola jelas ditemukan.
    sample_sizes = re.findall(
        r"\b(?:n|N)\s*=\s*(\d{1,7})\b", text
    )
    distinct_n = sorted(set(sample_sizes))
    if len(distinct_n) > 1:
        findings.append(finding(
            "Statistik", "Sedang", "Dokumen",
            f"Ditemukan beberapa ukuran sampel eksplisit: {', '.join(distinct_n)}.",
            "Periksa apakah angka merujuk ke tahap atau kelompok berbeda. Perbedaan tidak selalu merupakan kesalahan."
        ))

    if re.search(r"(\$[^$\n]{1,150}\$|\\begin\{equation\}|∑|∫|√|≤|≥|≈)", text):
        findings.append(finding(
            "Rumus", "Rendah", "Dokumen",
            "Simbol atau pola persamaan terdeteksi.",
            "Verifikasi definisi simbol, satuan, penomoran persamaan, dan konsistensi notasi secara manual."
        ))

    # Pemeriksaan gaya akademik berbasis aturan, bukan grammar checker penuh.
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if len(stripped.split()) > 45:
            findings.append(finding(
                "Bahasa", "Rendah", f"Baris teks {i}",
                "Kalimat atau baris teks sangat panjang.",
                "Pertimbangkan memecah kalimat dan memperjelas subjek, klaim, serta hubungan antaride."
            ))
        if re.search(r"\b(very very|sangat sangat|in order to in order to)\b", stripped, re.I):
            findings.append(finding(
                "Bahasa", "Rendah", f"Baris teks {i}",
                "Repetisi frasa terdeteksi.",
                "Periksa pengulangan kata atau frasa dan sederhanakan jika tidak menambah makna."
            ))

    if not findings:
        findings.append(finding(
            "Pemeriksaan awal", "Rendah", "Dokumen",
            "Tidak ada masalah yang terdeteksi oleh aturan dasar.",
            "Tetap lakukan telaah ilmiah, statistik, bahasa, dan referensi secara menyeluruh."
        ))
    return findings

def audit_text(text: str):
    """API lama agar tes MVP tetap kompatibel."""
    doc = {"pages": [{"location": "Dokumen", "text": text}], "tables": None}
    return [
        {
            "kategori": x["kategori"], "tingkat": x["prioritas"],
            "temuan": x["temuan"], "saran": x["saran"]
        }
        for x in audit_document(doc)
    ]
