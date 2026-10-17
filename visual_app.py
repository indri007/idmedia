import json
import tempfile
from pathlib import Path

import streamlit as st

from src.visual_quality import inspect_visual, format_report

st.set_page_config(
    page_title="Audit Visual Ilmiah",
    page_icon="🖼️",
    layout="wide",
)

st.title("Audit Visual untuk Publikasi Ilmiah")
st.caption(
    "Pemeriksaan awal gambar, diagram, dan ilustrasi hasil ekspor CorelDRAW. "
    "Hasil bukan jaminan penerimaan jurnal."
)

st.subheader("1. Ukuran cetak")
c1, c2 = st.columns(2)
with c1:
    print_width = st.number_input(
        "Lebar cetak (inci)", min_value=0.1, max_value=30.0,
        value=4.0, step=0.1
    )
with c2:
    print_height = st.number_input(
        "Tinggi cetak (inci)", min_value=0.1, max_value=30.0,
        value=3.0, step=0.1
    )

st.subheader("2. Unggah gambar")
uploaded = st.file_uploader(
    "Pilih file hasil ekspor CorelDRAW atau gambar",
    type=["png", "jpg", "jpeg", "tif", "tiff", "svg", "pdf", "eps"],
)

if uploaded:
    suffix = Path(uploaded.name).suffix.lower()

    with tempfile.TemporaryDirectory() as tmp:
        file_path = Path(tmp) / f"upload{suffix}"
        file_path.write_bytes(uploaded.getvalue())

        result = inspect_visual(
            file_path,
            print_width_in=float(print_width),
            print_height_in=float(print_height),
        )
        result["file"] = uploaded.name

        st.subheader("3. Hasil audit")

        status = result.get("status", "PERLU DITINJAU")
        st.write(f"**Status:** {status}")

        if "width_px" in result:
            st.write(
                f"**Dimensi raster:** {result['width_px']} × "
                f"{result['height_px']} piksel"
            )

        if "effective_dpi" in result:
            st.write(
                f"**Resolusi efektif:** {result['effective_dpi'][0]} × "
                f"{result['effective_dpi'][1]} DPI"
            )

        if "dpi_metadata" in result:
            st.write(f"**Metadata DPI:** {result['dpi_metadata']}")

        findings = result.get("findings", [])
        if findings:
            st.warning("Ada hal yang perlu diperiksa.")
            for finding in findings:
                st.markdown(f"- {finding}")
        else:
            st.success("Tidak ada temuan pada pemeriksaan dasar.")

        st.subheader("4. Rekomendasi")
        st.write(result.get("recommendation", "Periksa hasil secara manual."))

        report = format_report(result)
        st.download_button(
            "Unduh laporan TXT",
            data=report,
            file_name="audit_visual.txt",
            mime="text/plain",
        )
        st.download_button(
            "Unduh laporan JSON",
            data=json.dumps(result, ensure_ascii=False, indent=2),
            file_name="audit_visual.json",
            mime="application/json",
        )

        st.info(
            "Periksa pula keterbacaan font, ketebalan garis, legenda, "
            "ketepatan data, hak penggunaan gambar, dan pedoman jurnal. "
            "Untuk file PDF/EPS, pemeriksaan ini tidak membuktikan bahwa "
            "semua elemen berupa vektor."
        )
else:
    st.info(
        "Ekspor file CDR dari CorelDRAW ke format yang didukung, "
        "kemudian unggah di sini."
    )
