
import hashlib
import time
import logging
from pathlib import Path

# Set up security logging
logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

file_path = Path(__file__).parent / "test.txt"

if not file_path.is_file():
    print("ERROR: test.txt was not found.")
else:
    original_hash = calculate_hash(file_path)
    print("File Integrity Monitor started.")
    print("Monitoring test.txt every 3 seconds.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(3)

            if not file_path.is_file():
                message = "ALERT: Monitored file was deleted!"
                print(message)
                logging.warning(message)
                break

            try:
                new_hash = calculate_hash(file_path)
            except OSError as error:
                logging.error("Could not read file: %s", error)
                continue

            if original_hash != new_hash:
                message = "ALERT: File modification detected!"
                print(message)
                logging.warning(message)
                original_hash = new_hash

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
