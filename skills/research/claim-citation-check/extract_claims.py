#!/usr/bin/env python3
"""extract_claims.py -- find citation-marker patterns and pair each with its claim sentence.

This is a structural helper, not a fact-checker: it locates likely citation
markers (numeric [1], author-year (Smith, 2020), footnote ^1) and the
sentence they're attached to, so a reviewer (human or agent-with-web-access)
can then verify each one. It cannot itself confirm a citation is real or
that the source supports the claim -- that needs to actually fetch/read the
source, which this module deliberately does not do (see SKILL.md).

No dependencies. Run `python3 extract_claims.py` for the self-test.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# Citation marker patterns this helper recognizes. Deliberately conservative
# (a few common styles) rather than exhaustive -- false negatives (a missed
# citation style) are safer here than false positives (flagging non-citation
# text as a citation).
_MARKER_PATTERNS = [
    r"\[\d+(?:,\s*\d+)*\]",                          # [1] or [1, 2]
    r"\([A-Z][a-zA-Z\-]+(?:\s+et al\.)?,?\s+\d{4}\)",  # (Smith, 2020) or (Smith et al. 2020)
    r"\^\d+",                                          # footnote-style ^1
]
_MARKER_RE = re.compile("|".join(_MARKER_PATTERNS))

# Naive sentence splitter: splits on '.', '!', '?' followed by whitespace and
# a capital letter or end of string. Good enough for locating the sentence a
# marker sits in, not a linguistically complete sentence tokenizer.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z]|$)")


@dataclass
class ClaimCitation:
    sentence: str
    markers: list[str]


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]


def extract_claims_with_citations(text: str) -> list[ClaimCitation]:
    """Return every sentence that contains at least one citation marker, paired with the markers found."""
    results = []
    for sentence in split_sentences(text):
        markers = _MARKER_RE.findall(sentence)
        if markers:
            results.append(ClaimCitation(sentence=sentence, markers=markers))
    return results


def find_uncited_factual_sentences(text: str, factual_cue_words: tuple[str, ...] = (
    "%", "percent", "million", "billion", "according to", "found that", "reported that", "increased", "decreased",
)) -> list[str]:
    """Flag sentences that look like specific factual claims (contain a numeric/attribution cue)
    but have NO citation marker at all. A heuristic, not a definitive judgment -- review each hit.
    """
    flagged = []
    for sentence in split_sentences(text):
        has_marker = bool(_MARKER_RE.search(sentence))
        has_cue = any(cue in sentence.lower() for cue in factual_cue_words)
        if has_cue and not has_marker:
            flagged.append(sentence)
    return flagged


def _self_test() -> None:
    text = (
        "The market grew significantly last year. Revenue increased 24% year over year [1]. "
        "Adoption doubled in two years (Smith, 2020). "
        "This is a general statement with no specific claim. "
        "The study found that 40 percent of respondents agreed.^3"
    )

    sentences = split_sentences(text)
    assert len(sentences) == 5

    cited = extract_claims_with_citations(text)
    # 3 sentences carry a recognizable marker: the [1] one, the (Smith, 2020) one, and the ^3 one
    assert len(cited) == 3
    assert any("[1]" in c.markers for c in cited)
    assert any("(Smith, 2020)" in c.markers for c in cited)
    assert any("^3" in c.markers for c in cited)

    uncited = find_uncited_factual_sentences(text)
    # "The study found that 40 percent..." has a cue word ("percent"/"found that") AND a marker (^3) -- not flagged
    # "Revenue increased 24%..." has a marker [1] -- not flagged
    # Only sentences with a factual cue and NO marker should be flagged; this text has none such
    assert uncited == []

    # A sentence with a factual cue and genuinely no marker IS flagged
    unmarked_text = "Sales rose 15% in the region. This part is fine, no numbers here."
    flagged = find_uncited_factual_sentences(unmarked_text)
    assert len(flagged) == 1
    assert "15%" in flagged[0]

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
