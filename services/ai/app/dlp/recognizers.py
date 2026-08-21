"""Explicit Presidio recognizers for sensitive Indian public-service data."""

from dataclasses import dataclass

from presidio_analyzer import EntityRecognizer, Pattern, PatternRecognizer
from presidio_analyzer.predefined_recognizers import (
    CreditCardRecognizer,
    InAadhaarRecognizer,
    InPanRecognizer,
    InPassportRecognizer,
    InVehicleRegistrationRecognizer,
    InVoterRecognizer,
    PhoneRecognizer,
)

from app.models.enums import PIIEntityType


@dataclass(frozen=True, slots=True)
class RecognizerPolicy:
    recognizer: EntityRecognizer
    entity_type: PIIEntityType
    contexts: tuple[str, ...] = ()
    context_required: bool = False
    minimum_score: float = 0.45


AADHAAR_CONTEXT = ("aadhaar", "aadhar", "uidai", "आधार")
PAN_CONTEXT = ("pan", "permanent account number", "पैन")
PASSPORT_CONTEXT = ("passport", "passport number", "पासपोर्ट")
VOTER_CONTEXT = ("voter", "epic", "मतदाता", "वोटर")
PHONE_CONTEXT = ("phone", "mobile", "mob no", "फोन", "मोबाइल")
OTP_CONTEXT = (
    "otp",
    "one time password",
    "verification code",
    "ओटीपी",
    "सत्यापन कोड",
    "otp aaya",
)
LICENCE_CONTEXT = (
    "driving licence",
    "driving license",
    "learner licence",
    "learner license",
    "dl number",
    "ll number",
    "licence number",
    "लाइसेंस",
    "लर्नर",
)
APPLICATION_CONTEXT = (
    "application number",
    "application id",
    "application no",
    "acknowledgement",
    "receipt",
    "आवेदन संख्या",
    "रसीद",
)
VEHICLE_CONTEXT = (
    "vehicle",
    "registration number",
    "vehicle number",
    "rc number",
    "गाड़ी नंबर",
    "वाहन",
)
PAYMENT_CONTEXT = ("payment", "card", "cvv", "भुगतान", "कार्ड")
BANK_CONTEXT = (
    "bank account",
    "account number",
    "ifsc",
    "खाता संख्या",
    "बैंक खाता",
)
UPI_CONTEXT = ("upi", "upi id", "payment address", "यूपीआई")


def pattern_recognizer(
    entity: str,
    name: str,
    regex: str,
    score: float,
    contexts: tuple[str, ...] = (),
) -> PatternRecognizer:
    return PatternRecognizer(
        supported_entity=entity,
        name=name,
        patterns=[Pattern(name=name, regex=regex, score=score)],
        context=list(contexts),
        supported_language="en",
    )


