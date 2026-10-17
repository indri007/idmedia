"""Audit awal kualitas gambar ilmiah untuk manuskrip jurnal.

Tidak menjamin penerimaan jurnal. Selalu cocokkan dengan author guidelines.
CorelDRAW CDR harus diekspor dahulu ke SVG, PDF, EPS, TIFF, atau PNG.
"""
from __future__ import annotations

import io
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}
VECTOR_EXTENSIONS = {".svg", ".pdf", ".eps"}
SUPPORTED_EXTENSIONS = RASTER_EXTENSIONS | VECTOR_EXTENSIONS


def _svg_audit(data: bytes) -> dict:
    """Periksa SVG dasar; menolak deklarasi DTD/entity."""
    text = data.decode("utf-8-sig", errors="strict")

    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.IGNORECASE):
        raise ValueError("SVG mengandung deklarasi DTD/entity yang tidak diizinkan.")

    root = ET.fromstring(text)
    if root.tag.split("}")[-1].lower() != "svg":
        raise ValueError("Dokumen XML bukan SVG.")

    viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    width = root.attrib.get("width", "")
    height = root.attrib.get("height", "")

    findings = []
    if not viewbox:
        findings.append("SVG tidak memiliki viewBox; periksa skalabilitas.")

    if not width or not height:
        findings.append("Dimensi width/height tidak lengkap.")

    # SVG dapat merujuk gambar/font eksternal; tinjau sebelum publikasi.
    if any(
        key.lower().endswith("href") and value.strip()
        and not value.strip().startswith("#")
        for element in root.iter()
        for key, value in element.attrib.items()
    ):
        findings.append(
            "Ada referensi eksternal pada SVG; pastikan aset tertanam "
            "atau tersedia dan berlisensi."
        )

    return {
        "format": "SVG (vektor)",
        "width": width or "tidak tercantum",
        "height": height or "tidak tercantum",
        "viewBox": viewbox or "tidak tercantum",
        "findings": findings,
    }


