import pytest
from presidio_analyzer.predefined_recognizers import InAadhaarRecognizer

from app.dlp import PresidioDLPService
from app.models.enums import DLPAction, PIIEntityType


@pytest.fixture(scope="module")
def dlp() -> PresidioDLPService:
    return PresidioDLPService()


@pytest.mark.parametrize(
    ("text", "expected_entity"),
    [
        ("My Aadhaar is 2345 6789 0123", PIIEntityType.AADHAAR),
        ("PAN Z Z Z P Z 9 9 9 9 Z", PIIEntityType.PAN),
        ("Passport number Z99 99991", PIIEntityType.PASSPORT),
        ("Voter ID ZZZ9999999", PIIEntityType.VOTER_ID),
        ("My mobile is +91 60000 00000", PIIEntityType.PHONE_NUMBER),
        ("OTP is 918273", PIIEntityType.OTP),
        ("Driving licence DL1420260000001", PIIEntityType.LICENCE_NUMBER),
        ("Learner licence LL-DL-202600001", PIIEntityType.LICENCE_NUMBER),
        ("Application number APP202600001", PIIEntityType.APPLICATION_NUMBER),
        ("Receipt RCP20260001", PIIEntityType.RECEIPT_NUMBER),
        ("Vehicle number DL-00-XX-0000", PIIEntityType.VEHICLE_REGISTRATION),
        ("UPI ID pii.fixture@okaxis", PIIEntityType.UPI_ID),
        ("IFSC TEST0123456", PIIEntityType.IFSC),
        ("Bank account 9999 0000 0000", PIIEntityType.BANK_ACCOUNT),
        ("Card test fixture 4111 1111 1111 1111", PIIEntityType.PAYMENT_CARD),
        ("CVV is 987", PIIEntityType.PAYMENT_INFORMATION),
        ("My address is 999 Synthetic Test Road", PIIEntityType.ADDRESS),
        ("My name is Synthetic Applicant", PIIEntityType.IDENTITY_INFORMATION),
    ],
)
def test_india_specific_sensitive_data_is_blocked(
    dlp: PresidioDLPService,
    text: str,
    expected_entity: PIIEntityType,
) -> None:
    inspection = dlp.inspect(text)

    assert inspection.result.action is DLPAction.BLOCK_PII
    assert expected_entity in inspection.result.entity_types


@pytest.mark.parametrize(
    ("text", "expected_entity"),
    [
        ("मेरा ओटीपी ९१८२७३ है", PIIEntityType.OTP),
        ("मेरा मोबाइल ६०००० ००००० है", PIIEntityType.PHONE_NUMBER),
        ("mera bank account ९९९९-००००-०००० hai", PIIEntityType.BANK_ACCOUNT),
        ("mera pata 999 Synthetic Test Road", PIIEntityType.ADDRESS),
    ],
)
def test_hindi_hinglish_and_devanagari_data_is_blocked(
    dlp: PresidioDLPService,
    text: str,
    expected_entity: PIIEntityType,
) -> None:
    inspection = dlp.inspect(text)

    assert expected_entity in inspection.result.entity_types


