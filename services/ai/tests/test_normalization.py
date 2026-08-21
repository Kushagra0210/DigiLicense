from app.normalization import normalize_for_analysis


def test_nfkc_zero_width_and_devanagari_digits_are_normalized() -> None:
    normalized = normalize_for_analysis("ＯＴＰ\u200b ९१\u200c८२\t७३")

    assert normalized.value == "OTP 9182 73"


def test_normalized_text_cannot_be_accidentally_stringified() -> None:
    normalized = normalize_for_analysis("sensitive synthetic value")

    assert str(normalized) == "[NORMALIZED_TEXT_REDACTED]"
    assert repr(normalized) == "NormalizedText([REDACTED])"