def india_recognizer_policies() -> tuple[RecognizerPolicy, ...]:
    """Build an explicit registry; no implicit Presidio country defaults are used."""

    return (
        RecognizerPolicy(InAadhaarRecognizer(), PIIEntityType.AADHAAR, AADHAAR_CONTEXT),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_AADHAAR_CONTEXT",
                "DigiLicense contextual Aadhaar",
                r"(?<!\d)[2-9](?:[\s\-:]?\d){11}(?!\d)",
                0.45,
                AADHAAR_CONTEXT,
            ),
            PIIEntityType.AADHAAR,
            AADHAAR_CONTEXT,
            context_required=True,
        ),
        RecognizerPolicy(InPanRecognizer(), PIIEntityType.PAN, PAN_CONTEXT),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_PAN_OBFUSCATED",
                "DigiLicense obfuscated PAN",
                r"(?<![A-Z0-9])(?:[A-Z][\s\-]*){5}(?:\d[\s\-]*){4}[A-Z](?![A-Z0-9])",
                0.8,
                PAN_CONTEXT,
            ),
            PIIEntityType.PAN,
            PAN_CONTEXT,
        ),
        RecognizerPolicy(
            InPassportRecognizer(),
            PIIEntityType.PASSPORT,
            PASSPORT_CONTEXT,
            context_required=True,
            minimum_score=0.1,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_PASSPORT_OBFUSCATED",
                "DigiLicense obfuscated Indian passport",
                r"(?<![A-Z0-9])[A-Z][\s\-]*[1-9][\s\-]*\d"
                r"(?:[\s\-]*\d){4}[\s\-]*[1-9](?![A-Z0-9])",
                0.5,
                PASSPORT_CONTEXT,
            ),
            PIIEntityType.PASSPORT,
            PASSPORT_CONTEXT,
            context_required=True,
        ),
        RecognizerPolicy(
            InVoterRecognizer(),
            PIIEntityType.VOTER_ID,
            VOTER_CONTEXT,
            context_required=True,
            minimum_score=0.3,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_VOTER_OBFUSCATED",
                "DigiLicense obfuscated voter ID",
                r"(?<![A-Z0-9])(?:[A-Z][\s\-]*){3}(?:\d[\s\-]*){7}(?![A-Z0-9])",
                0.5,
                VOTER_CONTEXT,
            ),
            PIIEntityType.VOTER_ID,
            VOTER_CONTEXT,
            context_required=True,
        ),
        RecognizerPolicy(
            PhoneRecognizer(supported_regions=("IN",), context=list(PHONE_CONTEXT)),
            PIIEntityType.PHONE_NUMBER,
            PHONE_CONTEXT,
            minimum_score=0.3,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_MOBILE_OBFUSCATED",
                "DigiLicense Indian mobile",
                r"(?<!\d)(?:\+?[\s\-]*91[\s\-]*)?[6-9](?:[\s\-]?\d){9}(?!\d)",
                0.85,
                PHONE_CONTEXT,
            ),
            PIIEntityType.PHONE_NUMBER,
            PHONE_CONTEXT,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "OTP",
                "DigiLicense OTP",
                r"(?<!\d)(?:\d[\s\-]?){4,8}(?!\d)",
                0.4,
                OTP_CONTEXT,
            ),
            PIIEntityType.OTP,
            OTP_CONTEXT,
            context_required=True,
            minimum_score=0.4,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_DRIVING_LICENCE",
                "DigiLicense driving licence",
                r"(?<![A-Z0-9])(?:[A-Z][\s\-]*){2}(?:\d[\s\-]*){13}(?![A-Z0-9])",
                0.85,
                LICENCE_CONTEXT,
            ),
            PIIEntityType.LICENCE_NUMBER,
            LICENCE_CONTEXT,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_LEARNER_LICENCE",
                "DigiLicense learner licence",
                r"(?<![A-Z0-9])LL[\s\-]?[A-Z]{2}(?:[\s\-]?\d){8,15}(?![A-Z0-9])",
                0.85,
                LICENCE_CONTEXT,
            ),
            PIIEntityType.LICENCE_NUMBER,
            LICENCE_CONTEXT,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_APPLICATION_NUMBER",
                "DigiLicense application number",
                r"(?<![A-Z0-9])(?:[A-Z][\s\-]*){2,6}(?:\d[\s\-]*){6,14}"
                r"(?![A-Z0-9])",
                0.45,
                APPLICATION_CONTEXT,
            ),
            PIIEntityType.APPLICATION_NUMBER,
            APPLICATION_CONTEXT,
            context_required=True,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_RECEIPT_NUMBER",
                "DigiLicense receipt number",
                r"(?<![A-Z0-9])(?:[A-Z][\s\-]*){2,6}(?:\d[\s\-]*){6,14}"
                r"(?![A-Z0-9])",
                0.45,
                ("receipt", "acknowledgement", "रसीद"),
            ),
            PIIEntityType.RECEIPT_NUMBER,
            ("receipt", "acknowledgement", "रसीद"),
            context_required=True,
        ),
        RecognizerPolicy(
            InVehicleRegistrationRecognizer(),
            PIIEntityType.VEHICLE_REGISTRATION,
            VEHICLE_CONTEXT,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_VEHICLE_REGISTRATION_CONTEXT",
                "DigiLicense contextual vehicle registration",
                r"(?<![A-Z0-9])(?:[A-Z][\s\-]*){2}(?:\d[\s\-]*){1,2}"
                r"(?:[A-Z][\s\-]*){1,3}(?:\d[\s\-]*){4}(?![A-Z0-9])",
                0.5,
                VEHICLE_CONTEXT,
            ),
            PIIEntityType.VEHICLE_REGISTRATION,
            VEHICLE_CONTEXT,
            context_required=True,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_UPI_ID",
                "DigiLicense UPI ID",
                r"(?<![\w.])[A-Z0-9._-]{2,256}\s*@\s*"
                r"(?:UPI|YBL|PAYTM|OKAXIS|OKHDFCBANK|OKSBI|IBL|AXL)(?![\w.])",
                0.9,
                UPI_CONTEXT,
            ),
            PIIEntityType.UPI_ID,
            UPI_CONTEXT,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_UPI_ID_CONTEXT",
                "DigiLicense contextual UPI ID",
                r"(?<![\w.])[A-Z0-9._-]{2,256}\s*@\s*[A-Z]{2,64}(?![\w.])",
                0.5,
                UPI_CONTEXT,
            ),
            PIIEntityType.UPI_ID,
            UPI_CONTEXT,
            context_required=True,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_IFSC",
                "DigiLicense IFSC",
                r"(?<![A-Z0-9])(?:[A-Z][\s\-]*){4}0(?:[\s\-]?[A-Z0-9]){6}"
                r"(?![A-Z0-9])",
                0.85,
                BANK_CONTEXT,
            ),
            PIIEntityType.IFSC,
            BANK_CONTEXT,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IN_BANK_ACCOUNT",
                "DigiLicense bank account",
                r"(?<!\d)(?:\d[\s\-]?){9,18}(?!\d)",
                0.45,
                BANK_CONTEXT,
            ),
            PIIEntityType.BANK_ACCOUNT,
            BANK_CONTEXT,
            context_required=True,
        ),
        RecognizerPolicy(
            CreditCardRecognizer(),
            PIIEntityType.PAYMENT_CARD,
            PAYMENT_CONTEXT,
            minimum_score=0.3,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "PAYMENT_INFORMATION",
                "DigiLicense payment secret",
                r"(?<!\d)(?:\d[\s\-]?){3,4}(?!\d)",
                0.4,
                ("cvv", "cvc", "card pin", "कार्ड पिन"),
            ),
            PIIEntityType.PAYMENT_INFORMATION,
            ("cvv", "cvc", "card pin", "कार्ड पिन"),
            context_required=True,
            minimum_score=0.4,
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "ADDRESS",
                "DigiLicense address phrase",
                r"(?:my address is|mera pata|मेरा पता|पता है)\s+[^,.;!?]{5,80}",
                0.8,
                ("address", "pata", "पता"),
            ),
            PIIEntityType.ADDRESS,
            ("address", "pata", "पता"),
        ),
        RecognizerPolicy(
            pattern_recognizer(
                "IDENTITY_INFORMATION",
                "DigiLicense identity phrase",
                r"(?:my name is|mera naam|मेरा नाम|date of birth|dob is|जन्म तिथि)"
                r"\s+[^,.;!?]{2,60}",
                0.8,
                ("name", "naam", "नाम", "date of birth", "dob", "जन्म तिथि"),
            ),
            PIIEntityType.IDENTITY_INFORMATION,
            ("name", "naam", "नाम", "date of birth", "dob", "जन्म तिथि"),
        ),
    )
