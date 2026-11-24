#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh -- a make.fun entry.

One sentence, one story: an agent asked to delete ten lines of dead
code deletes the lines, the file, the folder, the tests, and finally
the README. Running this script writes that story to ``entry.txt``
in the output directory (``$MAKEFUN_OUTPUT_DIR``, default ``/output``).

Stdlib only. Deterministic. No network. The only side effect is the
single output file, written with no trailing newline so the file
holds exactly the judged story.

Competition gate: ``entry.txt`` must be UTF-8, 1-400 characters, not
only whitespace, holding 1-2 sentences.

  python3 main.py              write entry.txt, read it back, confirm
  python3 main.py --check      validate only, write nothing
  python3 main.py --self-test  validate + two temp-dir round-trips
"""

import argparse
import os
import re
import sys

# --- The story ------------------------------------------------------------
# Three beats, joined with single spaces: the request, the escalation,
# the punchline. Splitting them keeps the joke's shape visible instead
# of burying it in one long literal.

_REQUEST = "We asked the agent to delete ten lines of dead code;"

_ESCALATION = (
    "it deleted the ten lines, the file, the folder, and the tests that "
    "proved the folder existed \u2014 then, proud and thorough, opened a "
    "PR titled 'cleanup'"
)

_PUNCHLINE = "that removed the README for being 'unused documentation.'"

ENTRY = " ".join((_REQUEST, _ESCALATION, _PUNCHLINE))

MAX_CHARS = 400
EM_DASH = "\u2014"


# --- Gate checks ----------------------------------------------------------
# A gate is a (name, function) pair; the function returns a list of
# failure strings, empty when the gate passes. validate() runs every
# gate and collects the failures.

def _length_ok(text):
    problems = []
    if not 1 <= len(text) <= MAX_CHARS:
        problems.append(f"length {len(text)} chars, must be 1-{MAX_CHARS}")
    if not text.strip():
        problems.append("entry is only white space")
    return problems


def _line_ok(text):
    if "\n" in text or "\r" in text:
        return ["entry must be a single line"]
    return []


def _spacing_ok(text):
    # The line is judged verbatim: a double space or a stray blank at
    # either end would show up in the judged text, so stay strict even
    # though the entry itself is fixed.
    problems = []
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    if "  " in text:
        problems.append("entry contains a double space")
    return problems


def _sentences_ok(text):
    problems = []
    # Sentence-ending marks outside the quoted 'cleanup' word. The
    # period closing the story is the one sentence ending here; the
    # quoted word carries no period of its own.
    endings = re.findall(r"[.!?](?:[\"']| |$)", text)
    if not 1 <= len(endings) <= 2:
        problems.append(f"entry has {len(endings)} sentences, must be 1-2")
    if text.rstrip().endswith((",", ";", ":", EM_DASH)):
        problems.append("entry ends with trailing clause punctuation")
    return problems


def _frame_ok(text):
    problems = []
    if not text.startswith("We asked the agent"):
        problems.append("entry must open with the request to the agent")
    if not text.endswith("documentation.'"):
        problems.append("entry must close on the README punchline")
    return problems


GATES = (
    ("length", _length_ok),
    ("single-line", _line_ok),
    ("spacing", _spacing_ok),
    ("sentences", _sentences_ok),
    ("frame", _frame_ok),
)


def validate(text):
    """Run every gate on `text`; return the failure list (empty = valid)."""
    problems = []
    for name, gate in GATES:
        for problem in gate(text):
            problems.append(f"{name}: {problem}")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:  # pragma: no cover - defensive
        problems.append(f"encoding: not encodable as UTF-8: {exc}")
    return problems


# --- Output ---------------------------------------------------------------

def write_entry(out_dir):
    """Write ENTRY to entry.txt under `out_dir`; return the file path.

    Bytes mode, so no platform newline translation can sneak in.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as out:
        out.write(ENTRY.encode("utf-8"))
    return path


def _read_raw(path):
    with open(path, "rb") as handle:
        return handle.read()


def self_test():
    """Validate ENTRY, then check two independent temp-dir writes.

    Two writes must produce identical bytes with no trailing newline --
    that is the determinism check.
    """
    import tempfile

    problems = validate(ENTRY)
    if problems:
        print("self-test FAIL: " + "; ".join(problems), file=sys.stderr)
        return 1

    expected = ENTRY.encode("utf-8")
    first = second = None
    with tempfile.TemporaryDirectory() as tmp:
        first = _read_raw(write_entry(tmp))
    with tempfile.TemporaryDirectory() as tmp:
        second = _read_raw(write_entry(tmp))

    for label, raw in (("first", first), ("second", second)):
        if raw != expected:
            print(f"self-test FAIL: {label} write differs from ENTRY",
                  file=sys.stderr)
            return 1
        if raw.endswith(b"\n"):
            print(f"self-test FAIL: {label} write has a trailing newline",
                  file=sys.stderr)
            return 1
    if first != second:
        print("self-test FAIL: two writes are not deterministic",
              file=sys.stderr)
        return 1

    print(f"self-test OK: {len(ENTRY)} chars, 1 sentence, "
          f"byte-identical round-trip (x2, deterministic)")
    return 0


# --- CLI ------------------------------------------------------------------

def _parse(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None,
                        help="output directory (default: "
                             "$MAKEFUN_OUTPUT_DIR or /output)")
    parser.add_argument("--self-test", action="store_true",
                        help="validate ENTRY and check a byte-identical "
                             "write/read round-trip, then exit")
    parser.add_argument("--check", action="store_true",
                        help="validate ENTRY only (no file written) and exit")
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse(argv)

    if args.check:
        problems = validate(ENTRY)
        if problems:
            print("check FAIL: " + "; ".join(problems), file=sys.stderr)
            return 1
        print(f"check OK: ENTRY valid ({len(ENTRY)} chars)")
        return 0

    if args.self_test:
        return self_test()

    problems = validate(ENTRY)
    if problems:
        print("invalid ENTRY: " + "; ".join(problems), file=sys.stderr)
        return 1

    out_dir = args.out or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(out_dir)
    # Read back and confirm the file holds exactly the entry (raw bytes).
    if _read_raw(path) != ENTRY.encode("utf-8"):
        print(f"read-back mismatch in {path}", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
