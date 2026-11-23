
import hashlib
import time
import logging
from pathlib import Path

# Project folder
BASE_DIR = Path(__file__).resolve().parent
MONITOR_DIR = BASE_DIR / "monitored_files"

# Configure security logging
logging.basicConfig(
    filename=BASE_DIR / "security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

def scan_files():
    """Create a snapshot of all monitored files."""
    hashes = {}

    for file_path in MONITOR_DIR.rglob("*"):
        if file_path.is_file():
            try:
                relative_path = file_path.relative_to(MONITOR_DIR)
                hashes[str(relative_path)] = calculate_hash(file_path)
            except OSError as error:
                logging.error("Could not read %s: %s", file_path, error)

    return hashes

def report_alert(message):
    print(message, flush=True)
    logging.warning(message)

def main():
    if not MONITOR_DIR.is_dir():
        print("ERROR: Create the monitored_files folder first.")
        return

    previous = scan_files()

    print("File Integrity Monitor started.")
    print(f"Monitoring {len(previous)} files.")
    print("Checking every 3 seconds.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(3)
            current = scan_files()

            # Detect new files
            for file in sorted(current.keys() - previous.keys()):
                report_alert(f"ALERT: File added: {file}")

            # Detect deleted files
            for file in sorted(previous.keys() - current.keys()):
                report_alert(f"ALERT: File deleted: {file}")

            # Detect modified files
            for file in sorted(current.keys() & previous.keys()):
                if current[file] != previous[file]:
                    report_alert(f"ALERT: File modified: {file}")

            previous = current

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