def inspect_visual(
    path: str | Path,
    print_width_in: float = 4.0,
    print_height_in: float = 3.0,
) -> dict:
    """Audit awal gambar untuk publikasi; mengembalikan hasil terstruktur."""
    file_path = Path(path)
    result = {
        "file": file_path.name,
        "extension": file_path.suffix.lower(),
        "bytes": 0,
        "status": "PERLU DITINJAU",
        "findings": [],
        "recommendation": "",
    }

    if not file_path.is_file():
        result["status"] = "ERROR"
        result["findings"].append("File tidak ditemukan.")
        return result

    result["bytes"] = file_path.stat().st_size
    if result["bytes"] == 0:
        result["status"] = "ERROR"
        result["findings"].append("File kosong.")
        return result

    ext = file_path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        result["status"] = "TIDAK DIDUKUNG"
        result["findings"].append(
            "Gunakan SVG/PDF/EPS untuk vektor atau PNG/TIFF/JPEG untuk raster. "
            "File CDR harus diekspor dari CorelDRAW terlebih dahulu."
        )
        return result

    try:
        if ext == ".svg":
            details = _svg_audit(file_path.read_bytes())
            result.update(details)
            result["recommendation"] = (
                "Periksa font, garis, label, lisensi, referensi eksternal, "
                "dan hasil ekspor pada ukuran cetak."
            )

        elif ext == ".pdf":
            # PyMuPDF tersedia pada proyek ini untuk pemrosesan PDF.
            import fitz

            doc = fitz.open(file_path)
            if doc.page_count < 1:
                raise ValueError("PDF tidak memiliki halaman.")
            page = doc[0]
            result["format"] = "PDF"
            result["pages"] = doc.page_count
            result["page_size_pt"] = [
                round(page.rect.width, 2), round(page.rect.height, 2)
            ]
            result["findings"].append(
                "Periksa apakah teks/garis tetap vektor dan font tertanam. "
                "PDF dapat berisi gambar raster."
            )
            result["recommendation"] = (
                "Buka PDF hasil ekspor dan periksa font, transparansi, "
                "ketebalan garis, ukuran halaman, serta elemen yang terpotong."
            )
            doc.close()

        elif ext == ".eps":
            result["format"] = "EPS"
            result["findings"].append(
                "Audit otomatis hanya memeriksa keberadaan file; "
                "render dan periksa EPS secara visual."
            )
            result["recommendation"] = (
                "Buka melalui perangkat lunak yang mendukung EPS, "
                "lalu verifikasi font, bounding box, dan warna."
            )

        else:
            with Image.open(file_path) as image:
                image.verify()

            with Image.open(file_path) as image:
                width, height = image.size
                dpi = image.info.get("dpi")
                result.update({
                    "format": image.format,
                    "width_px": width,
                    "height_px": height,
                    "mode": image.mode,
                    "dpi_metadata": (
                        [round(float(x), 2) for x in dpi[:2]]
                        if dpi and len(dpi) >= 2 else None
                    ),
                })

                # Resolusi efektif bergantung pada ukuran cetak,
                # bukan ambang piksel tetap.
                if print_width_in <= 0 or print_height_in <= 0:
                    raise ValueError("Ukuran cetak harus lebih besar dari nol.")

                effective_dpi_x = width / print_width_in
                effective_dpi_y = height / print_height_in

                result["print_size_inches"] = [
                    print_width_in, print_height_in
                ]
                result["effective_dpi"] = [
                    round(effective_dpi_x, 2),
                    round(effective_dpi_y, 2),
                ]

                if min(effective_dpi_x, effective_dpi_y) < 300:
                    result["findings"].append(
                        "Resolusi efektif di bawah 300 DPI pada ukuran cetak "
                        f"{print_width_in} x {print_height_in} inci. "
                        "Periksa pedoman jurnal dan ukuran gambar aktual."
                    )

                if not dpi or len(dpi) < 2 or min(dpi[:2]) < 299.5:
                    result["findings"].append(
                        "Metadata DPI tidak ada atau di bawah 300. "
                        "Validasi ukuran cetak aktual; jangan sekadar "
                        "mengubah metadata DPI."
                    )

                if image.mode == "RGBA":
                    result["findings"].append(
                        "Gambar memiliki kanal alpha; periksa transparansi "
                        "pada latar dan format akhir jurnal."
                    )

            result["recommendation"] = (
                "Untuk foto, gunakan resolusi efektif sesuai pedoman jurnal. "
                "Untuk diagram garis, prioritaskan SVG/PDF/EPS atau raster "
                "dengan resolusi efektif lebih tinggi jika diwajibkan."
            )

        result["status"] = "LULUS PEMERIKSAAN DASAR" if not result["findings"] \
            else "PERLU DITINJAU"
    except Exception as exc:
        result["status"] = "ERROR"
        result["findings"].append(
            f"Gagal memeriksa file: {type(exc).__name__}: {exc}"
        )

    return result


def format_report(result: dict) -> str:
    lines = [
        "LAPORAN AUDIT VISUAL ILMIAH",
        f"File: {result.get('file')}",
        f"Format: {result.get('format', result.get('extension'))}",
        f"Status: {result.get('status')}",
        f"Ukuran file: {result.get('bytes', 0)} bytes",
    ]
    for finding in result.get("findings", []):
        lines.append(f"- TEMUAN: {finding}")
    if result.get("recommendation"):
        lines.append(f"Rekomendasi: {result['recommendation']}")
    lines.append(
        "Catatan: hasil otomatis bukan sertifikasi kualitas atau jaminan "
        "penerimaan oleh jurnal."
    )
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Audit dasar gambar untuk publikasi ilmiah"
    )
    parser.add_argument("file", help="Path gambar atau file vektor")
    args = parser.parse_args()
    print(format_report(inspect_visual(args.file)))
