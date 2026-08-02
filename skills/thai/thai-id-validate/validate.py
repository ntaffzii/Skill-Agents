#!/usr/bin/env python3
"""validate.py -- Thai national ID checksum, phone normalization, and PromptPay QR payload.

No third-party dependencies. Run `python3 validate.py` for the self-test.

All example IDs/phones in this file's self-test are synthetically generated
by the checksum function itself, not real people's data.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Thai national ID (13-digit) checksum
# ---------------------------------------------------------------------------


def compute_thai_id_checksum(first_12_digits: str) -> int:
    """Compute the 13th (check) digit for a 12-digit Thai national ID prefix.

    Algorithm: sum(d[i] * (13 - i)) for i in 0..11, weighted-mod-11 check digit
    check = (11 - (sum % 11)) % 10
    """
    if not re.fullmatch(r"\d{12}", first_12_digits):
        raise ValueError("expected exactly 12 digits")
    digits = [int(c) for c in first_12_digits]
    total = sum(d * (13 - i) for i, d in enumerate(digits))
    return (11 - (total % 11)) % 10


def validate_thai_id(id_number: str) -> bool:
    """Validate a 13-digit Thai national ID (or tax ID, same checksum scheme)."""
    cleaned = re.sub(r"[\s-]", "", id_number)
    if not re.fullmatch(r"\d{13}", cleaned):
        return False
    return compute_thai_id_checksum(cleaned[:12]) == int(cleaned[12])


def generate_test_id(first_12_digits: str) -> str:
    """Build a checksum-valid 13-digit ID from a 12-digit prefix. For synthetic test fixtures only."""
    return first_12_digits + str(compute_thai_id_checksum(first_12_digits))


# ---------------------------------------------------------------------------
# Phone number normalization
# ---------------------------------------------------------------------------


def normalize_phone(raw: str) -> str:
    """Normalize a Thai mobile/landline number to local 10-digit form starting with 0.

    Accepts "081-234-5678", "+66 81 234 5678", "66812345678", "0812345678".
    Raises ValueError if the result isn't a plausible 10-digit Thai number.
    """
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("66") and len(digits) == 11:
        digits = "0" + digits[2:]
    if not re.fullmatch(r"0\d{9}", digits):
        raise ValueError(f"not a recognizable Thai phone number: {raw!r}")
    return digits


# ---------------------------------------------------------------------------
# PromptPay QR payload (EMVCo QR Code for Payment Systems, Thai PromptPay profile)
# ---------------------------------------------------------------------------

PROMPTPAY_GUID = "A000000677010111"


def _tlv(tag: str, value: str) -> str:
    return f"{tag}{len(value):02d}{value}"


def crc16_ccitt_false(data: bytes) -> int:
    """CRC-16/CCITT-FALSE: poly 0x1021, init 0xFFFF, no reflect, xorout 0.

    Reference check value for ASCII "123456789" is 0x29B1 (see self-test).
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def build_promptpay_payload(
    proxy_type: str,
    proxy_value: str,
    amount: float | None = None,
) -> str:
    """Build an EMVCo-compliant PromptPay QR payload string.

    proxy_type: "mobile" (10-digit Thai phone) or "national_id" (13-digit ID/Tax ID).
    amount: THB amount for a dynamic (fixed-amount) QR; None for a static QR the
    payer types the amount into.
    """
    if proxy_type == "mobile":
        phone = normalize_phone(proxy_value)
        proxy_field = _tlv("01", "0066" + phone[1:])
    elif proxy_type == "national_id":
        if not validate_thai_id(proxy_value):
            raise ValueError("proxy_value fails Thai national ID checksum")
        proxy_field = _tlv("02", re.sub(r"[\s-]", "", proxy_value))
    else:
        raise ValueError("proxy_type must be 'mobile' or 'national_id'")

    merchant_account_info = _tlv("29", _tlv("00", PROMPTPAY_GUID) + proxy_field)
    poi_method = _tlv("01", "12" if amount is not None else "11")

    parts = [
        _tlv("00", "01"),          # Payload Format Indicator
        poi_method,                  # Point of Initiation Method
        merchant_account_info,       # PromptPay merchant account info
        _tlv("53", "764"),          # Currency: THB (ISO 4217 numeric)
    ]
    if amount is not None:
        parts.append(_tlv("54", f"{amount:.2f}"))
    parts.append(_tlv("58", "TH"))  # Country code

    payload_without_crc = "".join(parts) + "6304"
    crc = crc16_ccitt_false(payload_without_crc.encode("ascii"))
    return payload_without_crc + f"{crc:04X}"


