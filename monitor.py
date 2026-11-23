
import hashlib
from pathlib import Path

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

file_path = Path("test.txt")

if not file_path.exists():
    print("ERROR: test.txt was not found.")
else:
    original_hash = calculate_hash(file_path)

    print("Original SHA-256:", original_hash)

    input("Modify test.txt, save it, then press Enter...")

    new_hash = calculate_hash(file_path)

    if original_hash == new_hash:
        print("SAFE: No changes detected.")
    else:
        print("ALERT: File modification detected!")
