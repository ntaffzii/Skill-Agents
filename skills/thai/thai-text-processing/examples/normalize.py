#!/usr/bin/env python3
"""normalize.py -- Unicode NFC normalization for Thai text.

Pure stdlib (unicodedata), no third-party dependency. Run `python3 normalize.py`
for the self-test.

Why this matters: Thai vowels/tone marks are combining characters, and the
same visible glyph can be encoded as a single precomposed codepoint or as a
base character + combining mark sequence. Two visually identical strings can
compare unequal, fail a dictionary/database lookup, or break search/dedup if
they aren't normalized to the same form first.
"""
from __future__ import annotations

import unicodedata


def normalize_thai(text: str) -> str:
    """Normalize Thai (or any Unicode) text to NFC form.

    NFC (Normalization Form C) composes combining sequences into their
    precomposed form where one exists. Use this before comparing, sorting,
    searching, hashing, or storing user-submitted Thai text.
    """
    return unicodedata.normalize("NFC", text)


def is_normalized(text: str) -> bool:
    """True if `text` is already in NFC form (i.e. normalize_thai is a no-op)."""
    return unicodedata.is_normalized("NFC", text)


def _self_test() -> None:
    # A precomposed character vs. the same visual glyph built from base + combining mark
    # decompose then recompose to build a same-looking-but-differently-encoded pair
    sample = "กำลังใจ"
    decomposed = unicodedata.normalize("NFD", sample)
    recomposed = unicodedata.normalize("NFC", decomposed)
    assert recomposed == normalize_thai(decomposed)
    assert normalize_thai(sample) == normalize_thai(decomposed)

    # Two differently-encoded-but-visually-identical strings become equal after normalization
    assert is_normalized(normalize_thai(decomposed))

    # Idempotent: normalizing an already-normalized string is a no-op
    once = normalize_thai(sample)
    twice = normalize_thai(once)
    assert once == twice

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
