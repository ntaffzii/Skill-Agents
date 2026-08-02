#!/usr/bin/env python3
"""parse.py -- Thai address parsing and province/postal-code lookup.

No third-party dependencies. Run `python3 parse.py` for the self-test.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "provinces.json"


def load_provinces() -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)["provinces"]


_PROVINCES = load_provinces()
_BY_PREFIX: dict[str, list[dict]] = {}
for _p in _PROVINCES:
    if _p["postal_prefix"]:
        _BY_PREFIX.setdefault(_p["postal_prefix"], []).append(_p)


def find_province(name: str) -> dict | None:
    """Match a Thai or English province name, tolerant of 'จ.'/'จังหวัด'/'Province' prefixes and case."""
    cleaned = name.strip()
    cleaned = re.sub(r"^(จังหวัด|จ\.)\s*", "", cleaned)
    cleaned = re.sub(r"\s*Province$", "", cleaned, flags=re.IGNORECASE).strip()

    for p in _PROVINCES:
        if cleaned == p["name_th"] or cleaned.lower() == p["name_en"].lower():
            return p
    return None


def postal_prefix_to_provinces(code: str) -> list[dict]:
    """First 2 digits of a 5-digit postal code -> candidate province(s).

    Multiple provinces can share a prefix (e.g. Bangkok/Samut Prakan both '10').
    This narrows to a province-level candidate list; it does not resolve the
    exact district. Returns [] if the prefix isn't in the lookup table.
    """
    prefix = re.sub(r"\D", "", code)[:2]
    return _BY_PREFIX.get(prefix, [])


_ADDRESS_PATTERNS = {
    "postal_code": r"(?P<postal_code>\d{5})(?!\d)",
    "province": r"(?:จังหวัด|จ\.)\s*(?P<province>[ก-๙]+?)(?=\s|$|\d)",
    "district": r"(?:อำเภอ|เขต|อ\.)\s*(?P<district>[ก-๙]+?)(?=\s|$)",
    "subdistrict": r"(?:ตำบล|แขวง|ต\.)\s*(?P<subdistrict>[ก-๙]+?)(?=\s|$)",
}


def parse_thai_address(text: str) -> dict:
    """Extract postal code, province, district (อำเภอ/เขต), and subdistrict (ตำบล/แขวง) from free-text Thai address.

    This is a structural regex extractor, not a full address-parsing model — it
    expects the standard Thai particle words (จังหวัด/อำเภอ/ตำบล or their
    abbreviations) to be present. Addresses without those particles (plain
    comma-separated English-style addresses) will come back mostly empty;
    treat a mostly-empty result as "could not parse", not "no address present".
    """
    result: dict[str, str | None] = {
        "postal_code": None,
        "province": None,
        "district": None,
        "subdistrict": None,
    }
    for key, pattern in _ADDRESS_PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            result[key] = match.group(key)

    if result["province"]:
        matched = find_province(result["province"])
        if matched:
            result["province"] = matched["name_th"]

    return result


def _self_test() -> None:
    provinces = load_provinces()
    assert len(provinces) == 77, f"expected 77 provinces, got {len(provinces)}"
    assert len(set(p["name_en"] for p in provinces)) == 77, "duplicate English province name"
    assert len(set(p["name_th"] for p in provinces)) == 77, "duplicate Thai province name"

    # High-confidence, widely-cited postal prefixes
    known = {
        "Bangkok": "10", "Chiang Mai": "50", "Khon Kaen": "40",
        "Nakhon Ratchasima": "30", "Phuket": "83", "Songkhla": "90",
        "Surat Thani": "84", "Chonburi": "20",
    }
    by_en = {p["name_en"]: p for p in provinces}
    for name, prefix in known.items():
        assert by_en[name]["postal_prefix"] == prefix, f"{name} prefix mismatch"

    # Province name matching, Thai and English, with/without particles
    assert find_province("เชียงใหม่")["name_en"] == "Chiang Mai"
    assert find_province("จังหวัดเชียงใหม่")["name_en"] == "Chiang Mai"
    assert find_province("Chiang Mai")["name_en"] == "Chiang Mai"
    assert find_province("Chiang Mai Province")["name_en"] == "Chiang Mai"
    assert find_province("ไม่มีจังหวัดนี้") is None

    # Postal prefix -> province candidates (Bangkok/Samut Prakan share '10')
    candidates = postal_prefix_to_provinces("10110")
    names = {c["name_en"] for c in candidates}
    assert names == {"Bangkok", "Samut Prakan"}
    assert postal_prefix_to_provinces("50200")[0]["name_en"] == "Chiang Mai"
    assert postal_prefix_to_provinces("00000") == []

    # Full address parse
    parsed = parse_thai_address("123 หมู่ 4 ตำบลสุเทพ อำเภอเมืองเชียงใหม่ จังหวัดเชียงใหม่ 50200")
    assert parsed["postal_code"] == "50200"
    assert parsed["province"] == "เชียงใหม่"
    assert parsed["subdistrict"] == "สุเทพ"
    assert "เมืองเชียงใหม่" in parsed["district"]

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
