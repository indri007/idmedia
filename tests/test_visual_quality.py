from pathlib import Path

from PIL import Image

from src.visual_quality import inspect_visual, format_report


def test_missing_file_is_reported(tmp_path: Path):
    result = inspect_visual(tmp_path / "missing.png")
    assert result["status"] == "ERROR"


def test_png_dimensions_are_reported(tmp_path: Path):
    path = tmp_path / "figure.png"
    Image.new("RGB", (1200, 900), "white").save(path, dpi=(300, 300))
    result = inspect_visual(path)
    assert result["width_px"] == 1200
    assert result["height_px"] == 900
    assert result["status"] == "LULUS PEMERIKSAAN DASAR"


def test_low_resolution_is_flagged(tmp_path: Path):
    path = tmp_path / "small.png"
    Image.new("RGB", (300, 200), "white").save(path)
    result = inspect_visual(path)
    assert result["status"] == "PERLU DITINJAU"
    assert any(
        "Resolusi efektif di bawah 300 DPI" in item
        for item in result["findings"]
    )
    assert result["effective_dpi"] == [75.0, 66.67]


def test_svg_vector_is_recognized(tmp_path: Path):
    path = tmp_path / "figure.svg"
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="100mm" height="70mm" viewBox="0 0 100 70">'
        '<path d="M0 0 L100 70" stroke="black" fill="none"/>'
        '</svg>',
        encoding="utf-8",
    )
    result = inspect_visual(path)
    assert result["format"] == "SVG (vektor)"
    assert result["viewBox"] == "0 0 100 70"


def test_svg_entity_declaration_is_rejected(tmp_path: Path):
    path = tmp_path / "unsafe.svg"
    path.write_text(
        '<!DOCTYPE svg [<!ENTITY x "y">]>'
        '<svg xmlns="http://www.w3.org/2000/svg"/>',
        encoding="utf-8",
    )
    result = inspect_visual(path)
    assert result["status"] == "ERROR"


def test_report_is_human_readable(tmp_path: Path):
    result = inspect_visual(tmp_path / "missing.png")
    report = format_report(result)
    assert "LAPORAN AUDIT VISUAL ILMIAH" in report
    assert "ERROR" in report
