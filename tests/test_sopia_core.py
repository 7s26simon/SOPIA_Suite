#!/usr/bin/env python3
"""Headless unit tests for the SOPIA Suite shared core logic.

Covers file hashing (including the chunked-read path for large files) and
the DMS -> decimal GPS conversion. No GUI or imaging dependencies needed:

    python3 -m unittest discover -s tests
"""

import os
import sys
import hashlib
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sopiaCore


class HashFileTests(unittest.TestCase):
    def _write_temp(self, data):
        fd, path = tempfile.mkstemp()
        self.addCleanup(os.remove, path)
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        return path

    def test_md5_matches_hashlib(self):
        data = b"SOPIA Suite forensic tools"
        path = self._write_temp(data)
        self.assertEqual(
            sopiaCore.get_file_hash_md5(path), hashlib.md5(data).hexdigest()
        )

    def test_sha1_matches_hashlib(self):
        data = b"SOPIA Suite forensic tools"
        path = self._write_temp(data)
        self.assertEqual(
            sopiaCore.get_file_hash_sha1(path), hashlib.sha1(data).hexdigest()
        )

    def test_empty_file(self):
        path = self._write_temp(b"")
        self.assertEqual(
            sopiaCore.get_file_hash_md5(path), hashlib.md5(b"").hexdigest()
        )

    def test_large_file_uses_chunked_path(self):
        # Larger than CHUNK_SIZE so the file is read in multiple chunks.
        data = os.urandom(sopiaCore.CHUNK_SIZE * 4 + 123)
        path = self._write_temp(data)
        self.assertEqual(
            sopiaCore.get_file_hash_md5(path), hashlib.md5(data).hexdigest()
        )


class DmsToDecimalTests(unittest.TestCase):
    def test_north_is_positive(self):
        # 53° 48' 0" N -> 53.8
        self.assertAlmostEqual(sopiaCore.dms_to_decimal((53, 48, 0), "N"), 53.8)

    def test_south_is_negative(self):
        self.assertAlmostEqual(sopiaCore.dms_to_decimal((53, 48, 0), "S"), -53.8)

    def test_west_is_negative(self):
        self.assertAlmostEqual(sopiaCore.dms_to_decimal((1, 30, 0), "W"), -1.5)

    def test_east_is_positive(self):
        self.assertAlmostEqual(sopiaCore.dms_to_decimal((1, 30, 0), "E"), 1.5)

    def test_seconds_contribute(self):
        # 0° 0' 3600" == 1 degree
        self.assertAlmostEqual(sopiaCore.dms_to_decimal((0, 0, 3600), "N"), 1.0)

    def test_accepts_string_ref_variants(self):
        self.assertAlmostEqual(sopiaCore.dms_to_decimal((1, 0, 0), " s "), -1.0)


if __name__ == "__main__":
    unittest.main()
