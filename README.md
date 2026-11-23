# python-file-integrity-monitor# Python File Integrity Monitor

## Overview
This project is a Python-based file integrity monitoring tool that uses SHA-256 hashing to detect changes made to files.

I developed this project to gain hands-on experience with Python programming, cybersecurity automation, and file integrity monitoring.

## How It Works
1. The program calculates the original SHA-256 hash of a file.
2. The user modifies the monitored file.
3. The program calculates a new hash.
4. The program compares both hashes.
5. If they differ, it displays a security alert.

## Technologies Used
- Python 3
- SHA-256 Cryptographic Hashing
- Visual Studio Code
- GitHub

## How to Run
1. Download `monitor.py` and `test.txt`.
2. Open a terminal in the project folder.
3. Run `python monitor.py`.
4. Modify and save `test.txt` when prompted.
5. Press Enter to check whether the file changed.

## Example Output

    ALERT: File modification detected!

## Skills Demonstrated
- Python scripting
- File integrity monitoring
- Cryptographic hashing
- Security automation
- Basic threat detection

## Future Improvements
- Automatically monitor multiple files
- Create timestamped security logs
- Detect added or deleted files
- Develop a graphical dashboard

## Project Purpose
This project was created as part of my hands-on cybersecurity learning and professional portfolio development.
## Project Demonstration

The screenshot below shows the Python File Integrity Monitor
detecting a modification to the monitored file.

![File Integrity Monitor Alert](file-integrity-alert.png)
