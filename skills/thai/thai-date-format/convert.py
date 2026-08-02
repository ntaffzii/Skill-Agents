#!/usr/bin/env python3
"""convert.py -- Buddhist Era (BE) / Common Era (CE) date conversion and Thai date formatting.

No third-party dependencies. Run `python3 convert.py` to execute the self-test.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

BE_OFFSET = 543

THAI_MONTHS_FULL = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม",
]

THAI_MONTHS_ABBR = [
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค.",
]

THAI_DIGITS = "๐๑๒๓๔๕๖๗๘๙"


def ce_to_be(ce_year: int) -> int:
    """Convert a Common Era year to Buddhist Era.

    Valid for the modern Thai calendar (1 Jan 1941 / BE 2484 onward, when
    Thailand's New Year's Day moved from 1 April to 1 January). Dates before
    that use a shifted BE year for Jan-Mar; this function does not model
    that historical edge case.
    """
    return ce_year + BE_OFFSET


def be_to_ce(be_year: int) -> int:
    """Convert a Buddhist Era year to Common Era. See ce_to_be() for the pre-1941 caveat."""
    return be_year - BE_OFFSET


def to_thai_digits(value: int | str) -> str:
    """Render an integer or numeral string using Thai digit glyphs (๐-๙)."""
    return "".join(THAI_DIGITS[int(ch)] if ch.isdigit() else ch for ch in str(value))


def from_thai_digits(text: str) -> str:
    """Reverse of to_thai_digits(): Thai digit glyphs back to ASCII 0-9."""
    table = {d: str(i) for i, d in enumerate(THAI_DIGITS)}
    return "".join(table.get(ch, ch) for ch in text)


@dataclass
class ThaiDate:
    day: int
    month: int
    ce_year: int

    @property
    def be_year(self) -> int:
        return ce_to_be(self.ce_year)

    @classmethod
    def from_date(cls, d: date) -> "ThaiDate":
        return cls(day=d.day, month=d.month, ce_year=d.year)

    def format(self, style: str = "formal", numerals: str = "arabic") -> str:
        """Format the date.

        style:
            "formal"   -> "16 พฤษภาคม 2568" (government/document style, BE, full month)
            "business" -> "16 พ.ค. 68" (BE, abbreviated month, 2-digit year)
            "casual"   -> "16/5/68" (BE, numeric, 2-digit year)
            "iso_ce"   -> "2025-05-16" (ISO 8601, CE — for machine interchange, not display to a Thai reader)
        numerals:
            "arabic" -> 0-9 (default; standard even in Thai-language documents)
            "thai"   -> ๐-๙ (used in some royal/ceremonial and government contexts)
        """
        if style == "iso_ce":
            return f"{self.ce_year:04d}-{self.month:02d}-{self.day:02d}"

        if style == "formal":
            text = f"{self.day} {THAI_MONTHS_FULL[self.month - 1]} {self.be_year}"
        elif style == "business":
            text = f"{self.day} {THAI_MONTHS_ABBR[self.month - 1]} {self.be_year % 100:02d}"
        elif style == "casual":
            text = f"{self.day}/{self.month}/{self.be_year % 100:02d}"
        else:
            raise ValueError(f"unknown style: {style!r}")

        return to_thai_digits(text) if numerals == "thai" else text


def format_date(d: date, style: str = "formal", numerals: str = "arabic") -> str:
    """Convenience wrapper: format a stdlib date object as a Thai date string."""
    return ThaiDate.from_date(d).format(style=style, numerals=numerals)


def _self_test() -> None:
    assert ce_to_be(2025) == 2568
    assert be_to_ce(2568) == 2025
    assert be_to_ce(ce_to_be(1999)) == 1999

    assert to_thai_digits(2568) == "๒๕๖๘"
    assert to_thai_digits("16/05/2568") == "๑๖/๐๕/๒๕๖๘"
    assert from_thai_digits("๒๕๖๘") == "2568"
    assert from_thai_digits(to_thai_digits(12345)) == "12345"

    d = date(2025, 5, 16)
    assert format_date(d, style="formal") == "16 พฤษภาคม 2568"
    assert format_date(d, style="business") == "16 พ.ค. 68"
    assert format_date(d, style="casual") == "16/5/68"
    assert format_date(d, style="iso_ce") == "2025-05-16"
    assert format_date(d, style="formal", numerals="thai") == "๑๖ พฤษภาคม ๒๕๖๘"

    # Round trip through ThaiDate
    td = ThaiDate.from_date(date(2568 - BE_OFFSET, 1, 1))
    assert td.be_year == 2568

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
