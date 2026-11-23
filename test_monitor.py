
import hashlib
import tempfile
import unittest
from pathlib import Path

from monitor import calculate_hash


class TestFileIntegrityMonitor(unittest.TestCase):

    def test_hash_matches_expected_value(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "sample.txt"
            content = b"Cybersecurity test file"
            file_path.write_bytes(content)

            expected = hashlib.sha256(content).hexdigest()
            actual = calculate_hash(file_path)

            self.assertEqual(actual, expected)

    def test_hash_changes_when_file_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "sample.txt"

            file_path.write_text("Original content")
            original_hash = calculate_hash(file_path)

            file_path.write_text("Modified content")
            modified_hash = calculate_hash(file_path)

            self.assertNotEqual(original_hash, modified_hash)


if __name__ == "__main__":
    unittest.main()
