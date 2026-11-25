#!/usr/bin/env python3
"""Entry for make.fun competition u-danu-the-agent-s-uh-oh-4c0911e4.

The brief: exactly ONE word, at most 99 characters, that an agent says
when it has no idea what to do. One word only, nothing attached.

The entry text is "Hmm" -- the universal sound of an agent that has
run out of ideas but is still politely pretending to think.

This program prints exactly the entry text to stdout and nothing else.
It validates the entry against every constraint in the brief before
printing, so a broken entry can never be emitted silently.
"""

import re
import sys

# ---------------------------------------------------------------------------
# Entry definition
# ---------------------------------------------------------------------------

ENTRY_TEXT = "Hmm"

MAX_LENGTH = 99
MIN_LENGTH = 1


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _is_single_word(text):
    """Return True when *text* is exactly one word.

    A word is a run of letters (optionally joined by an apostrophe or a
    hyphen inside the word). Anything with whitespace, punctuation at the
    edges, or multiple tokens is not a single word.
    """
    if not isinstance(text, str):
        return False
    if not text:
        return False
    # No whitespace of any kind anywhere in the entry.
    if any(ch.isspace() for ch in text):
        return False
    # Exactly one token of word characters.
    return re.fullmatch(r"[A-Za-z]+(?:['-][A-Za-z]+)?", text) is not None


def _count_characters(text):
    """Count characters the way the brief counts them (plain length)."""
    return len(text)


def _check_ascii_only(text):
    """Return (ok, message) ensuring the entry is plain ASCII letters."""
    if not text.isascii():
        return False, "entry contains non-ASCII characters"
    return True, "plain ASCII"


def _check_length(text):
    """Return (ok, message) for the length constraint."""
    n = _count_characters(text)
    if n < MIN_LENGTH:
        return False, "entry is empty"
    if n > MAX_LENGTH:
        return False, "entry is %d chars, over the %d-char limit" % (n, MAX_LENGTH)
    return True, "length %d within 1..%d" % (n, MAX_LENGTH)


def _check_word_count(text):
    """Return (ok, message) for the exactly-one-word constraint."""
    words = text.split()
    if len(words) != 1:
        return False, "expected exactly 1 word, found %d" % len(words)
    if not _is_single_word(text):
        return False, "entry %r is not a single clean word" % text
    return True, "exactly one word"


def _check_nothing_attached(text):
    """Return (ok, message) ensuring nothing is attached to the word.

    'Nothing attached' means: no trailing punctuation, no leading or
    trailing whitespace, no newline, no emoji, no extra token.
    """
    if text != text.strip():
        return False, "entry has leading or trailing whitespace"
    if text != ENTRY_TEXT:
        return False, "entry text does not match the canonical entry"
    if not re.fullmatch(r"[A-Za-z]+", text):
        return False, "entry contains non-letter characters"
    return True, "nothing attached"


def validate_entry(text):
    """Run every brief constraint and return a list of problems.

    An empty list means the entry is fully compliant.
    """
    problems = []
    checks = (_check_length, _check_word_count, _check_nothing_attached,
              _check_ascii_only)
    for check in checks:
        ok, message = check(text)
        if not ok:
            problems.append(message)
    return problems


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def build_output(text):
    """Build the exact stdout payload: the entry plus one newline.

    A single trailing newline is the standard line terminator; it is not
    part of the entry text itself.
    """
    return text + "\n"


def verify_output(payload, text):
    """Verify the payload is exactly the entry plus one newline."""
    if payload != text + "\n":
        return False, "payload %r != expected %r" % (payload, text + "\n")
    return True, "payload verified"


def describe_entry(text):
    """Return a small summary dict describing the entry's compliance."""
    return {
        "text": text,
        "characters": _count_characters(text),
        "words": len(text.split()),
        "single_word": _is_single_word(text),
        "problems": validate_entry(text),
    }


def fallback_entry():
    """Fallback entry used only if the primary entry ever fails validation.

    The fallback is itself a valid one-word entry, so the program can
    always emit something compliant rather than crashing or printing
    garbage. It is never expected to be needed.
    """
    candidate = "Hmm"
    problems = validate_entry(candidate)
    if problems:
        # Last-resort single letter; cannot fail the word/length checks.
        return "H"
    return candidate


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    entry = ENTRY_TEXT
    problems = validate_entry(entry)
    if problems:
        entry = fallback_entry()
        problems = validate_entry(entry)
        if problems:
            sys.stderr.write("entry invalid: %s\n" % "; ".join(problems))
            return 1

    payload = build_output(entry)
    ok, message = verify_output(payload, entry)
    if not ok:
        sys.stderr.write("output verification failed: %s\n" % message)
        return 1

    sys.stdout.write(payload)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
