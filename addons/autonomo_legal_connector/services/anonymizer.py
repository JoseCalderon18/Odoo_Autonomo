import re


IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b")
NIF_RE = re.compile(r"\b(?:[XYZ]\d{7}[A-Z]|\d{8}[A-Z])\b", re.IGNORECASE)


def anonymize_text(value):
    value = value or ""
    value = IBAN_RE.sub("[IBAN]", value)
    value = NIF_RE.sub("[NIF]", value)
    return value
