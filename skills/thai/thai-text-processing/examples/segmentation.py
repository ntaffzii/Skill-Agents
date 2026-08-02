#!/usr/bin/env python3
"""segmentation.py -- Thai word segmentation: the naive-split failure and the correct approach.

Thai script has NO spaces between words within a sentence (spaces mark clause/
sentence boundaries instead). `"ฉันรักการเขียนโค้ด".split(" ")` returns one
long unsegmented string, not a word list -- there is nothing to split on.

Real word segmentation needs a dictionary- or model-based tokenizer. This repo
does not vendor one (see SKILL.md "Known limitations" -- avoid vendoring
third-party code/models per this project's attribution policy). Install
PyThaiNLP separately (`pip install pythainlp`) to run the tokenizer path
below; the naive-split demonstration runs with no dependency.

Run `python3 segmentation.py` for the self-test.
"""
from __future__ import annotations


def naive_split_is_broken(text: str) -> bool:
    """Demonstrate why `.split(" ")` does not segment Thai: it returns the
    whole string as a single token whenever there's no literal space in it."""
    tokens = text.split(" ")
    return len(tokens) == 1 and len(text) > 1


def tokenize(text: str) -> list[str] | None:
    """Word-segment Thai text using PyThaiNLP if installed, else return None.

    This wraps an external library rather than reimplementing a tokenizer --
    Thai word segmentation needs a maintained dictionary/model to be accurate;
    a hand-rolled rule-based splitter would silently produce wrong boundaries.
    """
    try:
        from pythainlp.tokenize import word_tokenize
    except ImportError:
        return None
    return word_tokenize(text)


def _self_test() -> None:
    sample = "ฉันรักการเขียนโค้ดภาษาไทยมาก"

    # The failure mode this skill exists to prevent
    assert naive_split_is_broken(sample) is True
    assert sample.split(" ") == [sample]  # literally one "token" -- not segmented at all

    # A real sentence with actual spaces (clause boundary) does split on those,
    # but each resulting chunk is still unsegmented Thai, not a word list
    multi_clause = "ฉันไป ตลาด แล้วก็กลับบ้าน"
    assert len(multi_clause.split(" ")) == 3
    # None of those three chunks is further split into words by .split(" ") alone
    for chunk in multi_clause.split(" "):
        assert " " not in chunk

    # Optional path: only asserted if PyThaiNLP is actually installed
    result = tokenize(sample)
    if result is None:
        print("PyThaiNLP not installed -- skipped tokenizer self-test (naive-split demo still passed).")
    else:
        assert isinstance(result, list)
        assert len(result) > 1, "expected the sentence to segment into multiple words"
        assert "".join(result) == sample, "segmented tokens should reconstruct the original text"

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