def _parse_tlv(payload: str) -> dict:
    """Walk a flat TLV string (tag(2) + len(2) + value(len)) end to end.

    Use on a self-contained TLV blob, e.g. the value of a nested field like "29".
    For the *outer* PromptPay payload, strip the trailing 4-char CRC value first
    (it is not itself a TLV entry) via _parse_outer_tlv().
    """
    fields = {}
    i = 0
    while i < len(payload):
        tag = payload[i : i + 2]
        length = int(payload[i + 2 : i + 4])
        value = payload[i + 4 : i + 4 + length]
        fields[tag] = value
        i += 4 + length
    return fields


def _parse_outer_tlv(payload: str) -> dict:
    """Parse the outer PromptPay payload, excluding the trailing 4-char CRC value."""
    return _parse_tlv(payload[:-4])


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> None:
    # CRC-16/CCITT-FALSE reference check value (standard CRC catalogue vector)
    assert crc16_ccitt_false(b"123456789") == 0x29B1

    # Checksum-generated synthetic ID round-trips through the validator
    synthetic_id = generate_test_id("110170023070")
    assert len(synthetic_id) == 13
    assert validate_thai_id(synthetic_id) is True
    # Flipping the check digit must fail
    bad_id = synthetic_id[:12] + str((int(synthetic_id[12]) + 1) % 10)
    assert validate_thai_id(bad_id) is False
    # Non-digit / wrong length input must fail, not raise
    assert validate_thai_id("not-an-id") is False
    assert validate_thai_id("123") is False

    # Phone normalization
    assert normalize_phone("081-234-5678") == "0812345678"
    assert normalize_phone("+66 81 234 5678") == "0812345678"
    assert normalize_phone("66812345678") == "0812345678"
    assert normalize_phone("0812345678") == "0812345678"

    # PromptPay payload: mobile proxy, static (no amount)
    payload = build_promptpay_payload("mobile", "0812345678")
    assert payload.startswith("000201")
    assert "010211" in payload  # static POI method
    assert "5303764" in payload  # currency THB
    assert "5802TH" in payload  # country TH
    assert len(payload[-4:]) == 4  # sanity: has a 4-char CRC tail
    fields = _parse_outer_tlv(payload)
    assert fields["00"] == "01"
    assert fields["53"] == "764"
    assert fields["58"] == "TH"
    sub_fields = _parse_tlv(fields["29"])
    assert sub_fields["00"] == PROMPTPAY_GUID
    assert sub_fields["01"] == "0066812345678"
    # CRC self-consistency: recompute and compare
    body = payload[:-4]
    assert f"{crc16_ccitt_false(body.encode('ascii')):04X}" == payload[-4:]

    # Dynamic QR with amount
    payload_amt = build_promptpay_payload("mobile", "0812345678", amount=100.0)
    assert "010212" in payload_amt  # dynamic POI method
    assert "5406100.00" in payload_amt

    # National ID proxy
    id_payload = build_promptpay_payload("national_id", synthetic_id)
    id_fields = _parse_outer_tlv(id_payload)
    id_sub = _parse_tlv(id_fields["29"])
    assert id_sub["02"] == synthetic_id

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