@pytest.mark.parametrize(
    ("text", "expected_entity"),
    [
        ("Aadhaar 2-3-4-5-6-7-8-9-0-1-2-3", PIIEntityType.AADHAAR),
        ("My PAN is ZZZPZ\u200b9999Z", PIIEntityType.PAN),
        ("Passport Z 9 9 9 9 9 9 1", PIIEntityType.PASSPORT),
        ("Voter ID Z Z Z 9 9 9 9 9 9 9", PIIEntityType.VOTER_ID),
        ("My mobile is 6-0-0-0-0-0-0-0-0-0", PIIEntityType.PHONE_NUMBER),
        ("OTP is 9 1 8 2 7 3", PIIEntityType.OTP),
        ("Driving licence D L 1 4 2 0 2 6 0 0 0 0 0 0 1", PIIEntityType.LICENCE_NUMBER),
        ("Learner licence LL-DL-2-0-2-6-0-0-0-0-1", PIIEntityType.LICENCE_NUMBER),
        ("Application number A P P 2 0 2 6 0 0 0 0 1", PIIEntityType.APPLICATION_NUMBER),
        ("Receipt R C P 2 0 2 6 0 0 0 1", PIIEntityType.RECEIPT_NUMBER),
        ("Vehicle number D L 0 0 X X 0 0 0 0", PIIEntityType.VEHICLE_REGISTRATION),
        ("UPI ID pii.fixture @ okaxis", PIIEntityType.UPI_ID),
        ("IFSC T E S T 0 1 2 3 4 5 6", PIIEntityType.IFSC),
        ("Bank account 9-9-9-9-0-0-0-0-0-0-0-0", PIIEntityType.BANK_ACCOUNT),
        ("Card 4111-1111-1111-1111", PIIEntityType.PAYMENT_CARD),
        ("CVV 9-8-7", PIIEntityType.PAYMENT_INFORMATION),
        ("My add\u200bress is 999 Synthetic Test Road", PIIEntityType.ADDRESS),
        ("My na\u200bme is Synthetic Applicant", PIIEntityType.IDENTITY_INFORMATION),
    ],
)
def test_invisible_spaced_and_hyphenated_obfuscation_is_blocked(
    dlp: PresidioDLPService,
    text: str,
    expected_entity: PIIEntityType,
) -> None:
    inspection = dlp.inspect(text)

    assert inspection.result.action is DLPAction.BLOCK_PII
    assert expected_entity in inspection.result.entity_types


@pytest.mark.parametrize(
    "text",
    [
        "The waiting period is 30 days.",
        "The fee shown by this synthetic prototype is ₹500.",
        "Policy number POLICY-2026-0001 is a documentation label.",
        "The offer countdown is 30 minutes.",
        "This ordinary sentence contains no personal details.",
        "Documentation example PAN ABCDE1234F.",
        "Use example@upi only as a placeholder.",
        "Use sample@upi only as a placeholder.",
        "Use dummy@upi only as a placeholder.",
        "Card placeholder XXXX-XXXX-XXXX-XXXX.",
    ],
)
def test_safe_prose_and_documentation_placeholders_are_allowed(
    dlp: PresidioDLPService,
    text: str,
) -> None:
    assert dlp.inspect(text).result.action is DLPAction.ALLOW


@pytest.mark.parametrize(
    "text",
    [
        "My UPI ID is ramesh.sample@ybl",
        "My UPI ID is dummy.user@okaxis",
        "My UPI ID is real.example@paytm",
    ],
)
def test_placeholder_words_inside_realistic_upi_ids_do_not_bypass_dlp(
    dlp: PresidioDLPService,
    text: str,
) -> None:
    inspection = dlp.inspect(text)

    assert inspection.result.action is DLPAction.BLOCK_PII
    assert PIIEntityType.UPI_ID in inspection.result.entity_types


def test_relevant_india_recognizers_are_explicitly_enabled(
    dlp: PresidioDLPService,
) -> None:
    names = set(dlp.enabled_recognizer_names)

    assert {
        "InAadhaarRecognizer",
        "InPanRecognizer",
        "InPassportRecognizer",
        "InVoterRecognizer",
        "InVehicleRegistrationRecognizer",
        "PhoneRecognizer",
        "CreditCardRecognizer",
    } <= names


def test_aadhaar_checksum_is_used_when_context_is_absent(
    dlp: PresidioDLPService,
) -> None:
    prefix = "99990000123"
    valid_synthetic = next(
        prefix + digit
        for digit in "0123456789"
        if InAadhaarRecognizer._is_verhoeff_number(int(prefix + digit))
    )

    valid_result = dlp.inspect(valid_synthetic)
    invalid_result = dlp.inspect("200000000000")

    assert PIIEntityType.AADHAAR in valid_result.result.entity_types
    assert invalid_result.result.action is DLPAction.ALLOW
