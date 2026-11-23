
import hashlib
import json
import time
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MONITOR_DIR = BASE_DIR / "monitored_files"
BASELINE_FILE = BASE_DIR / "baseline.json"

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
    hashes = {}

    for file_path in MONITOR_DIR.rglob("*"):
        if file_path.is_file():
            relative_path = str(
                file_path.relative_to(MONITOR_DIR)
            )

            hashes[relative_path] = calculate_hash(file_path)

    return hashes

def report_alert(message):
    print(message, flush=True)
    logging.warning(message)

def compare_files(previous, current):
    for file in sorted(current.keys() - previous.keys()):
        report_alert(f"ALERT: File added: {file}")

    for file in sorted(previous.keys() - current.keys()):
        report_alert(f"ALERT: File deleted: {file}")

    for file in sorted(current.keys() & previous.keys()):
        if current[file] != previous[file]:
            report_alert(f"ALERT: File modified: {file}")

def save_baseline(hashes):
    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(hashes, file, indent=4)

def load_baseline():
    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def main():
    if not MONITOR_DIR.is_dir():
        print("ERROR: monitored_files folder not found.")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        hashes = scan_files()
        save_baseline(hashes)
        print(f"Baseline created for {len(hashes)} files.")
        return

    if not BASELINE_FILE.exists():
        print("No baseline found.")
        print("Run: python monitor.py --init")
        return

    baseline = load_baseline()
    current = scan_files()

    print("Checking files against saved baseline...")
    compare_files(baseline, current)

    print("File Integrity Monitor started.")
    print("Checking every 3 seconds.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(3)
            updated = scan_files()
            compare_files(current, updated)
            current = updated

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
