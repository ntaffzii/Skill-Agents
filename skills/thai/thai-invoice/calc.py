#!/usr/bin/env python3
"""calc.py -- VAT and withholding-tax (WHT) math for Thai tax documents.

Decimal-based so totals never drift by fractions of a satang. No third-party
dependencies. Run `python3 calc.py` for the self-test.

Not legal or tax advice. Rates below are the commonly published rates at the
time this skill was written; the VAT rate in particular is fixed by a
renewable Royal Decree, not by permanent statute -- verify the current rate
against a Revenue Department (rd.go.th) source before relying on it for a
real filing. See SKILL.md "Known limitations".
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

# Reduced VAT rate in force under the current Royal Decree. Statutory rate is
# 10% (Revenue Code); it has been administratively reduced to 7% and renewed
# repeatedly. Treat this constant as provisional, not permanent.
DEFAULT_VAT_RATE = Decimal("0.07")

CENT = Decimal("0.01")

# Common withholding-tax categories under the Revenue Code (Section 3 ter /
# Section 50). Base is always the pre-VAT amount. Verify against a current
# Revenue Department source before filing -- categories and edge cases
# (e.g. rent vs. service classification) are frequently disputed in practice.
WHT_RATES = {
    "services": Decimal("0.03"),          # ค่าบริการทั่วไป -> ภ.ง.ด.3/53
    "rent": Decimal("0.05"),               # ค่าเช่าอสังหาริมทรัพย์
    "advertising": Decimal("0.02"),        # ค่าโฆษณา
    "transport": Decimal("0.01"),          # ค่าขนส่ง (ผู้ประกอบการขนส่งที่จดทะเบียน)
    "professional_fee": Decimal("0.03"),   # ค่าวิชาชีพอิสระ (individual) -> ภ.ง.ด.3
    "interest": Decimal("0.15"),           # ดอกเบี้ย -> ภ.ง.ด.2
    "dividend": Decimal("0.10"),           # เงินปันผล -> ภ.ง.ด.2
}


def _round(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_vat(subtotal, rate: Decimal = DEFAULT_VAT_RATE) -> dict:
    """VAT-exclusive subtotal -> {subtotal, vat, total}, all Decimal, rounded to satang."""
    subtotal = Decimal(str(subtotal))
    vat = _round(subtotal * rate)
    total = _round(subtotal + vat)
    return {"subtotal": subtotal, "vat": vat, "total": total, "rate": rate}


def calculate_vat_inclusive(total, rate: Decimal = DEFAULT_VAT_RATE) -> dict:
    """Back out VAT from a VAT-inclusive total -> {subtotal, vat, total}."""
    total = Decimal(str(total))
    subtotal = _round(total / (Decimal("1") + rate))
    vat = _round(total - subtotal)
    return {"subtotal": subtotal, "vat": vat, "total": total, "rate": rate}


def calculate_wht(amount, rate: Decimal) -> dict:
    """Pre-VAT amount + WHT rate -> {amount, wht, net_payable}.

    `rate` can be a Decimal or a key into WHT_RATES.
    """
    if isinstance(rate, str):
        rate = WHT_RATES[rate]
    amount = Decimal(str(amount))
    wht = _round(amount * rate)
    net_payable = _round(amount - wht)
    return {"amount": amount, "wht": wht, "rate": rate, "net_payable": net_payable}


def _self_test() -> None:
    r = calculate_vat(1000)
    assert r["subtotal"] == Decimal("1000.00")
    assert r["vat"] == Decimal("70.00")
    assert r["total"] == Decimal("1070.00")

    r = calculate_vat_inclusive(Decimal("1070.00"))
    assert r["subtotal"] == Decimal("1000.00")
    assert r["vat"] == Decimal("70.00")

    r = calculate_wht(30000, "services")
    assert r["wht"] == Decimal("900.00")
    assert r["net_payable"] == Decimal("29100.00")

    r = calculate_wht(10000, WHT_RATES["rent"])
    assert r["wht"] == Decimal("500.00")

    # Round-trip: VAT-exclusive -> total -> VAT-inclusive should agree
    excl = calculate_vat(Decimal("999.99"))
    incl = calculate_vat_inclusive(excl["total"])
    assert incl["subtotal"] == excl["subtotal"]

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
