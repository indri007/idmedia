from src.quality_rules import audit_text

def test_missing_sections_are_reported():
    findings = audit_text("Ini adalah naskah singkat tanpa struktur lengkap.")
    assert any("Abstrak" in item["temuan"] for item in findings)

def test_causal_claim_is_flagged():
    findings = audit_text(
        "The results show that the intervention causes a change."
    )
    assert any(item["kategori"] == "Metodologi" for item in findings)

def test_complete_sections_do_not_crash():
    text = """
    Abstract
    Introduction
    Methods
    Results
    Discussion
    Conclusion
    References
    """
    assert isinstance(audit_text(text), list)
