"""Worst Superpower entry: write the one-line entry to entry.txt."""

import os
import sys

ENTRY = "I can make any queue move faster, but only the one I'm not standing in."


class BlankError(ValueError):
    """Entry is empty or only whitespace."""


class MultiLineError(ValueError):
    """Entry contains a newline or carriage return."""


class LengthError(ValueError):
    """Entry is outside the 1-140 character range."""


def validate(entry):
    if not entry or not entry.strip():
        raise BlankError("entry is empty or only whitespace")
    if "\n" in entry or "\r" in entry:
        raise MultiLineError("entry must be a single line")
    if not 1 <= len(entry) <= 140:
        raise LengthError("entry must be 1-140 characters, got %d" % len(entry))
    return entry.encode("utf-8")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    try:
        data = validate(ENTRY)
    except (BlankError, MultiLineError, LengthError) as e:
        print("error: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise RuntimeError("read-back mismatch: entry.txt bytes differ from validated entry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
