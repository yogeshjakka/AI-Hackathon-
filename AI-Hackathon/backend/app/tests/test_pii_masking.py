from backend.app.core.pii_masker import mask_text_for_llm, post_llm_contains_pii

def test_masking_and_post_check():
    text = "Hi, call me at +911234567890 or email me at test@example.com. I'm Yogesh."
    masked, tokens = mask_text_for_llm(text)
    assert "REDACTED" in masked
    assert isinstance(tokens, dict)

    assert post_llm_contains_pii("Call me at +919876543210") == True
    assert post_llm_contains_pii("No PII here") == False
