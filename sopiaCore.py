#!/usr/bin/env python3
"""Pure helper logic shared across the SOPIA Suite tools.

This module deliberately has no GUI (tkinter) or imaging (Pillow)
dependencies so it can be imported and unit-tested in a headless
environment.
"""

import hashlib

# Read files in chunks rather than loading large files entirely into RAM.
CHUNK_SIZE = 8192


def hash_file(filename, hasher=hashlib.md5):
    """Return the hex digest of a file using the given hashlib constructor."""
    h = hasher()
    with open(filename, "rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def get_file_hash_md5(filename):
    """Return the MD5 hex digest of a file."""
    return hash_file(filename, hashlib.md5)


def get_file_hash_sha1(filename):
    """Return the SHA-1 hex digest of a file."""
    return hash_file(filename, hashlib.sha1)


def dms_to_decimal(dms, ref):
    """Convert a (degrees, minutes, seconds) EXIF tuple to signed decimal.

    ``ref`` is the hemisphere reference ('N'/'S' for latitude,
    'E'/'W' for longitude); 'S' and 'W' yield a negative result.
    """
    degrees, minutes, seconds = (float(value) for value in dms)
    decimal = degrees + minutes / 60 + seconds / 3600
    if str(ref).strip().upper().startswith(("S", "W")):
        decimal = -decimal
    return decimal
