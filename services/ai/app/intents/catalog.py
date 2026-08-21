"""Fixed, reviewed assistant guidance. Raw user text is never interpolated here."""

from dataclasses import dataclass

from app.models.enums import Intent, Locale


@dataclass(frozen=True, slots=True)
class Guidance:
    answer: str
    escalation: str | None = None


ENGLISH_GUIDANCE = {
    Intent.CURRENT_STEP: Guidance(
        "Use the primary action shown on your dashboard. It reflects the next available step "
        "in this synthetic DigiLicense journey."
    ),
    Intent.LOCKED_ACTION: Guidance(
        "This action is currently locked because an earlier requirement or eligibility date "
        "has not been completed. Check the reason shown beside the action."
    ),
    Intent.WAITING_PERIOD: Guidance(
        "Your permanent-licence step remains unavailable during the learner’s-licence waiting "
        "period. DigiLicense will show the synthetic eligibility date on your dashboard."
    ),
    Intent.LEARNER_LICENCE_EXPIRY: Guidance(
        "Check the expiry date shown on your synthetic learner’s licence and complete the next "
        "eligible step before that date."
    ),
    Intent.NO_APPOINTMENT_AVAILABLE: Guidance(
        "No matching synthetic appointment is currently available for the selected preferences. "
        "You can adjust the preferences or join the DigiLicense waitlist."
    ),
    Intent.WAITLIST_EXPLANATION: Guidance(
        "The synthetic waitlist checks matching cancelled or newly simulated slots. Allocation "
        "uses the published prototype priority rules, not AI ranking."
    ),
    Intent.OFFER_EXPIRY: Guidance(
        "A synthetic appointment offer is held only until the countdown shown on the offer. If "
        "it expires or is rejected, the slot can be offered to the next matching applicant."
    ),
    Intent.MOCK_VS_REAL: Guidance(
        "DigiLicense is an independent prototype. Identity checks, payments, test results, "
        "appointments and government-record changes are simulated and affect no real system."
    ),
    Intent.PREPARATION_CHECKLIST: Guidance(
        "Review the preparation checklist on the confirmed-appointment screen. It lists the "
        "synthetic journey’s required preparation without validating real documents."
    ),
    Intent.UNSUPPORTED: Guidance(
        "I can explain the current DigiLicense step, locked actions, waiting periods, appointment "
        "availability, the waitlist, offers, simulations and preparation checklists.",
        "Use the page guidance or ask a question about the current synthetic journey.",
    ),
}

HINDI_GUIDANCE = {
    Intent.CURRENT_STEP: Guidance(
        "अपने डैशबोर्ड पर दिखाया गया मुख्य बटन चुनें। यह इस सिंथेटिक DigiLicense यात्रा में "
        "आपका अगला उपलब्ध कदम बताता है।"
    ),
    Intent.LOCKED_ACTION: Guidance(
        "यह विकल्प अभी लॉक है क्योंकि कोई पिछली आवश्यकता या पात्रता तिथि पूरी नहीं हुई है। "
        "विकल्प के पास दिखाया गया कारण देखें।"
    ),
    Intent.WAITING_PERIOD: Guidance(
        "लर्नर लाइसेंस की प्रतीक्षा अवधि के दौरान स्थायी लाइसेंस वाला कदम उपलब्ध नहीं होगा। "
        "सिंथेटिक पात्रता तिथि आपके डैशबोर्ड पर दिखाई जाएगी।"
    ),
    Intent.LEARNER_LICENCE_EXPIRY: Guidance(
        "अपने सिंथेटिक लर्नर लाइसेंस पर दिखाई गई समाप्ति तिथि देखें और उससे पहले अगला पात्र "
        "कदम पूरा करें।"
    ),
    Intent.NO_APPOINTMENT_AVAILABLE: Guidance(
        "चुनी गई प्राथमिकताओं के लिए अभी कोई मेल खाता सिंथेटिक अपॉइंटमेंट उपलब्ध नहीं है। "
        "आप प्राथमिकताएँ बदल सकते हैं या DigiLicense वेटलिस्ट में शामिल हो सकते हैं।"
    ),
    Intent.WAITLIST_EXPLANATION: Guidance(
        "सिंथेटिक वेटलिस्ट रद्द हुए या नए सिम्युलेटेड स्लॉट से मिलान करती है। आवंटन प्रकाशित "
        "प्रोटोटाइप नियमों से होता है, AI रैंकिंग से नहीं।"
    ),
    Intent.OFFER_EXPIRY: Guidance(
        "सिंथेटिक अपॉइंटमेंट ऑफर केवल दिखाए गए काउंटडाउन तक सुरक्षित रहता है। ऑफर समाप्त या "
        "अस्वीकार होने पर स्लॉट अगले मेल खाते आवेदक को दिया जा सकता है।"
    ),
    Intent.MOCK_VS_REAL: Guidance(
        "DigiLicense एक स्वतंत्र प्रोटोटाइप है। पहचान जाँच, भुगतान, परीक्षा परिणाम, अपॉइंटमेंट "
        "और सरकारी रिकॉर्ड में बदलाव सिम्युलेटेड हैं और किसी वास्तविक प्रणाली को प्रभावित नहीं करते।"
    ),
    Intent.PREPARATION_CHECKLIST: Guidance(
        "पुष्ट अपॉइंटमेंट स्क्रीन पर तैयारी सूची देखें। यह वास्तविक दस्तावेज सत्यापित किए बिना "
        "सिंथेटिक यात्रा की तैयारी बताती है।"
    ),
    Intent.UNSUPPORTED: Guidance(
        "मैं DigiLicense के वर्तमान कदम, लॉक विकल्प, प्रतीक्षा अवधि, अपॉइंटमेंट उपलब्धता, "
        "वेटलिस्ट, ऑफर, सिम्युलेशन और तैयारी सूची समझा सकता हूँ।",
        "पेज पर दी गई सहायता देखें या वर्तमान सिंथेटिक यात्रा से जुड़ा प्रश्न पूछें।",
    ),
}

PII_BLOCK_GUIDANCE = {
    Locale.ENGLISH: Guidance(
        "For your safety, do not share Aadhaar, OTP, phone, licence, application, payment or "
        "other personal details. Ask again without personal information.",
        "Use only synthetic, non-personal information in this prototype.",
    ),
    Locale.HINDI: Guidance(
        "आपकी सुरक्षा के लिए आधार, OTP, फोन, लाइसेंस, आवेदन, भुगतान या अन्य व्यक्तिगत जानकारी "
        "साझा न करें। व्यक्तिगत जानकारी हटाकर दोबारा पूछें।",
        "इस प्रोटोटाइप में केवल सिंथेटिक और गैर-व्यक्तिगत जानकारी का उपयोग करें।",
    ),
}

SAFETY_FAILURE_GUIDANCE = {
    Locale.ENGLISH: Guidance(
        "The safety check is temporarily unavailable, so I cannot process this question.",
        "Use the page’s static guidance and try again later.",
    ),
    Locale.HINDI: Guidance(
        "सुरक्षा जाँच अभी उपलब्ध नहीं है, इसलिए मैं इस प्रश्न को प्रोसेस नहीं कर सकता।",
        "पेज पर दी गई स्थिर सहायता देखें और बाद में फिर कोशिश करें।",
    ),
}


def guidance_for(intent: Intent, locale: Locale) -> Guidance:
    catalog = HINDI_GUIDANCE if locale is Locale.HINDI else ENGLISH_GUIDANCE
    return catalog[intent]

