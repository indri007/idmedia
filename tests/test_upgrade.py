from src.quality_rules import audit_document
from src.references import split_references

def test_audit_returns_priorities_and_locations():
    doc = {"pages": [{"location": "Halaman 1", "text": "Short text."}], "tables": None}
    results = audit_document(doc)
    assert results
    assert all("prioritas" in x and "lokasi" in x for x in results)

def test_reference_split_requires_heading():
    assert split_references("No references here") == []

def test_reference_split_extracts_entries():
    text = "References\n\nSmith, J. (2022). A sufficiently long reference title. https://doi.org/10.1234/example\n\n"
    assert len(split_references(text)) == 1
