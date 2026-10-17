import json
from datetime import datetime, timezone
import streamlit as st

from src.document_parser import extract_document
from src.quality_rules import audit_document
from src.references import audit_references
from src.reporting import make_docx_report, make_pdf_report

st.set_page_config(page_title="Scientific Manuscript QA", page_icon="📑", layout="wide")
st.title("Scientific Manuscript Quality Assurance")
st.caption("Audit awal struktur, referensi, statistik, rumus, dan bahasa akademik.")

st.warning(
    "Temuan otomatis adalah indikator untuk ditinjau, bukan bukti kesalahan, "
    "validasi ilmiah menyeluruh, atau jaminan penerimaan jurnal."
)

uploaded = st.file_uploader("Unggah manuskrip PDF/DOCX (maks. 175 halaman PDF; 50 MB)", type=["pdf", "docx"])
provider = st.selectbox("Penyedia metadata referensi", ["Crossref", "OpenAlex"])
limit = st.slider("Maksimum referensi yang diperiksa melalui API", 1, 30, 10)
run = st.button("Jalankan audit", type="primary", disabled=uploaded is None)

if run and uploaded:
    try:
        data = uploaded.getvalue()
        document = extract_document(uploaded.name, data)
        findings = audit_document(document)
        full_text = "\n".join(p["text"] for p in document["pages"])

        with st.spinner("Memeriksa metadata referensi. API eksternal mungkin membutuhkan waktu..."):
            references = audit_references(full_text, provider=provider, limit=limit)

        report = {
            "file": uploaded.name,
            "waktu_utc": datetime.now(timezone.utc).isoformat(),
            "format": document["format"],
            "jumlah_halaman_pdf": document["page_count"],
            "jumlah_gambar_terdeteksi": document["images"],
            "jumlah_temuan": len(findings),
            "temuan": findings,
            "referensi": references,
            "catatan": "Pemeriksaan otomatis bersifat indikatif dan perlu diverifikasi.",
        }
        st.session_state["smqa_report"] = report
        st.session_state["smqa_findings"] = findings
        st.session_state["smqa_refs"] = references
        st.session_state["smqa_filename"] = uploaded.name
        st.session_state["smqa_document"] = document
    except Exception as exc:
        st.error(f"Audit gagal: {exc}")

if "smqa_report" in st.session_state:
    report = st.session_state["smqa_report"]
    findings = st.session_state["smqa_findings"]
    references = st.session_state["smqa_refs"]

    a, b, c = st.columns(3)
    a.metric("Temuan", len(findings))
    b.metric("Referensi diperiksa", len(references))
    c.metric("Gambar terdeteksi", report["jumlah_gambar_terdeteksi"])

    st.subheader("Temuan revisi")
    for i, item in enumerate(findings, 1):
        with st.expander(f"{i}. [{item['prioritas']}] {item['kategori']} — {item['lokasi']}", expanded=item["prioritas"] == "Tinggi"):
            st.write("**Temuan:**", item["temuan"])
            st.write("**Saran:**", item["saran"])

    st.subheader("Pencocokan metadata referensi")
    if not references:
        st.info("Tidak ada entri referensi yang terdeteksi. Periksa heading Daftar Pustaka.")
    for i, ref in enumerate(references, 1):
        with st.expander(f"{i}. {ref.get('reference', '')[:160]}"):
            st.write("Penyedia:", ref.get("provider"))
            st.write("Kandidat cocok:", ref.get("match"))
            st.write("Judul kandidat:", ref.get("title", "Tidak tersedia"))
            st.write("DOI:", ref.get("doi", "Tidak tersedia"))
            if ref.get("error"):
                st.warning("API tidak dapat diakses: " + ref["error"])
            st.caption("Hasil pencarian metadata adalah kandidat dan harus dicocokkan dengan referensi asli.")

    st.subheader("Unduh laporan")
    stem = st.session_state["smqa_filename"].rsplit(".", 1)[0]
    st.download_button(
        "Unduh JSON",
        json.dumps(report, ensure_ascii=False, indent=2),
        file_name=f"{stem}_audit.json",
        mime="application/json",
    )
    st.download_button(
        "Unduh laporan Word",
        make_docx_report(st.session_state["smqa_filename"], findings, references),
        file_name=f"{stem}_audit.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    st.download_button(
        "Unduh laporan PDF",
        make_pdf_report(st.session_state["smqa_filename"], findings, references),
        file_name=f"{stem}_audit.pdf",
        mime="application/pdf",
    )

st.divider()
st.caption(
    "Privasi: teks manuskrip diproses lokal oleh aplikasi, tetapi potongan entri referensi "
    "dikirim ke API Crossref/OpenAlex saat fitur pencocokan diaktifkan. Jangan unggah naskah rahasia "
    "ke deployment publik tanpa kebijakan privasi dan kontrol akses."
)
